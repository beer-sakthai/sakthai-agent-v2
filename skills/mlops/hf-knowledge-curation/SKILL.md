---
name: hf-knowledge-curation
description: "Autonomous Hugging Face knowledge curation — learning-loop pattern for cron jobs and agents: discover new HF subtopics, avoid duplicates, research from external sources, and author class-level skills. Covers fallback strategies when primary scraping paths fail."
category: mlops
---

# Hugging Face Knowledge Curation

Use this skill when asked to run a learning loop: periodically pick a fresh, specific Hugging Face / AI subtopic, research it, and save a reusable class-level skill.

## Workflow

1. **Deduplicate first**
   - List existing skills (`skills_list`, `find .../SKILL.md`) in the target profile.
   - Search Supermemory (`mcp_supermemory_recall query="hf ..."`) for prior sessions on the topic.
   - Do NOT create a skill that already exists.

2. **Pick a novel, class-level subtopic**
   - Prefer class-level umbrellas over one-off narrative skills.
   - Good: "Hugging Face Optimum" (library), "Inference Providers", "XET protocol".
   - Bad: "How I debugged X today", "Summary of paper Y", "Fix error Z on 2026-06-21".

3. **Research with graceful fallback**
   - Prefer `web_search` to find authoritative sources (docs.huggingface.co, GitHub, DeepWiki).
   - Use `web_extract` for clean markdown content.
   - If `web_extract` fails twice on similar domains (billing errors, loop-warning, or repeated timeouts), pivot:
     - Try `browser_navigate` + `browser_snapshot` on the same URL or a GitHub raw path.
     - Use `web_search` to find an alternate host (e.g., DeepWiki, `raw.githubusercontent.com`, Blogs).
   - Do not continue the same failing path after a loop-warning.

4. **Author class-level skills**
   - Target shape: umbrella SKILL.md + `references/`, `templates/`, `scripts/` directories.
   - New skill path: `~/.hermes/profiles/<profile>/skills/<category>/hf-<slug>/SKILL.md`.
   - After non-trivial research or a non-obvious workaround, save the technique as a skill rather than just a memory entry.

5. **Record in Supermemory**
   - Save a durable entry summarizing the new skill topic, file path, and key facts.
   - If research is genuinely blocked and you would have to fabricate, record the no-op instead and stay silent.

## Pitfalls

- **Flat skills are discouraged.** A skill that only makes sense for a single session, PR, or date is a memory entry, not a skill.
- **Do not hardcode broken tools as permanent constraints.** If a tool fails, capture the retry/switching pattern, not the failure itself.
- **Loop-detection is real.** When the tool runtime warns about repeated identical failures, switch approach immediately.
