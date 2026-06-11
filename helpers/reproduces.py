#!/usr/bin/env python3
"""
reproduces.py - the deterministic reproduction predicate for paper-workshop (Act II).

"Reproduces" was previously an LLM-asserted boolean. This script defines it as code, per
number:  a rerun value reproduces its baseline iff
    |rerun - baseline| <= max(tol_abs, tol_rel * max(|baseline|, |rerun|)).
It is deterministic, stdlib-only (Python 3.8+), and fails CLOSED: a baseline number that
is absent from the rerun is NOT reproduced, and the overall verdict is true only if every
baseline number reproduced and none were missing.

ARTIFACT CLASSES (defaults; override with --tol-abs/--tol-rel). Relax tolerance only for
legitimately stochastic outputs that were run WITH a fixed seed (grounding rule 13 / the
Act-II sandbox): seeds make a "stochastic" output deterministic, so prefer 'exact'.
    exact        tol_abs=1e-9  tol_rel=1e-6   exact deterministic recomputation (default)
    rounded3     tol_abs=5e-4  tol_rel=1e-6   values reported to 3 decimals
    rounded2     tol_abs=5e-3  tol_rel=1e-6   values reported to 2 decimals
    simulation   tol_abs=1e-9  tol_rel=1e-2   seeded Monte-Carlo / simulation output
    bootstrap    tol_abs=1e-9  tol_rel=5e-2   seeded bootstrap / resampling CI

INPUT (baseline.json, rerun.json): a flat object mapping a label to either a number or
{"value": number, "class": "<artifact-class>"}. A per-number "class" overrides the global
class for that number - honored from the BASELINE side (or the CLI) only, never from the
rerun under audit, and an unknown class name fails the verdict (fail closed).

USAGE
    python reproduces.py compare --baseline base.json --rerun rerun.json [--class rounded3]
    python reproduces.py compare --baseline base.json --rerun rerun.json --tol-abs 1e-6 --tol-rel 1e-4
    python reproduces.py classes        # print the class table as JSON
    python reproduces.py selftest
Exit 0 iff every baseline number reproduced (and none missing), 2 otherwise.
"""
import argparse
import json
import sys

CLASSES = {
    "exact":      {"tol_abs": 1e-9, "tol_rel": 1e-6},
    "rounded3":   {"tol_abs": 5e-4, "tol_rel": 1e-6},
    "rounded2":   {"tol_abs": 5e-3, "tol_rel": 1e-6},
    "simulation": {"tol_abs": 1e-9, "tol_rel": 1e-2},
    "bootstrap":  {"tol_abs": 1e-9, "tol_rel": 5e-2},
}


def _num(x):
    """Extract the numeric value from a bare number or a {'value': ...} object."""
    if isinstance(x, dict):
        return float(x["value"])
    return float(x)


def _cls(x):
    if isinstance(x, dict):
        return x.get("class")
    return None


def compare(baseline, rerun, tol_abs, tol_rel, default_class="exact"):
    per = []
    missing = []
    nonnumeric = []
    unknown_class = []
    all_ok = True
    for label, bval in baseline.items():
        try:
            b = _num(bval)
        except (TypeError, ValueError, KeyError):
            nonnumeric.append(label)
            continue
        # per-number class override is honored from the BASELINE side or the CLI only:
        # the rerun under audit must not choose its own leniency (a rerun stamping
        # itself 'bootstrap' would wave a real drift through). An unknown class name
        # fails the verdict rather than silently falling back.
        cls = _cls(bval)
        if cls is not None and cls not in CLASSES:
            unknown_class.append(label)
            all_ok = False
            per.append({"label": label, "baseline": b, "rerun": None,
                        "reproduced": False, "delta": None, "tol": None, "class": cls})
            continue
        ta, tr = (CLASSES[cls]["tol_abs"], CLASSES[cls]["tol_rel"]) if cls in CLASSES else (tol_abs, tol_rel)
        if label not in rerun:
            missing.append(label)
            all_ok = False
            per.append({"label": label, "baseline": b, "rerun": None,
                        "reproduced": False, "delta": None, "tol": None, "class": cls})
            continue
        try:
            r = _num(rerun[label])
        except (TypeError, ValueError, KeyError):
            nonnumeric.append(label)
            all_ok = False
            per.append({"label": label, "baseline": b, "rerun": None,
                        "reproduced": False, "delta": None, "tol": None, "class": cls})
            continue
        delta = abs(r - b)
        tol = max(ta, tr * max(abs(b), abs(r)))
        rep = delta <= tol
        all_ok = all_ok and rep
        per.append({"label": label, "baseline": b, "rerun": r, "reproduced": rep,
                    "delta": delta, "tol": tol, "class": cls})
    # FAIL CLOSED on a vacuous comparison: an empty baseline means zero numbers were
    # compared (e.g. an extractor wrote {}), so "reproduced" would be meaningless.
    vacuous = not per
    reproduced = bool(all_ok and not missing and not nonnumeric and not unknown_class
                      and not vacuous)
    return {"reproduced": reproduced, "per_value": per, "missing": missing,
            "nonnumeric": nonnumeric, "unknown_class": unknown_class,
            "no_baseline_numbers": vacuous,
            "tol_abs": tol_abs, "tol_rel": tol_rel, "default_class": default_class}


