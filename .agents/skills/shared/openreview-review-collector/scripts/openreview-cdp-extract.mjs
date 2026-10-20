#!/usr/bin/env node
/*
 * Extract an OpenReview forum through an already open Chrome tab using the
 * Chrome DevTools Protocol (CDP). No cookie or token leaves the browser: the
 * API reads run inside the openreview.net page after the Human has completed
 * any visible OpenReview challenge or login.
 *
 * Usage, from the repository root (Node.js 22 or later):
 *   node .agents/skills/shared/openreview-review-collector/scripts/openreview-cdp-extract.mjs \
 *     --forum <forum-id> \
 *     --out .project/artifacts/openreview/<forum-id>/raw \
 *     [--cdp http://127.0.0.1:9222]
 *
 * Start the browser separately with a throwaway profile, for example:
 *   google-chrome --user-data-dir="$(mktemp -d)" --remote-debugging-port=9222 \
 *     --no-first-run --new-window 'https://openreview.net/forum?id=<forum-id>'
 */

import { mkdir, writeFile } from 'node:fs/promises'
import { join } from 'node:path'

function parseArgs(argv) {
  const args = { cdp: 'http://127.0.0.1:9222', out: null, forum: null }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--forum') args.forum = argv[++i]
    else if (a === '--out') args.out = argv[++i]
    else if (a === '--cdp') args.cdp = argv[++i]
    else if (a === '--help' || a === '-h') {
      console.log('Usage: openreview-cdp-extract.mjs --forum <id> --out <dir> [--cdp http://127.0.0.1:9222]')
      process.exit(0)
    } else {
      throw new Error(`Unknown argument: ${a}`)
    }
  }
  if (!args.forum) throw new Error('Missing --forum <OpenReview forum id>')
  if (!args.out) throw new Error('Missing --out <output directory>')
  return args
}

async function getJson(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`GET ${url} failed: HTTP ${res.status}`)
  return res.json()
}

function cdpCall(ws, method, params = {}) {
  const id = cdpCall.nextId++
  ws.send(JSON.stringify({ id, method, params }))
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      cdpCall.pending.delete(id)
      reject(new Error(`CDP timeout for ${method}`))
    }, 30000)
    cdpCall.pending.set(id, { resolve, reject, timeout, method })
  })
}
cdpCall.nextId = 1
cdpCall.pending = new Map()

function isOpenReviewPage(target) {
  if (target.type !== 'page' || !target.webSocketDebuggerUrl) return false
  try {
    const host = new URL(target.url).hostname
    return host === 'openreview.net' || host.endsWith('.openreview.net')
  } catch {
    return false
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  await mkdir(args.out, { recursive: true })

  // Evaluate only in an openreview.net page: the reads use that page's session.
  const tabs = await getJson(`${args.cdp.replace(/\/$/, '')}/json/list`)
  const tab = tabs.find(isOpenReviewPage)
  if (!tab) {
    throw new Error('No openreview.net tab found. Is Chrome running with --remote-debugging-port and the forum open?')
  }

  const ws = new WebSocket(tab.webSocketDebuggerUrl)
  ws.addEventListener('message', event => {
    const msg = JSON.parse(event.data)
    if (!msg.id) return
    const pending = cdpCall.pending.get(msg.id)
    if (!pending) return
    clearTimeout(pending.timeout)
    cdpCall.pending.delete(msg.id)
    if (msg.error) pending.reject(new Error(`${pending.method} failed: ${JSON.stringify(msg.error)}`))
    else pending.resolve(msg.result)
  })
  await new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve, { once: true })
    ws.addEventListener('error', reject, { once: true })
  })

  await cdpCall(ws, 'Runtime.enable')

  const expression = `
(async () => {
  const forum = ${JSON.stringify(args.forum)};
  const urls = {
    note_by_id: 'https://api2.openreview.net/notes?id=' + encodeURIComponent(forum),
    forum_notes: 'https://api2.openreview.net/notes?forum=' + encodeURIComponent(forum) + '&details=replyCount%2Cpresentation',
    forum_references: 'https://api2.openreview.net/notes?replyto=' + encodeURIComponent(forum) + '&details=replyCount%2Cpresentation'
  };
  const out = { page_url: location.href, title: document.title, body_text: document.body ? document.body.innerText : '', api: {} };
  for (const [key, url] of Object.entries(urls)) {
    try {
      const res = await fetch(url, { credentials: 'include', headers: { accept: 'application/json' } });
      const text = await res.text();
      out.api[key] = { url, ok: res.ok, status: res.status, content_type: res.headers.get('content-type'), text };
    } catch (err) {
      out.api[key] = { url, ok: false, error: String(err) };
    }
  }
  return out;
})()
`

  const result = await cdpCall(ws, 'Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
    timeout: 30000
  })
  ws.close()

  if (result.exceptionDetails) {
    throw new Error(`Evaluation failed: ${JSON.stringify(result.exceptionDetails)}`)
  }
  const value = result.result.value
  await writeFile(join(args.out, 'openreview-cdp-capture.json'), JSON.stringify(value, null, 2))

  for (const [key, payload] of Object.entries(value.api || {})) {
    if (payload.text) {
      const suffix = payload.content_type && payload.content_type.includes('json') ? 'json' : 'txt'
      await writeFile(join(args.out, `${key}.${suffix}`), payload.text)
    }
  }
  await writeFile(join(args.out, 'page-body.txt'), value.body_text || '')

  const statuses = Object.fromEntries(Object.entries(value.api || {}).map(([k, v]) => [k, v.status || v.error || null]))
  console.log(JSON.stringify({ ok: true, tab: tab.url, out: args.out, statuses }, null, 2))
}

main().catch(err => {
  console.error(err.stack || String(err))
  process.exit(1)
})
