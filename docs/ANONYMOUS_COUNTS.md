# Free persistent generation count

Live status observed on 11 November 2026 (Australia/Sydney): the reviewed Blueprint has already been applied, the existing API reports `scope: persistent`, and its count survived this release deployment. This update provisions no new database or compute. The preparation notes below document the reviewed design.

The pilot observation goal is 20 completed maps per day. This does not change the existing daily AI provider-attempt limit of 10, the trial start date, or any paid plan. A provider attempt and a completed map are different measures; repairs also consume the provider budget.

`render-counts.yaml` proposes one free Render PostgreSQL database in Singapore and an update to the existing free API service. It installs the optional PostgreSQL driver and supplies the database's private connection string as `COUNTER_DATABASE_URL`. The OpenAI key and existing quota configuration are retained. The static site is unchanged by this infrastructure plan. Apply only after review and explicit approval; automatic Blueprint syncing is disabled.

The only table is `career_dna_generation_counts`, containing `generation_day DATE` and `generated_count BIGINT`. The public stats endpoint returns the summed count and today's count in Australia/Sydney time. A transaction assigns the total as the new map's generation number. Completed initial generations increment once; clarification, failure, refinement and image download do not. This measures server-completed maps, not unique visitors or guaranteed downloads. There is no visitor identifier, input text, CV, transcript or map in this table.

Render's free PostgreSQL expires 30 days after creation; it does not become a paid plan automatically. After expiry it becomes inaccessible, with a 14-day upgrade grace period before deletion. Free databases have no backups. Export the aggregate date/count rows before expiry if needed. This is suitable for the requested short pilot, not indefinite free storage.

Before approval, the app uses a process-memory counter explicitly labelled “this server run”; restarts reset it. Historical usage before the counter was deployed cannot be recovered. After database activation, numbering starts from the persisted count. If the database is unavailable, a generated map remains usable but no generation number is claimed for it; the UI says the count is unavailable.

App content remains in browser/request memory. OpenAI and the hosting provider have their own processing and retention policies, linked from the site. The existing short-lived, hashed rate-limit bookkeeping remains separate from the aggregate count and contains no experience text.