def _load(path):
    with open(path, encoding="utf-8-sig") as fh:
        return json.load(fh)


def cmd_compare(args):
    base = _load(args.baseline)
    rerun = _load(args.rerun)
    ta, tr = CLASSES[args.cls]["tol_abs"], CLASSES[args.cls]["tol_rel"]
    if args.tol_abs is not None:
        ta = args.tol_abs
    if args.tol_rel is not None:
        tr = args.tol_rel
    res = compare(base, rerun, ta, tr, default_class=args.cls)
    print(json.dumps(res, indent=2))
    return 0 if res["reproduced"] else 2


def cmd_classes(args):
    print(json.dumps(CLASSES, indent=2))
    return 0


def cmd_selftest(args):
    ok = True

    def expect(name, cond):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + name)
        ok = ok and cond

    ta, tr = CLASSES["exact"]["tol_abs"], CLASSES["exact"]["tol_rel"]
    expect("identical reproduces",
           compare({"a": 0.345, "b": 12.0}, {"a": 0.345, "b": 12.0}, ta, tr)["reproduced"] is True)
    expect("tiny drift within rel tol reproduces",
           compare({"a": 1000.0}, {"a": 1000.0005}, ta, tr)["reproduced"] is True)
    expect("real change fails",
           compare({"a": 0.345}, {"a": 0.402}, ta, tr)["reproduced"] is False)
    expect("missing rerun number fails closed",
           compare({"a": 0.345, "b": 1.0}, {"a": 0.345}, ta, tr)["reproduced"] is False)
    expect("rounded3 class tolerates 3rd-decimal noise",
           compare({"a": {"value": 0.345, "class": "rounded3"}}, {"a": 0.3452}, ta, tr)["reproduced"] is True)
    expect("exact class rejects 3rd-decimal noise",
           compare({"a": 0.345}, {"a": 0.3452}, ta, tr)["reproduced"] is False)
    expect("nonnumeric baseline fails closed",
           compare({"a": "n/a"}, {"a": "n/a"}, ta, tr)["reproduced"] is False)
    # tolerance class is honored from the baseline side only, never the rerun under audit
    expect("rerun-side class is IGNORED (no self-selected leniency)",
           compare({"a": 0.345}, {"a": {"value": 0.360, "class": "bootstrap"}}, ta, tr)["reproduced"] is False)
    expect("baseline-side class still honored",
           compare({"a": {"value": 0.345, "class": "bootstrap"}}, {"a": 0.360}, ta, tr)["reproduced"] is True)
    # unknown class names fail the verdict instead of silently falling back
    expect("unknown baseline class fails closed",
           compare({"a": {"value": 0.345, "class": "rounded33"}}, {"a": 0.345}, ta, tr)["reproduced"] is False)
    expect("empty baseline fails closed (vacuous comparison)",
           compare({}, {}, ta, tr)["reproduced"] is False)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic Act-II reproduction predicate.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compare", help="compare baseline vs rerun numbers under a tolerance")
    c.add_argument("--baseline", required=True)
    c.add_argument("--rerun", required=True)
    c.add_argument("--class", dest="cls", choices=sorted(CLASSES), default="exact")
    c.add_argument("--tol-abs", type=float, default=None)
    c.add_argument("--tol-rel", type=float, default=None)
    c.set_defaults(func=cmd_compare)

    k = sub.add_parser("classes", help="print the artifact-class tolerance table")
    k.set_defaults(func=cmd_classes)

    s = sub.add_parser("selftest", help="run built-in tests")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
