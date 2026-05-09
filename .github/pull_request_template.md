<!-- Polis PR template -->

## Summary

<!-- One or two sentences: what changed and why. -->

## Tier

<!-- Mark with [x] -->

- [ ] **Tier 1** — Spec / code (schemas, SDK, CLI, examples, docs). License: Apache 2.
- [ ] **Tier 2** — Reference implementation (default world / country / industry / institution config). License: CC-BY 4.0 + MIT glue.
- [ ] **Tier 3** — Original creation (royalty-bearing). Requires CLA + KYC. License: creator-owned with license-to-host grant.

## Schema impact

- [ ] No schema changes
- [ ] Touches a schema file (`polis/schemas/*.schema.json`)
  - **RFC reference:** <!-- link to RFC issue / discussion (V1+) -->
  - **Existing config impact:** <!-- which configs need to be updated to satisfy the new schema? -->

## Voice / framing review (Tier 2 + Tier 3 only)

- [ ] Reads like substrate-fictional editorial content, not chatbot / SaaS marketing
- [ ] No real-world names that would be refused by LLM-judge (verified locally)
- [ ] Information-dense (tables, named entities, real numbers); no filler
- [ ] Consistent with existing reference content (`england-on-polis/`, `football-modern-earth/`)
- [ ] Source attribution complete in `polis/configs/sources.yaml` if any public-domain corpus was adapted

## Test coverage

- [ ] Schema validators pass (`polis-cli validate ...`)
- [ ] Round-trip test passes (config validates against schema; toy basketball CI fixture still validates if schema changed)
- [ ] Unit tests added/updated for code changes
- [ ] Documentation updated where behavior changed

## Sign-off

- [ ] Commits signed off with DCO (`-s` flag)
- [ ] Tier 3 only: CLA signed (per `CONTRIBUTING.md §3`)
- [ ] License confirmed: <!-- Apache 2 / CC-BY 4.0 / Tier 3 CLA -->

## Linked issues

<!-- Closes #N, References #N, etc. -->

---

By submitting this PR, I certify that:
- I authored these changes (or have permission to contribute them)
- The contribution is licensed as marked above
- I agree to the [Code of Conduct](../CODE_OF_CONDUCT.md)
