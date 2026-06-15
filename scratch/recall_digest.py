"""Print a short digest of what's currently in SakThai memory.

Prototype / example only. Run: python scratch/recall_digest.py
"""

from __future__ import annotations

from sakthai.memory.store import MemoryStore


def main() -> None:
    with MemoryStore() as store:
        stats = store.stats()
        facts = store.list_facts(limit=5)
        observations = store.top_observations(limit=3)

    print("SakThai memory digest")
    print(f"  facts: {stats['facts']['total']}  observations: {stats['observations']['total']}")
    if stats["tags"]:
        top_tags = ", ".join(f"#{t} ({n})" for t, n in list(stats["tags"].items())[:5])
        print(f"  top tags: {top_tags}")

    if facts:
        print("\nRecent facts:")
        for f in facts:
            head = f"[{f.kind}] {f.key}: " if f.key else f"[{f.kind}] "
            print(f"  {head}{f.value}")

    if observations:
        print("\nTop observations:")
        for o in observations:
            print(f"  ({o.weight:.2f}) {o.summary}")


if __name__ == "__main__":
    main()
