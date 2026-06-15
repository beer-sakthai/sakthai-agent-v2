# scratch/

Throwaway prototypes and one-off experiments. **Not** part of the installed
package, not linted or type-checked in CI, and not covered by the test suite.
Don't import from here in `sakthai/`; promote anything worth keeping into the
package (with tests) first.

The original project's `scratch/` held GCP / Twilio / Dialogflow voice
experiments — those were Vertex/voice-specific and are intentionally not carried
over.

- [`recall_digest.py`](./recall_digest.py) — print a short digest of what's in
  memory. A minimal example of using `MemoryStore` directly.
