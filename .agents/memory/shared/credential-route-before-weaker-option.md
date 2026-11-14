---
name: credential-route-before-weaker-option
date: 2026-11-14
source: RSI_light_paper `device-resources-through-project-links` record, written after a paper fell back to a weaker public route while a usable device credential existed
applies_to: paper repositories that call a service through a device-level credential
---

# Check the device's credential route before taking a weaker option

## Decision

Before switching to a public, anonymous or reduced route, check whether the
device already holds a usable credential for the service. A resource is used
through a link inside the project's `.project/`, and the check reads names and
supported readers, never values.

## Why

A route that needs no login is easy to take and quietly changes what the paper
can retrieve; the reader cannot tell a limited result from an absent one. A
failed login is not the end of the route either: an expired session, a
challenge or a wrong reader says nothing about whether the device holds a
working key.

## Apply

- Look for the project's link to the device's shared credential file and for the
  project-owned login the service needs, in the place the project records; never
  read, print or copy values.
- Separate "no credential exists" from "this reader failed": test the endpoint
  directly before concluding the route is unavailable.
- Record which route a run used, so a weaker route in the results is visible.
- Never borrow, link or restore another project's session, and never write a
  credential into Git, logs or the manifest.
