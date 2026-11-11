# Render release runbook

Published status: see [DEPLOYED.md](DEPLOYED.md). The steps below also describe future paired releases.

## Current release sources and configuration

The working branch is `pm-career-dna-live`, published to existing `main` (static frontend) and `ai-experience` (API) branches. Historical `career-dna-release` notes below are not the current source of truth. No key is tracked. The Blueprint remains paused; this update uses the existing services and merges only targeted environment keys rather than applying infrastructure changes.

- `OPENAI_CAREER_MODEL=gpt-6.1-sol`: dedicated career generation/refinement selection. Existing `OPENAI_MODEL=gpt-5` is retained as a fallback only when the dedicated variable is unset; this is not automatic failover.
- `PM_INTERNAL_TEST_TOKEN`: server-only generated secret for authenticated production testing/diagnostics. Never put it in the frontend or public docs.
- `PUBLIC_COUNTER_ENV=production`: set only on the real production API. Local/staging defaults must not count.
- Existing `OPENAI_API_KEY`, `COUNTER_DATABASE_URL`, daily provider-attempt quota and trial date are preserved.
- No runtime image-model variable is needed: visuals use SVG/local assets. Configuring an unused `OPENAI_IMAGE_MODEL` does not change this renderer.

Model access/benchmarks: [PM_MODEL_BENCHMARK.md](PM_MODEL_BENCHMARK.md). Counter receipts, legacy-count preservation and session privacy: [CAREER_STUDIO_ARCHITECTURE.md](CAREER_STUDIO_ARCHITECTURE.md).

### Existing services

- Public frontend: `product-dna-studio-preview`, https://product-dna-studio-preview.onrender.com
- API: `product-dna-studio-ai`, https://product-dna-studio-ai.onrender.com
- Confirmed workspace: Suzie's AI World.

The public frontend hostname is allowed by CORS. A custom frontend domain must be added through `ALLOWED_ORIGINS`; a separately hosted custom static frontend must also configure `API_ORIGIN` in `preview/studio.js` and rebuild the bundle. A standalone deployment uses relative same-origin API paths automatically.

## Prepare and validate

```sh
python build_preview.py
python -m unittest test_ai tests.test_e2e -v
node --check preview/studio.js
node --check preview/poster.js
# When Render CLI 2.7+ is available:
render blueprints validate render.yaml
render blueprints validate render-ai.yaml
render blueprints validate render-preview.yaml
```

JSON-schema validation is also available from https://render.com/schema/render.yaml.json. Schema validation is structural, not a substitute for Render's platform validation. No infrastructure plan has been approved as part of this prepared release.

## Publish an approved release

1. Merge the reviewed release into `main` and fast-forward `ai-experience` to the same commit. Preserve unrelated work if either branch has moved.
2. On the existing API service, retain the existing server-side `OPENAI_API_KEY`, `OPENAI_MODEL`, quota, and any trial date. The build command should be `python build_preview.py && python -m compileall -q ai_server.py career_ai.py`; start is `python ai_server.py`; health path is `/health`. Existing build commands that only compile `ai_server.py` also work because the bundle is committed and imports load `career_ai.py` at runtime.
3. Deploy the API and monitor its specific commit/deploy ID to `live`, then deploy the matching static frontend. The current static copy command can still publish the committed bundled `preview/index.html` unchanged. For future releases prefer `render-preview.yaml`'s build-and-copy command.
4. These services were connected by public repository URL and have required manual deploys despite their auto-deploy field. First inspect deploy history for a matching automatic deployment; do not create a duplicate. Trigger manually only if no deployment will happen automatically.
5. Run the smoke flow: CV/typed input → clarification if sparse → real generation → refinement consent → factual correction → unchanged unrelated fields → evidence review → direct edit review → PNG download. Check both formats and phone viewport.
6. Only set `TRIAL_START_DATE=YYYY-MM-DD` when the owner explicitly starts the seven-day pilot; preparation does not start it.

The old live client uses `/api/generate`, while this release uses `/api/career-dna/*`. The rollout is a paired API/frontend release: announce a brief preview maintenance window and refresh old browser tabs. This avoids pretending the retired schema is compatible. Roll back **both services to the previous matching commits** if the smoke flow fails; no database migration needs reversing.

## Optional standalone deployment

`render.yaml` is a single free Python web service that serves both the bundled UI and API, with no disk or database. Configure its secret through Render Environment, not YAML. `render-ai.yaml`/`render-preview.yaml` document the existing two-service setup; do not apply all manifests together and create duplicate services. Review any proposed Blueprint plan before applying it.

`Dockerfile` is an optional equivalent container build. The nonpersistent runtime uses the Python standard library. Optional persistent counts install the PostgreSQL driver from `requirements.txt`. The container runs as an unprivileged user and takes its API key only from the runtime environment.

Free hosting remains subject to Render's included usage allowances. OpenAI generation/refinement charges are separate. No paid infrastructure or public trial date is provisioned by this prepared release.

## Anonymous counter pilot

See [ANONYMOUS_COUNTS.md](ANONYMOUS_COUNTS.md) and `render-counts.yaml`. The prepared free plan creates only a date/count database and connects the existing free API. It was subsequently applied through the Dashboard; live stats now report persistent counting. This release preserves that connection. Original Render plan review: https://dashboard.render.com/blueprint/exs-dbprosek1f9s73cpln4g/sync/exe-dbprosmk1f9s73cplo6g . Explicit approval of this reviewed plan is required before applying it. The existing provider-attempt limit stays 10/day; 20 completed maps/day is only an observation target.
