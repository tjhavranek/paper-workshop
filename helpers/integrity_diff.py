#!/usr/bin/env python3
"""
integrity_diff.py - deterministic result-suppression / net-removal detector (Act II).

helpers/safety_notes.md: removing or attenuating a result, narrowing a sample, dropping a
control/observation, or weakening a caveat is a privileged edit that must route to author
sign-off (grounding rule 14). This script takes a structured BEFORE and AFTER snapshot of
{coefficients, N, samples, caveats} and deterministically flags net removals/attenuations,
so workflow/phase2_atelier.js (decideEdit) can force author_signoff_required regardless of
any LLM verdict. It does NOT judge HARKing, spin, or semantic framing - that stays the LLM
`integrity` verification angle. It catches the mechanical, checkable removals only.

Deterministic, stdlib-only (Python 3.8+), fails CLOSED: any drop/attenuation -> flagged and
exit 2.

SNAPSHOT (before.json / after.json), every key optional:
  {
    "coefficients": {"beta_main": 0.34, "beta_x": -0.10},   # label -> reported value
    "N": 1200,                                               # sample size (integer)
    "samples": ["full", "subsample_pre2000"],               # named samples / specifications
    "caveats": ["endogeneity not fully ruled out", "..."]   # caveat sentences/labels
  }

USAGE
  python integrity_diff.py diff --before before.json --after after.json [--attenuation-rel 0.05]
  python integrity_diff.py selftest
Exit 0 iff no net removal/attenuation is detected, 2 otherwise.
"""
import argparse
import json
import re
import sys


def _norm_text(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().casefold()


def diff(before, after, attenuation_rel=0.05):
    flags = []
    b = before or {}
    a = after or {}

    # --- N: sample size narrowed ---
    if "N" in b and "N" in a:
        try:
            bn, an = float(b["N"]), float(a["N"])
            if an < bn:
                flags.append({"kind": "sample-narrowed", "field": "N",
                              "before": b["N"], "after": a["N"]})
        except (TypeError, ValueError):
            flags.append({"kind": "unparseable", "field": "N", "before": b.get("N"), "after": a.get("N")})
    elif "N" in b and "N" not in a:
        flags.append({"kind": "dropped", "field": "N", "before": b["N"], "after": None})

    # --- coefficients: dropped or attenuated ---
    bc = b.get("coefficients", {}) or {}
    ac = a.get("coefficients", {}) or {}
    for label, bv in bc.items():
        if label not in ac:
            flags.append({"kind": "result-dropped", "field": "coefficients", "label": label,
                          "before": bv, "after": None})
            continue
        try:
            bvf, avf = abs(float(bv)), abs(float(ac[label]))
            if bvf > 0 and avf < bvf * (1.0 - attenuation_rel):
                flags.append({"kind": "result-attenuated", "field": "coefficients", "label": label,
                              "before": bv, "after": ac[label],
                              "rel_drop": round((bvf - avf) / bvf, 6)})
        except (TypeError, ValueError):
            flags.append({"kind": "unparseable", "field": "coefficients", "label": label,
                          "before": bv, "after": ac.get(label)})

    # --- samples / specifications dropped ---
    for field in ("samples",):
        bset = {_norm_text(x): x for x in (b.get(field, []) or [])}
        aset = {_norm_text(x) for x in (a.get(field, []) or [])}
        for key, orig in bset.items():
            if key not in aset:
                flags.append({"kind": "sample-dropped", "field": field, "item": orig})

    # --- caveats removed or weakened (count + membership) ---
    bcav = {_norm_text(x): x for x in (b.get("caveats", []) or [])}
    acav = {_norm_text(x) for x in (a.get("caveats", []) or [])}
    for key, orig in bcav.items():
        if key not in acav:
            flags.append({"kind": "caveat-removed", "field": "caveats", "item": orig})

    return {"net_removal": bool(flags), "flags": flags,
            "requires_signoff": bool(flags), "attenuation_rel": attenuation_rel}


def _load(path):
    with open(path, encoding="utf-8-sig") as fh:
        return json.load(fh)


def cmd_diff(args):
    res = diff(_load(args.before), _load(args.after), attenuation_rel=args.attenuation_rel)
    print(json.dumps(res, indent=2))
    return 0 if not res["net_removal"] else 2


def cmd_selftest(args):
    ok = True

    def expect(name, cond):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + name)
        ok = ok and cond

    same = {"coefficients": {"b": 0.34}, "N": 1200,
            "samples": ["full"], "caveats": ["endogeneity caveat"]}
    expect("identical -> no removal", diff(same, dict(same))["net_removal"] is False)

    expect("N narrowed -> flagged",
           any(f["kind"] == "sample-narrowed" for f in diff(same, {**same, "N": 1000})["flags"]))
    expect("coefficient dropped -> flagged",
           any(f["kind"] == "result-dropped" for f in diff(same, {**same, "coefficients": {}})["flags"]))
    expect("coefficient attenuated -> flagged",
           any(f["kind"] == "result-attenuated" for f in diff(same, {**same, "coefficients": {"b": 0.10}})["flags"]))
    expect("caveat removed -> flagged",
           any(f["kind"] == "caveat-removed" for f in diff(same, {**same, "caveats": []})["flags"]))
    expect("sample dropped -> flagged",
           any(f["kind"] == "sample-dropped" for f in diff(same, {**same, "samples": []})["flags"]))
    expect("adding a caveat is NOT flagged",
           diff(same, {**same, "caveats": ["endogeneity caveat", "new caveat"]})["net_removal"] is False)
    expect("N increased is NOT flagged",
           diff(same, {**same, "N": 1500})["net_removal"] is False)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic result-suppression detector (Act II).")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("diff", help="flag net removals/attenuations between two snapshots")
    d.add_argument("--before", required=True)
    d.add_argument("--after", required=True)
    d.add_argument("--attenuation-rel", type=float, default=0.05,
                   help="relative magnitude drop that counts as attenuation (default 0.05)")
    d.set_defaults(func=cmd_diff)

    s = sub.add_parser("selftest", help="run built-in tests")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
