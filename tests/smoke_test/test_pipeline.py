from core.diagnostics import build_report
from core.samples import SAMPLES


def main():
    failures = 0
    for s in SAMPLES:
        r = build_report(s["input"])
        ok = (r["formal_accepted"] == s["formal"]) and (r["system_accepted"] == s["system"])
        if not ok:
            failures += 1
        tag = "OK  " if ok else "FAIL"
        print(f"{tag} '{s['input']}' formal={r['formal_accepted']} system={r['system_accepted']} | {s['note']}")
        if not ok:
            print(f"     expected formal={s['formal']} system={s['system']}")
    print("-" * 70)
    print("ALL PASSED" if failures == 0 else f"{failures} FAILURES")


if __name__ == "__main__":
    main()