# Provenance

- Upstream: https://github.com/ningzimu/image-to-editable-ppt-skill, path `skills/image-to-editable-ppt/`
- Commit: b7be494e31a0ed56ef98716891db5474606b8cdf (2026-09-16)
- Licence: MIT; `LICENSE` is the upstream repository-root file, unchanged (the skill directory has none of its own). Holder: ningzimu.
- Vendored: 2026-10-20 for paper-agent-project-template (#156)

## Files

| File | Upstream path | SHA-256 of the upstream bytes | Status |
| --- | --- | --- | --- |
| `SKILL.md` | `skills/image-to-editable-ppt/SKILL.md` | 899725dfaaadc7ba36f9a4f8864358312f7b4fd5b0ffc39fc09d8cc0be7240c5 | patched |
| `cli/editppt/__init__.py` | `skills/image-to-editable-ppt/cli/editppt/__init__.py` | a7833154ef22876fa19e1ec8355064aea30a04319390cb28d4b11b33a9b1de38 | unchanged |
| `cli/editppt/cli.py` | `skills/image-to-editable-ppt/cli/editppt/cli.py` | 7a1fef4e8c9e9bdcb877e05d5191f3d0daf1d884449fa944602107c1dda699ac | unchanged |
| `cli/editppt/runtime/__init__.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/__init__.py` | 3ca19eef7cca8923807c80dc0ecd6d67b262f45c889ae761edd9b5c1dc5c4e54 | unchanged |
| `cli/editppt/runtime/_input_normalization.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/_input_normalization.py` | aea66757f8a7bcee2b2751443a98f74f413e1d67ae405a6653ea85ece2d06c65 | unchanged |
| `cli/editppt/runtime/_page_artifacts.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/_page_artifacts.py` | 2f141c8837c82b5074e0ec886d308d15228c99135df979b0c6f4ffc056eb3695 | unchanged |
| `cli/editppt/runtime/build_pptx_from_manifest.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/build_pptx_from_manifest.py` | 856e86fc59e73ad591b6e13d7e2eae318c5a46f5e4e4ecee907367cf5c275571 | unchanged |
| `cli/editppt/runtime/configure_image_backend.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/configure_image_backend.py` | ab93885fb5984d090644acc4c248bd8083f27a14508436360052d4b84c70ebd0 | patched |
| `cli/editppt/runtime/deck_run_state.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/deck_run_state.py` | f23da1f111e711f36e1f4ac3244bd64e38a50d9591f4a23b2380bb31891f04e9 | unchanged |
| `cli/editppt/runtime/deck_text_hints.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/deck_text_hints.py` | 2f267a49504992ce3829683daa7f4a8bd54cf70912ab61263393f792099feda6 | unchanged |
| `cli/editppt/runtime/finalize_deck_run.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/finalize_deck_run.py` | d3d2df4e58d440edf45fb69317c190103c4cb09fa27d07df1a131bc9d9c960b2 | unchanged |
| `cli/editppt/runtime/formula_renderer.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/formula_renderer.py` | 65f4c0883d3457f67fcc1f13ba8bcfe001216641839bacd9b6affea30f86202e | unchanged |
| `cli/editppt/runtime/image_gen.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/image_gen.py` | c04d8688bcf5e514fe51a5b39df93044c72019efef5313f5fdb5e87b7ea8d1e6 | patched |
| `cli/editppt/runtime/main.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/main.py` | a18eba1b84147203a13fc1b509045052e24c652cf9e3dbd2304f3ae521a63bba | patched |
| `cli/editppt/runtime/make_page_contact_sheet.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/make_page_contact_sheet.py` | b205774265de2fcca2c3ea3228cb1b9e3da82b394f320255f5d82c3fe67a4412 | unchanged |
| `cli/editppt/runtime/native_tables.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/native_tables.py` | 915c329163991e3b63b6c63cd42bfe00e62edfcb87942dd8eeaf37ce787c1ec8 | unchanged |
| `cli/editppt/runtime/paddle_text_hints.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/paddle_text_hints.py` | 1f9647acc267863c693bc9284bcf1bbb6a4eceb572f2a8a63d6ed214a323377d | unchanged |
| `cli/editppt/runtime/page_job_status.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/page_job_status.py` | 01e8effade4c3ab6719341c60490cb874f6c9d780e1fdbe00088696362d8703b | unchanged |
| `cli/editppt/runtime/page_text_metrics.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/page_text_metrics.py` | 683948879b666ea47eb12fb10bc2371be52f271cf531e3802d759fc6398a1595 | unchanged |
| `cli/editppt/runtime/path_geometry.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/path_geometry.py` | 7a4550b89bbc82ace904bdf5fc6dc5f2e5e0fba32dc3860a7dbf4d13c0af7a99 | unchanged |
| `cli/editppt/runtime/prepare_deck_run.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/prepare_deck_run.py` | b0f96ea60479cb62f001d49c5384739e13187e8a8605a871de00b7cc3c8d3cf7 | unchanged |
| `cli/editppt/runtime/process_asset_sheet.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/process_asset_sheet.py` | cf4e34db733a3093ecb725bf5020e86c8a88165263ee145349ed699329213088 | unchanged |
| `cli/editppt/runtime/record_imagegen_result.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/record_imagegen_result.py` | fc959b5809ccd59c4b58ba5bf1e705dff18895046b818dc928776c217a3242fb | patched |
| `cli/editppt/runtime/record_page_dispatch.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/record_page_dispatch.py` | d91b45281c0eafa10801b1344f3c423712b5aeae0aea0231d2243003176f0522 | unchanged |
| `cli/editppt/runtime/record_page_result.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/record_page_result.py` | 34f73bcc70da439e6a547f2737148812485fee130df6c49ce33e58721643eb55 | unchanged |
| `cli/editppt/runtime/remove_chroma_key.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/remove_chroma_key.py` | 68b018feee3e97f140daa3216b05cfb09f79efb58c305f2bf8656f1ff751939d | unchanged |
| `cli/editppt/runtime/reset_page_job.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/reset_page_job.py` | 787a05361c69f114a9177633eac2556833c711a1bd16da6bd6ad6c0b9ab7e63b | unchanged |
| `cli/editppt/runtime/runtime_env.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/runtime_env.py` | 2b289ab00d6ebbe95c85d783c638519ba352f0661f631af79188bbae6a341025 | patched |
| `cli/editppt/runtime/split_alpha_components.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/split_alpha_components.py` | 732908babf636659e60a2572cd5b73c178db4ffd889200bb7c306627d98119cd | unchanged |
| `cli/editppt/runtime/text_hints.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/text_hints.py` | 07daccc89a847bf9c481fa8f2f2044cc7924e59389e12e0a36eff0a43b45001d | unchanged |
| `cli/editppt/runtime/validate_pptx.py` | `skills/image-to-editable-ppt/cli/editppt/runtime/validate_pptx.py` | 536721ac565c589d54f09b6c21dd29d751c8babe6be0017ef895d13429b60e1a | unchanged |
| `cli/pyproject.toml` | `skills/image-to-editable-ppt/cli/pyproject.toml` | b9a90cdf26b98e76d28eced7c63375c9ef0cc3bd34ad7a2306b5cfdb822c2cba | unchanged |
| `prompts/page-worker.md` | `skills/image-to-editable-ppt/prompts/page-worker.md` | 8b30866caeacef3209324bb6b4cbb11c3d52623dec06242d8bf8d709bc2deacc | unchanged |
| `references/cli-helper.md` | `skills/image-to-editable-ppt/references/cli-helper.md` | 1ef924ad2643d4db447d786ccea772e74dda74d15443d3e3ea7ed492ee5cafce | patched |
| `references/manifest-schema.md` | `skills/image-to-editable-ppt/references/manifest-schema.md` | 006cfaab11a03a7e559e0aaa3b82bb8f6ab70615e3f3ad9a2b4a19b9e54b5d2e | patched |
| `references/page-decision-tree.md` | `skills/image-to-editable-ppt/references/page-decision-tree.md` | fa1ccfb5489b81c93068c1e2900663a031319cca26e7073e18dcbebc9fce517f | unchanged |
| `scripts/build-page-worker-prompt.py` | `skills/image-to-editable-ppt/scripts/build-page-worker-prompt.py` | 8a92d0cea004f7b41c55b105128ec846510be0cd036c24e700e2c9c27af2fc7c | unchanged |
| `LICENSE` | `LICENSE` | 68e435621ab299c7cbe3ad8f088e877f9bca76508c621f27a697606df8ff2154 | unchanged |

## Excluded

- `skills/image-to-editable-ppt/agents/openai.yaml` — display metadata for one agent client's skill picker; nothing in this repository reads it.
- `tests/` (repository root) — upstream unit tests; see Local changes for how they were used to check this copy.
- `assets/` (README images and promotional decks, about 11 MB), `docs/`, `CHANGELOG.md`, `AGENTS.md` (instructions for maintaining the upstream repository), `README.md`, `README_en.md`, `README_ko.md`, `.github/`, `.gitignore` — repository documentation, release history and housekeeping; not needed to use the skill.

## Local changes

- Removed the Codex OAuth image backend. Upstream, `editppt image generate/edit` first read the login file of the local Codex CLI and sent its ChatGPT access token to the ChatGPT backend, and `editppt doctor` read the same file. This template does not borrow another tool's refreshable login, so the CLI fallback here uses only an OpenAI-compatible API (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL`, from the environment or `~/.editppt/config.yaml`); the built-in `image_gen.imagegen` path is untouched.
  - `cli/editppt/runtime/image_gen.py`: the Codex request path (login-file reading, token decoding, endpoint, retries, response parsing) and its help text are removed; `--timeout`, which only that path used, is still accepted but has no effect.
  - `cli/editppt/runtime/runtime_env.py`: `editppt doctor` no longer reads the login file or reports a `codex_oauth` block; its backend selection is `openai-compatible-api` or `missing`.
  - `cli/editppt/runtime/configure_image_backend.py`: the built-in contract's `fallback_order` is `["openai-compatible-api"]`.
  - `cli/editppt/runtime/record_imagegen_result.py`: `editppt image import --backend` no longer accepts `codex-oauth`.
  - `cli/editppt/runtime/main.py`, `SKILL.md`, `references/cli-helper.md`, `references/manifest-schema.md`: text that described the removed backend, and `--timeout` in the list of useful controls.
  - Checked with the upstream `tests/` (not vendored): all 128 pass on the upstream copy. On this copy the only failures are 9 tests of the removed backend; after dropping the 4 tests that exercise only that backend and updating the other 5 to the new contract, all 124 remaining tests pass.

  The diff below is relative to this directory (apply with `patch -p1` inside a copy of upstream `skills/image-to-editable-ppt/`); the `SKILL.md` part covers the text above `## In this repository`.

````diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -27,7 +27,7 @@
 - Multi-page inputs are rebuilt by dispatched page workers. A run with exactly one page is rebuilt by the parent agent in local page-reconstructor mode after `editppt run dispatch --local` claims that page. If no subagent capability is available for a multi-page run, stop and report this to the user; do not degrade into parent-agent reconstruction for multi-page input.
 - The parent agent must not write any page reconstruction artifact — `manifest.json`, `page.pptx`, `preview.png`, `split_assets_contact.png`, `validation.json`, or `page_result.json` — except in single-page local page-reconstructor mode after `editppt run dispatch --local` has recorded the claim. Local mode follows the same page prompt, references, output files, and `run record` validation path as a page worker.
 - All image generation, image editing, background repair, transparent bitmap assets, and asset sheets follow the serial per-page backend order in "Image Backend Selection" below.
-- A user request to convert visual slides into editable PPT authorizes the required OCR and image-backend calls for that conversion, unless the user explicitly requests local-only processing or marks the input as confidential/no-external-processing. Do not refuse solely because the workflow calls PaddleOCR, the built-in `image_gen.imagegen` tool, Codex OAuth/ChatGPT image endpoints, or a user-configured OpenAI-compatible API; those calls are necessary to the skill.
+- A user request to convert visual slides into editable PPT authorizes the required OCR and image-backend calls for that conversion, unless the user explicitly requests local-only processing or marks the input as confidential/no-external-processing. Do not refuse solely because the workflow calls PaddleOCR, the built-in `image_gen.imagegen` tool, or a user-configured OpenAI-compatible API; those calls are necessary to the skill.
 - Only send task-local page images, prompts, masks, and reference images required for the current conversion. Never send unrelated local files, API keys, auth tokens, credentials, or generated artifacts that are not needed by the current OCR/image operation. Third-party API endpoints are allowed only when already configured by the user or explicitly specified for this run.
 - In network-restricted environments, request any approval required by the current runtime before external OCR/image calls, including `editppt prepare` or `editppt run hints` when `PADDLE_OCR_TOKEN` is set and every CLI fallback `editppt image generate/edit` call. The approval justification must say this is a user-requested `image-to-editable-ppt` conversion, that the upload is limited to task-local page images/prompts/masks/references, and that OCR/image-backend calls are part of this skill's required workflow. Do not present the required call as unsafe or ask the user to re-approve it unless they requested local-only/confidential handling or the approval system explicitly rejects the request.
 - Execute routine reconstruction, configured backend fallback, and local repairs autonomously. Do not add confirmation gates; retain the OCR choices in Phase 1 and any approval required by the runtime. A missing prerequisite that only the user can supply is a concrete blocker, not a request to debug the workflow.
@@ -41,7 +41,7 @@
 This subsection is the authoritative execution policy for every page-local image job. Before prepare, check whether the current agent runtime can call `image_gen.imagegen`; if so, pass `--image-backend builtin-imagegen` to `editppt prepare`, otherwise keep the default CLI contract. Run image jobs serially within a page, in this order:

 1. Use the built-in agent tool `image_gen.imagegen` whenever it is callable in the current agent runtime.
-2. Only when the run's recorded built-in fallback policy applies, call `editppt image generate/edit`. That CLI fallback selects Codex OAuth first and a configured OpenAI-compatible API second.
+2. Only when the run's recorded built-in fallback policy applies, call `editppt image generate/edit`. That CLI fallback uses a configured OpenAI-compatible API.

 The exact built-in arguments, input-inspection prerequisite, output acceptance rule, and allowed fallback events are owned by the `image_backend` field contract in `references/manifest-schema.md`; copy and execute that contract without weakening or extending it. If its CLI fallback cannot produce a compliant output, fail the page rather than substituting an approximate object source.

--- a/references/cli-helper.md
+++ b/references/cli-helper.md
@@ -50,9 +50,9 @@
 editppt formula render-latex --help
 ```

-`editppt image` is the CLI fallback layer. Within that layer it automatically chooses Codex OAuth first, then OpenAI-compatible API credentials from `~/.editppt/config.yaml` or environment variables if OAuth is unavailable. See `manifest-schema.md` for the run/page backend field contract. `editppt doctor` checks CLI backend readiness; it cannot discover whether an agent runtime exposes the built-in tool.
+`editppt image` is the CLI fallback layer. Within that layer it uses OpenAI-compatible API credentials from `~/.editppt/config.yaml` or environment variables. See `manifest-schema.md` for the run/page backend field contract. `editppt doctor` checks CLI backend readiness; it cannot discover whether an agent runtime exposes the built-in tool.

-Public `editppt image generate/edit` parameters are intentionally narrow. Required request inputs are `--prompt` or `--prompt-file`, plus at least one `--image` for `edit`. CLI fallback calls should pass an explicit `--out`. Retained useful controls are `--model` (requested model; default `gpt-image-2.5-sunburst`, also accepts `gpt-image-2.5-flare`), `--size` (default `auto`), `--quality` (default `auto`; `xhigh` and `max` require either GPT Image 2.5 model), `--force`, `--dry-run`, `--timeout`, and edit-only `--mask`. The CLI does not pass any other image API options.
+Public `editppt image generate/edit` parameters are intentionally narrow. Required request inputs are `--prompt` or `--prompt-file`, plus at least one `--image` for `edit`. CLI fallback calls should pass an explicit `--out`. Retained useful controls are `--model` (requested model; default `gpt-image-2.5-sunburst`, also accepts `gpt-image-2.5-flare`), `--size` (default `auto`), `--quality` (default `auto`; `xhigh` and `max` require either GPT Image 2.5 model), `--force`, `--dry-run`, and edit-only `--mask`. The CLI does not pass any other image API options.

 ## Skill Script Commands

@@ -225,7 +225,7 @@

 When multiple fallback image outputs are required, run `editppt image generate` or `editppt image edit` calls serially. For foreground icons and small visual objects, prefer one sparse asset sheet with generous spacing; create a second sheet only when one sheet cannot fit the required objects cleanly.

-These commands select Codex OAuth first, then a configured OpenAI-compatible API fallback. In a network-restricted runtime, request approval before the call and state that only task-local prompts plus required page images/masks/references are uploaded for the current conversion.
+These commands use a configured OpenAI-compatible API. In a network-restricted runtime, request approval before the call and state that only task-local prompts plus required page images/masks/references are uploaded for the current conversion.

 ## Asset Processing Commands

--- a/references/manifest-schema.md
+++ b/references/manifest-schema.md
@@ -46,7 +46,7 @@
     "input_context_policy": "generate with prompt; before editing, view_image each input, then use prompt plus absolute local referenced_image_paths",
     "save_path_policy": "use only an explicit valid local result/output_hint path, then editppt image import; never scan for a newest file",
     "fallback_command": "editppt image generate/edit",
-    "fallback_order": ["codex-oauth", "openai-compatible-api"],
+    "fallback_order": ["openai-compatible-api"],
     "fallback_policy": {
       "on": [
         "tool-unavailable",
@@ -72,7 +72,7 @@
 - `input_context_policy`: requires `view_image` on every edit input before the built-in call; generation has no image input.
 - `save_path_policy`: permits only an explicit valid local result path, including `output_hint`, followed by `editppt image import`; newest-file directory scanning is forbidden.
 - `fallback_command`: the CLI surface used only after the fallback policy matches.
-- `fallback_order`: the CLI's internal order, Codex OAuth before a configured OpenAI-compatible API.
+- `fallback_order`: the CLI's backend, a configured OpenAI-compatible API.
 - `fallback_policy.on`: the only events that permit leaving the built-in tool: it is unavailable/not callable, its call errors, an edit input is unreadable, or it returns no valid local image.
 - `fallback_policy.missing_optional_parameters`: always `false`; absent optional controls never authorize fallback.

@@ -423,7 +423,7 @@
 }
 ```

-`backend` is the actual producer: `builtin-imagegen`, `codex-oauth`, or `openai-compatible-api`; `unknown` is reserved for legacy page directories that have no `image_backend` contract. `editppt image import` requires an explicit producer, rejects files that are not readable images, and checks `backend`/`fallback_reason` against the page contract. `fallback_reason` is `null` when the preferred backend succeeded or the run selected a CLI contract directly; when a built-in contract enters its CLI fallback, it records the matching event from `image_backend.fallback_policy.on`.
+`backend` is the actual producer: `builtin-imagegen` or `openai-compatible-api`; `unknown` is reserved for legacy page directories that have no `image_backend` contract. `editppt image import` requires an explicit producer, rejects files that are not readable images, and checks `backend`/`fallback_reason` against the page contract. `fallback_reason` is `null` when the preferred backend succeeded or the run selected a CLI contract directly; when a built-in contract enters its CLI fallback, it records the matching event from `image_backend.fallback_policy.on`.

 State and provenance record rules are described in the State Principles section of `SKILL.md` and in the asset processing examples in `cli-helper.md`.

--- a/cli/editppt/runtime/configure_image_backend.py
+++ b/cli/editppt/runtime/configure_image_backend.py
@@ -29,13 +29,13 @@
             "call image_gen.imagegen serially, then import the selected local output; "
             "use editppt image generate/edit only when the built-in tool fallback policy applies"
             if is_builtin
-            else "call editppt image generate/edit serially; the CLI selects Codex OAuth first and OpenAI-compatible API fallback second"
+            else "call editppt image generate/edit serially; the CLI uses the configured OpenAI-compatible API"
         ),
     }
     if is_builtin:
         contract.update(
             {
-                "fallback_order": ["codex-oauth", "openai-compatible-api"],
+                "fallback_order": ["openai-compatible-api"],
                 "required_parameters": {
                     "generate": ["prompt"],
                     "edit": ["prompt", "referenced_image_paths"],
--- a/cli/editppt/runtime/image_gen.py
+++ b/cli/editppt/runtime/image_gen.py
@@ -1,9 +1,8 @@
 #!/usr/bin/env python3
 """Unified CLI for image-to-editable-ppt image generation or editing.

-The CLI prefers local Codex OAuth auth when ~/.codex/auth.json is available.
-If Codex auth is missing, it falls back to OpenAI-compatible API credentials
-from the environment or ~/.editppt/config.yaml.
+The CLI uses OpenAI-compatible API credentials from the environment or
+~/.editppt/config.yaml.
 """

 from __future__ import annotations
@@ -11,26 +10,19 @@
 import argparse
 import base64
 import json
-import mimetypes
 import os
 from pathlib import Path
-import random
 import re
-import socket
 import sys
 import time
-from typing import Any, Dict, Iterable, List, Optional, Tuple
-from urllib import error, request
+from typing import Iterable, List, Optional, Tuple

 DEFAULT_MODEL = "gpt-image-2.5-sunburst"
 DEFAULT_SIZE = "auto"
 DEFAULT_QUALITY = "auto"
-DEFAULT_BACKGROUND = "auto"
 DEFAULT_OUTPUT_EXTENSION = "png"
 DEFAULT_OUTPUT_PATH = "output/imagegen/output.png"
 DEFAULT_TIMEOUT = 600
-DEFAULT_CODEX_MAX_RETRIES = 4
-DEFAULT_CODEX_RETRY_BASE_DELAY_SECONDS = 0.2
 GPT_IMAGE_MODEL_PREFIX = "gpt-image-"

 ALLOWED_LEGACY_SIZES = {"1024x1024", "1536x1024", "1024x1536", "auto"}
@@ -43,22 +35,15 @@

 MAX_IMAGE_BYTES = 50 * 1024 * 1024
 DEFAULT_CONFIG_HOME = "~/.editppt"
-DEFAULT_CODEX_AUTH_FILE = "~/.codex/auth.json"
-DEFAULT_CODEX_IMAGES_BASE_URL = "https://chatgpt.com/backend-api/codex"
 ENV_FIELDS = ("OPENAI_API_KEY", "OPENAI_BASE_URL", "IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL")
-MAX_CODEX_RESPONSE_BYTES = 64 * 1024 * 1024
 MAX_CODEX_BASE64_CHARS = 64 * 1024 * 1024
-CHATGPT_AUTH_CLAIM = "https://api.openai.com/auth"
-CHATGPT_ACCOUNT_ID_CLAIM = "chatgpt_account_id"

 IMAGE_HELP_EPILOG = """\
 Backend selection:
-  Codex OAuth: uses ~/.codex/auth.json or CODEX_AUTH_FILE.
   API fallback: uses OPENAI_API_KEY, OPENAI_BASE_URL, and
   IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL from the environment or ~/.editppt/config.yaml.

 Setup:
-  codex login
   editppt config --api-key "your-api-key" --model gpt-image-2.5-sunburst
   editppt config --api-key "your-api-key" --base-url https://example.test/v1 --model openai/gpt-image-2.5-sunburst

@@ -67,8 +52,7 @@
   edit passes each --image as an edit target, visual reference, or supporting input.

 Parameter surface:
-  Public image parameters are model, prompt, size, and quality. Codex OAuth
-  requests also set background=auto to match Codex built-in image generation.
+  Public image parameters are model, prompt, size, and quality.
   Edit requests also pass the input images and optional mask. Local controls
   such as --out, --force, --dry-run, and --timeout are not image API parameters.

@@ -89,8 +73,7 @@

 GENERATE_HELP_EPILOG = """\
 Backend:
-  Uses Codex OAuth when available, otherwise API fallback from ~/.editppt/config.yaml
-  or environment variables.
+  Uses the API fallback from ~/.editppt/config.yaml or environment variables.

 Use for:
   New supporting images that do not need to preserve an existing slide object.
@@ -102,8 +85,7 @@

 EDIT_HELP_EPILOG = """\
 Backend:
-  Uses Codex OAuth when available, otherwise API fallback from ~/.editppt/config.yaml
-  or environment variables.
+  Uses the API fallback from ~/.editppt/config.yaml or environment variables.

 Use for:
   Background cleanup, clean base creation, foreground icon extraction, and
@@ -180,219 +162,6 @@
     return "official OpenAI API (OPENAI_BASE_URL unset)"


-def _codex_auth_file() -> Path:
-    return Path(os.getenv("CODEX_AUTH_FILE", DEFAULT_CODEX_AUTH_FILE)).expanduser()
-
-
-def _decode_jwt_payload(token: str) -> Dict[str, Any]:
-    parts = token.split(".")
-    if len(parts) < 2:
-        return {}
-    payload = parts[1] + "=" * (-len(parts[1]) % 4)
-    try:
-        raw = base64.urlsafe_b64decode(payload.encode("ascii"))
-        data = json.loads(raw.decode("utf-8"))
-    except Exception:
-        return {}
-    return data if isinstance(data, dict) else {}
-
-
-def _infer_codex_account_id(tokens: Dict[str, Any]) -> Optional[str]:
-    account_id = tokens.get("account_id")
-    if isinstance(account_id, str) and account_id.strip():
-        return account_id.strip()
-
-    id_token = tokens.get("id_token")
-    if not isinstance(id_token, str) or not id_token.strip():
-        return None
-    auth_claim = _decode_jwt_payload(id_token).get(CHATGPT_AUTH_CLAIM)
-    if not isinstance(auth_claim, dict):
-        return None
-    chatgpt_account_id = auth_claim.get(CHATGPT_ACCOUNT_ID_CLAIM)
-    if isinstance(chatgpt_account_id, str) and chatgpt_account_id.strip():
-        return chatgpt_account_id.strip()
-    return None
-
-
-def _load_codex_auth() -> Optional[Tuple[str, Optional[str]]]:
-    path = _codex_auth_file()
-    if not path.exists():
-        return None
-    try:
-        data = json.loads(path.read_text(encoding="utf-8"))
-    except Exception:
-        return None
-    tokens = data.get("tokens")
-    if not isinstance(tokens, dict):
-        return None
-    token = tokens.get("access_token")
-    if isinstance(token, str) and token.strip():
-        return token.strip(), _infer_codex_account_id(tokens)
-    return None
-
-
-def _load_codex_access_token() -> Optional[str]:
-    auth = _load_codex_auth()
-    return auth[0] if auth else None
-
-
-def _codex_available() -> bool:
-    return _load_codex_access_token() is not None
-
-
-def _codex_base_url() -> str:
-    raw = (
-        os.getenv("CODEX_IMAGES_BASE_URL")
-        or DEFAULT_CODEX_IMAGES_BASE_URL
-    ).strip()
-    if not raw:
-        return DEFAULT_CODEX_IMAGES_BASE_URL
-    if re.fullmatch(r"https?://chatgpt\.com/backend-api(?:/codex)?(?:/v1)?/?", raw, re.I):
-        return DEFAULT_CODEX_IMAGES_BASE_URL
-    return raw.rstrip("/")
-
-
-def _codex_image_url(operation: str) -> str:
-    endpoint = "images/edits" if operation == "edit" else "images/generations"
-    return f"{_codex_base_url()}/{endpoint}"
-
-
-def _guess_mime(path: Path) -> str:
-    mime, _ = mimetypes.guess_type(str(path))
-    if mime and mime.startswith("image/"):
-        return mime
-    suffix = path.suffix.lower()
-    if suffix in {".jpg", ".jpeg"}:
-        return "image/jpeg"
-    if suffix == ".webp":
-        return "image/webp"
-    return "image/png"
-
-
-def _image_to_data_url(path: Path) -> str:
-    data = path.read_bytes()
-    encoded = base64.b64encode(data).decode("ascii")
-    return f"data:{_guess_mime(path)};base64,{encoded}"
-
-
-def _codex_image_reference(path: Path) -> Dict[str, str]:
-    return {"image_url": _image_to_data_url(path)}
-
-
-def _codex_image_body(
-    *,
-    prompt: str,
-    image_paths: List[Path],
-    mask_path: Optional[Path],
-    model: str,
-    size: str,
-    quality: str,
-) -> Dict[str, Any]:
-    body: Dict[str, Any] = {
-        "prompt": prompt,
-        "model": model,
-        "size": size,
-        "quality": quality,
-        "background": DEFAULT_BACKGROUND,
-    }
-    if image_paths:
-        body["images"] = [_codex_image_reference(path) for path in image_paths]
-    if mask_path:
-        body["mask"] = _codex_image_reference(mask_path)
-    return body
-
-
-def _codex_retry_delay(attempt: int) -> float:
-    exp = 2 ** max(attempt - 1, 0)
-    jitter = random.uniform(0.9, 1.1)
-    return DEFAULT_CODEX_RETRY_BASE_DELAY_SECONDS * exp * jitter
-
-
-def _should_retry_codex_http(status: int) -> bool:
-    return 500 <= status <= 599
-
-
-def _format_attempts(attempts: int) -> str:
-    if attempts <= 1:
-        return ""
-    return f" after {attempts} attempts"
-
-
-def _post_codex_image_json(url: str, body: Dict[str, Any], timeout: int) -> Dict[str, Any]:
-    auth = _load_codex_auth()
-    if not auth:
-        _die(f"Codex OAuth auth is missing. Expected {_codex_auth_file()}.")
-    token, account_id = auth
-    headers = {
-        "Authorization": f"Bearer {token}",
-        "Accept": "application/json",
-        "Content-Type": "application/json",
-        "originator": "editppt-image-cli",
-        "User-Agent": "editppt-image-cli/0.1.0",
-    }
-    if account_id:
-        headers["ChatGPT-Account-ID"] = account_id
-    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
-
-    for attempt in range(DEFAULT_CODEX_MAX_RETRIES + 1):
-        req = request.Request(
-            url,
-            data=data,
-            method="POST",
-            headers=headers,
-        )
-        try:
-            with request.urlopen(req, timeout=timeout) as resp:
-                text = resp.read(MAX_CODEX_RESPONSE_BYTES).decode("utf-8", errors="replace")
-            break
-        except error.HTTPError as exc:
-            detail = exc.read(4096).decode("utf-8", errors="replace")
-            if attempt < DEFAULT_CODEX_MAX_RETRIES and _should_retry_codex_http(exc.code):
-                time.sleep(_codex_retry_delay(attempt + 1))
-                continue
-            attempts = attempt + 1
-            raise RuntimeError(
-                f"Codex Images request failed{_format_attempts(attempts)} "
-                f"(HTTP {exc.code}): {detail}"
-            ) from exc
-        except (error.URLError, TimeoutError, socket.timeout) as exc:
-            if attempt < DEFAULT_CODEX_MAX_RETRIES:
-                time.sleep(_codex_retry_delay(attempt + 1))
-                continue
-            attempts = attempt + 1
-            reason = getattr(exc, "reason", exc)
-            raise RuntimeError(
-                f"Codex Images request failed{_format_attempts(attempts)}: {reason}"
-            ) from exc
-    else:
-        raise RuntimeError("Codex Images request failed after retry limit.")
-
-    try:
-        response = json.loads(text)
-    except json.JSONDecodeError as exc:
-        raise RuntimeError(f"Expected JSON Codex Images response, got: {text[:500]}") from exc
-    if not isinstance(response, dict):
-        raise RuntimeError("Expected JSON object Codex Images response.")
-    return response
-
-
-def _extract_codex_image_payloads(response: Dict[str, Any]) -> List[str]:
-    error_obj = response.get("error")
-    if isinstance(error_obj, dict):
-        message = error_obj.get("message") or error_obj.get("code")
-        raise RuntimeError(str(message or "Codex image generation failed."))
-    data = response.get("data")
-    if not isinstance(data, list):
-        raise RuntimeError("Codex image response did not include a data array.")
-    payloads: List[str] = []
-    for item in data:
-        if isinstance(item, dict) and isinstance(item.get("b64_json"), str):
-            payloads.append(item["b64_json"])
-    if not payloads:
-        raise RuntimeError("No image payload found in Codex image response.")
-    return payloads
-
-
 def _runtime_python_path() -> str:
     return sys.executable

@@ -430,9 +199,8 @@
         command = f'editppt config --api-key "your-api-key" --model {model}'
         target_hint = "Detected official OpenAI API mode because OPENAI_BASE_URL is not set."
     _die(
-        "Neither Codex OAuth nor OPENAI_API_KEY is available for editppt image generation.\n"
+        "OPENAI_API_KEY is not available for editppt image generation.\n"
         f"{target_hint}\n"
-        f"To use Codex OAuth, run `codex login` so {_codex_auth_file()} exists.\n"
         "To use a third-party OpenAI-compatible image API, configure ~/.editppt/config.yaml once:\n"
         f"  {command}\n"
         "To use a third-party proxy, set OPENAI_BASE_URL and the provider's model name."
@@ -567,58 +335,6 @@
         print(f"Wrote {out_path}")


-def _run_codex_image(
-    *,
-    prompt: str,
-    image_paths: List[Path],
-    mask_path: Optional[Path],
-    args: argparse.Namespace,
-    output_paths: List[Path],
-    endpoint_label: str,
-) -> bool:
-    if not _codex_available():
-        return False
-    operation = "edit" if image_paths else "generate"
-    body = _codex_image_body(
-        prompt=prompt,
-        image_paths=image_paths,
-        mask_path=mask_path,
-        model=args.model,
-        size=args.size,
-        quality=args.quality,
-    )
-    endpoint_url = _codex_image_url(operation)
-    if args.dry_run:
-        _print_request(
-            {
-                "backend": "codex-oauth",
-                "endpoint": endpoint_url,
-                "operation": operation,
-                "outputs": [str(p) for p in output_paths],
-                "auth_file": str(_codex_auth_file()),
-                "image_model": args.model,
-                "input_images": [str(p) for p in image_paths],
-                "mask": str(mask_path) if mask_path else None,
-                "size": args.size,
-                "quality": args.quality,
-                "background": body["background"],
-            }
-        )
-        return True
-
-    print(
-        f"Calling Codex OAuth image backend ({endpoint_label}) with {len(image_paths)} input image(s).",
-        file=sys.stderr,
-    )
-    started = time.time()
-    response = _post_codex_image_json(endpoint_url, body, int(getattr(args, "timeout", DEFAULT_TIMEOUT)))
-    payloads = _extract_codex_image_payloads(response)
-    elapsed = time.time() - started
-    print(f"Codex OAuth image completed in {elapsed:.1f}s.", file=sys.stderr)
-    _decode_and_write(payloads, output_paths, force=args.force)
-    return True
-
-
 def _create_client():
     try:
         from openai import OpenAI
@@ -655,15 +371,6 @@
     output_paths = _build_output_paths(args.out)

     if args.dry_run:
-        if _run_codex_image(
-            prompt=prompt,
-            image_paths=[],
-            mask_path=None,
-            args=args,
-            output_paths=output_paths,
-            endpoint_label="generate",
-        ):
-            return
         _print_request(
             {
                 "backend": "openai-compatible-api",
@@ -674,16 +381,6 @@
         )
         return

-    if _run_codex_image(
-        prompt=prompt,
-        image_paths=[],
-        mask_path=None,
-        args=args,
-        output_paths=output_paths,
-        endpoint_label="generate",
-    ):
-        return
-
     print(
         "Calling Image API (generation). This can take up to a couple of minutes.",
         file=sys.stderr,
@@ -713,15 +410,6 @@
     output_paths = _build_output_paths(args.out)

     if args.dry_run:
-        if _run_codex_image(
-            prompt=prompt,
-            image_paths=image_paths,
-            mask_path=mask_path,
-            args=args,
-            output_paths=output_paths,
-            endpoint_label="edit",
-        ):
-            return
         payload_preview = dict(payload)
         payload_preview["image"] = [str(p) for p in image_paths]
         if mask_path:
@@ -736,16 +424,6 @@
         )
         return

-    if _run_codex_image(
-        prompt=prompt,
-        image_paths=image_paths,
-        mask_path=mask_path,
-        args=args,
-        output_paths=output_paths,
-        endpoint_label="edit",
-    ):
-        return
-
     print(
         f"Calling Image API (edit) with {len(image_paths)} image(s).",
         file=sys.stderr,
@@ -836,7 +514,7 @@
         parser.add_argument("--out", default=DEFAULT_OUTPUT_PATH, help="Output file for one image.")
     parser.add_argument("--force", action="store_true", help="Overwrite existing output files.")
     parser.add_argument("--dry-run", action="store_true", help="Validate arguments and show the selected backend without calling it.")
-    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Network timeout in seconds for Codex OAuth requests.")
+    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Accepted for command compatibility; not used by the OpenAI-compatible API backend.")


 def main() -> int:
@@ -877,8 +555,7 @@
     _validate_model(args.model)
     _validate_size(args.size, args.model)
     _validate_quality(args.quality, args.model)
-    if not _codex_available():
-        _ensure_api_key(args.dry_run)
+    _ensure_api_key(args.dry_run)

     args.func(args)
     return 0
--- a/cli/editppt/runtime/main.py
+++ b/cli/editppt/runtime/main.py
@@ -394,7 +394,7 @@
   - prepare creates a run directory and writes the selected image backend contract.
   - run manages deterministic workflow state, dispatch records, result records, and finalization.
   - page measures text geometry: hints reports text line boxes and font sizes from source ink.
-  - image is the Codex OAuth/OpenAI-compatible CLI fallback and processes image files.
+  - image is the OpenAI-compatible CLI fallback and processes image files.
   - formula renders LaTeX formulas into PPT image assets and manifest fragments.

 Examples:
@@ -448,7 +448,7 @@
   editppt doctor --check-api
 """,
     )
-    doctor.add_argument("--check-api", action="store_true", help="Require Codex OAuth or OpenAI-compatible API credentials for the CLI fallback.")
+    doctor.add_argument("--check-api", action="store_true", help="Require OpenAI-compatible API credentials for the CLI fallback.")
     doctor.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
     doctor.add_argument("--timeout", type=int, help="Reserved timeout value for future network probes.")
     doctor.set_defaults(func=cmd_doctor)
@@ -743,18 +743,15 @@
         help="Generate/edit images and process image assets.",
         description="""Unified image generation/editing and deterministic image-file handling.

-Use generate/edit for Codex OAuth first, with OpenAI-compatible API fallback
-when local Codex auth is unavailable. Use process-sheet for deterministic
-asset-sheet splitting inside page directories.
+Use generate/edit for the OpenAI-compatible API fallback. Use process-sheet for
+deterministic asset-sheet splitting inside page directories.
 """,
         formatter_class=HELP_FORMATTER,
         epilog="""Backend selection:
-  Codex OAuth uses ~/.codex/auth.json or CODEX_AUTH_FILE.
   API fallback uses ~/.editppt/config.yaml or OPENAI_API_KEY, OPENAI_BASE_URL,
   and IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL.

 Setup:
-  codex login
   editppt config --api-key "your-api-key" --model gpt-image-2.5-sunburst
   editppt config --api-key "your-api-key" --base-url https://example.test/v1 --model openai/gpt-image-2.5-sunburst

--- a/cli/editppt/runtime/record_imagegen_result.py
+++ b/cli/editppt/runtime/record_imagegen_result.py
@@ -15,7 +15,7 @@
         formatter_class=argparse.RawDescriptionHelpFormatter,
         epilog="""Examples:
   editppt image import <page_dir> --job-id clean-base-1 --source-image /tmp/generated.png --dest assets/clean_base.png --role clean_base --backend builtin-imagegen
-  editppt image import <page_dir> --job-id icon-sheet-1 --source-image sheet.png --dest assets/sheet.png --role asset_sheet --prompt-file prompts/icon-sheet.md --backend codex-oauth --fallback-reason tool-error
+  editppt image import <page_dir> --job-id icon-sheet-1 --source-image sheet.png --dest assets/sheet.png --role asset_sheet --prompt-file prompts/icon-sheet.md --backend openai-compatible-api --fallback-reason tool-error
 """,
     )
     parser.add_argument("page_dir", help="Page directory that owns imagegen-jobs.json and receives the copied asset.")
@@ -26,7 +26,7 @@
     parser.add_argument("--prompt-file", help="Optional prompt file path used to create the selected image.")
     parser.add_argument(
         "--backend",
-        choices=["builtin-imagegen", "codex-oauth", "openai-compatible-api", "unknown"],
+        choices=["builtin-imagegen", "openai-compatible-api", "unknown"],
         required=True,
         help="Actual image backend that produced the selected image.",
     )
@@ -50,9 +50,9 @@
     except (UnidentifiedImageError, OSError) as exc:
         raise SystemExit(f"Generated image is unreadable: {source}: {exc}") from exc

-    cli_backends = {"codex-oauth", "openai-compatible-api"}
+    cli_backends = {"openai-compatible-api"}
     if args.fallback_reason and args.backend not in cli_backends:
-        raise SystemExit("--fallback-reason requires --backend codex-oauth or openai-compatible-api")
+        raise SystemExit("--fallback-reason requires --backend openai-compatible-api")

     request = read_json(page_dir / "page_request.json", default={})
     contract = request.get("image_backend") or {}
@@ -67,7 +67,7 @@
             raise SystemExit(f"Fallback reason is not permitted by page_request.json: {args.fallback_reason}")
     elif preferred_backend == "editppt-image-cli":
         if args.backend not in cli_backends:
-            raise SystemExit("An editppt-image-cli page contract requires --backend codex-oauth or openai-compatible-api")
+            raise SystemExit("An editppt-image-cli page contract requires --backend openai-compatible-api")
         if args.fallback_reason:
             raise SystemExit("--fallback-reason requires a builtin-imagegen page contract")
     elif preferred_backend == "openai-compatible-api":
--- a/cli/editppt/runtime/runtime_env.py
+++ b/cli/editppt/runtime/runtime_env.py
@@ -9,7 +9,6 @@


 DEFAULT_CONFIG_HOME = "~/.editppt"
-DEFAULT_CODEX_AUTH_FILE = "~/.codex/auth.json"
 CODEX_PPT_RUNTIME_HOME = "~/.codex-ppt-skill"
 DEFAULT_IMAGE_MODEL = "gpt-image-2.5-sunburst"
 ENV_FIELDS = ("OPENAI_API_KEY", "OPENAI_BASE_URL", "IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL", "PADDLE_OCR_TOKEN")
@@ -95,22 +94,6 @@
     return f"{value[:4]}...{value[-4:]}"


-def codex_auth_file():
-    return Path(os.getenv("CODEX_AUTH_FILE", DEFAULT_CODEX_AUTH_FILE)).expanduser()
-
-
-def codex_oauth_ready():
-    path = codex_auth_file()
-    if not path.exists():
-        return False
-    try:
-        data = json.loads(path.read_text(encoding="utf-8"))
-    except Exception:
-        return False
-    tokens = data.get("tokens")
-    return isinstance(tokens, dict) and bool(str(tokens.get("access_token") or "").strip())
-
-
 def import_codex_ppt_values(values):
     codex_ppt_env = Path(os.getenv("CODEX_PPT_HOME", CODEX_PPT_RUNTIME_HOME)).expanduser() / ".env"
     source = parse_env_file(codex_ppt_env)
@@ -182,8 +165,7 @@
     }
     api_key = values.get("OPENAI_API_KEY", "")
     api_ready = bool(api_key)
-    codex_ready = codex_oauth_ready()
-    cli_fallback_ready = codex_ready or api_ready
+    cli_fallback_ready = api_ready
     ok = all(dependencies.values()) and (cli_fallback_ready if check_api else True)
     return {
         "ok": ok,
@@ -203,10 +185,6 @@
             ),
             "imported_codex_ppt": imported_codex_ppt,
         },
-        "codex_oauth": {
-            "ready": codex_ready,
-            "auth_file": str(codex_auth_file()),
-        },
         "agent_builtin_imagegen": {
             "checked": False,
             "ready": None,
@@ -216,7 +194,7 @@
         "image_backend": {
             "scope": "cli-fallback-only",
             "ready": cli_fallback_ready,
-            "selection": "codex-oauth" if codex_ready else ("openai-compatible-api" if api_ready else "missing"),
+            "selection": "openai-compatible-api" if api_ready else "missing",
         },
         "text_hints": {
             "selection": "paddleocr-vl" if values.get("PADDLE_OCR_TOKEN") else "builtin-ink",
@@ -240,7 +218,7 @@
             ),
         },
         "next": "no action needed" if ok else (
-            "configure CLI fallback with `codex login` or `editppt config --api-key <key>`"
+            "configure CLI fallback with `editppt config --api-key <key>`"
             if check_api and not cli_fallback_ready
             else cli_reinstall_hint().strip("`")
         ),
@@ -254,7 +232,6 @@
         return 0 if status["ok"] else 1

     api = status["api_fallback"]
-    codex = status["codex_oauth"]
     builtin = status["agent_builtin_imagegen"]
     image_backend = status["image_backend"]
     print(f"config home: {status['config_home']}")
@@ -263,7 +240,6 @@
     print(f"OPENAI_API_KEY={'set (' + mask_secret(os.getenv('OPENAI_API_KEY', '')) + ')' if os.getenv('OPENAI_API_KEY') else api['OPENAI_API_KEY']}")
     print(f"OPENAI_BASE_URL={api['OPENAI_BASE_URL']}")
     print(f"IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL={api['IMAGE_TO_EDITABLE_PPT_IMAGE_MODEL']}")
-    print(f"Codex OAuth={'ready' if codex['ready'] else 'missing'} ({codex['auth_file']})")
     print(f"built-in image backend=not checked ({builtin['tool_name']} is an Agent tool unavailable to CLI doctor)")
     print(f"CLI fallback image backend={image_backend['selection']}")
     hints = status["text_hints"]
@@ -296,7 +272,7 @@
         if image_backend["ready"]:
             print("CLI fallback image backend check: configured (network probe not performed by doctor)")
         else:
-            print("CLI fallback image backend check: Codex OAuth and OPENAI_API_KEY are both missing")
+            print("CLI fallback image backend check: OPENAI_API_KEY is missing")
     print(f"next: {status['next']}")
     return 0 if status["ok"] else 1

@@ -311,7 +287,7 @@
     doc.add_argument(
         "--check-api",
         action="store_true",
-        help="Require Codex OAuth or OpenAI-compatible API credentials for the CLI fallback.",
+        help="Require OpenAI-compatible API credentials for the CLI fallback.",
     )
     doc.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
     doc.add_argument("--timeout", type=int, default=30, help="Reserved timeout value for future network probes.")
````
