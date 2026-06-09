#!/usr/bin/env python3
"""
provenance.py - deterministic Execution-Provenance Wall checks for paper-workshop (Act II).

Grounding rule 13: no number enters the revised paper unless it is the output of code
actually executed in this run, identified by a content hash. quote_gate.py grounds Act-I
quotes; this script grounds Act-II numbers. It recomputes content hashes and confirms a
transcribed value really appears in the named run artifact. Like the quote gate it is
deterministic, stdlib-only (Python 3.8+), and fails CLOSED: any missing field, missing
file, hash mismatch, or absent value => verified:false (never a silent pass).

USAGE
  Hash a file (sha256 of its bytes):
    python provenance.py hash --file output/table1.csv
  -> {"file": "...", "sha256": "..."}

  Verify a provenance token against the run artifacts:
    python provenance.py verify --token token.json --artifact-dir phase2/runs/E1
    echo '<token json>' | python provenance.py verify --token-stdin --artifact-dir DIR
  A token is { value, script, line_or_chunk, run_id, input_data_hash, output_file, output_hash }.
  verify confirms: all 7 token fields are present (value/script/run_id/output_file/output_hash
  non-empty; line_or_chunk/input_data_hash may be "" when there is no input data); output_file
  exists (under --artifact-dir if relative); sha256(output_file) == output_hash; the token's
  `value` appears as a STANDALONE numeric literal in output_file (0.08 must NOT match inside
  0.083); and, when --data-file is given, sha256(data_file) == input_data_hash. Exit 0 iff
  verified, 2 otherwise.

  Self-test (no external files needed):
    python provenance.py selftest
"""
import argparse
import hashlib
import json
import os
import re
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# A standalone numeric literal: optional sign, either digits with optional thousands
# commas and decimal or a leading-dot decimal, optional exponent, optional percent.
_NUM_RE = re.compile(
    r"(?<![A-Za-z0-9_.+-])[-+]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?%?"
    r"(?![A-Za-z0-9_]|\.[A-Za-z0-9_])"
)


def _canon_num(raw):
    n = (raw or "").replace(",", "").replace(" ", "").strip()
    if n.startswith("-."):
        return "-0" + n[1:]
    if n.startswith("+."):
        return "+0" + n[1:]
    if n.startswith("."):
        return "0" + n
    return n


def _num_literals(text):
    """Set of normalized numeric literals in text ('1,200' -> '1200'); bare signs dropped.
    The Unicode MINUS SIGN (U+2212), ubiquitous in PDF/LaTeX-rendered numbers, is mapped to
    ASCII '-' first so a negative value stays negative and matches a token's '-0.10'."""
    text = (text or "").replace("−", "-")
    out = set()
    for raw in _NUM_RE.findall(text):
        n = _canon_num(raw)
        if n not in ("", "+", "-"):
            out.add(n)
    return out


def _value_present(value, text):
    """The token value's numeric literal(s) must each appear as a STANDALONE numeric literal in
    the artifact — never as a substring of a longer number (so 0.08 does not match 0.083, and
    12 does not match 120). A value with no numeric literal fails closed."""
    vlits = _num_literals(value)
    if not vlits:
        return False
    tlits = _num_literals(text)
    return all(v in tlits for v in vlits)


def verify_token(token, artifact_dir=None, data_file=None):
    """Deterministic, fail-closed verification of one provenance token."""
    checks = {
        "fields_present": False,
        "output_exists": False,
        "output_hash_match": False,
        "value_present": False,
        "input_hash_match": None,  # None = not requested
    }
    reasons = []
    core = ["value", "script", "run_id", "output_file", "output_hash"]  # must be present and non-empty
    present = ["line_or_chunk", "input_data_hash"]  # must be present (may be "" when there is no input data)
    missing = [k for k in core if not token.get(k)] + [k for k in present if k not in token]
    if missing:
        return {"verified": False, "checks": checks,
                "reason": "missing required field(s): " + ", ".join(missing)}
    checks["fields_present"] = True

    out = token["output_file"]
    if artifact_dir and not os.path.isabs(out):
        out = os.path.join(artifact_dir, out)
    if not os.path.isfile(out):
        return {"verified": False, "checks": checks,
                "reason": "output_file not found: " + out}
    checks["output_exists"] = True

    actual = sha256_file(out)
    if actual.lower() != str(token["output_hash"]).lower():
        reasons.append("output_hash mismatch (token=%s actual=%s)" % (token["output_hash"], actual))
    else:
        checks["output_hash_match"] = True

    try:
        with open(out, encoding="utf-8-sig", errors="replace") as fh:
            text = fh.read()
    except Exception as e:  # pragma: no cover - unreadable artifact
        text = ""
        reasons.append("could not read artifact text: %s" % e)
    if _value_present(str(token["value"]), text):
        checks["value_present"] = True
    else:
        reasons.append("token value not found as a standalone numeric literal in output artifact")

    if data_file is not None:
        # The caller asked for an input-hash check; if it cannot run, FAIL CLOSED.
        if os.path.isfile(data_file) and token.get("input_data_hash"):
            checks["input_hash_match"] = (
                sha256_file(data_file).lower() == str(token["input_data_hash"]).lower()
            )
            if not checks["input_hash_match"]:
                reasons.append("input_data_hash mismatch")
        else:
            checks["input_hash_match"] = False
            reasons.append("data_file missing or token has no input_data_hash")

    verified = (
        checks["fields_present"]
        and checks["output_exists"]
        and checks["output_hash_match"]
        and checks["value_present"]
        and (checks["input_hash_match"] in (None, True))
    )
    return {"verified": bool(verified), "checks": checks,
            "reason": "; ".join(reasons) if reasons else "ok"}


def _load_token(args):
    if getattr(args, "token_stdin", False):
        return json.loads(sys.stdin.read())
    if args.token:
        with open(args.token, encoding="utf-8-sig") as fh:
            return json.load(fh)
    raise SystemExit("provide --token PATH or --token-stdin")


def cmd_hash(args):
    print(json.dumps({"file": args.file, "sha256": sha256_file(args.file)}))
    return 0


def cmd_verify(args):
    token = _load_token(args)
    res = verify_token(token, artifact_dir=args.artifact_dir, data_file=args.data_file)
    print(json.dumps(res, indent=2))
    return 0 if res["verified"] else 2


def cmd_selftest(args):
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as d:
        art = os.path.join(d, "table1.txt")
        with open(art, "w", encoding="utf-8") as fh:
            fh.write("Headline estimate = 0.345 (se 0.012), N = 1,200\n")
        good_hash = sha256_file(art)
        base = {"value": "0.345", "script": "01_main.R", "line_or_chunk": "L42",
                "run_id": "r1", "input_data_hash": "", "output_file": "table1.txt",
                "output_hash": good_hash}

        def expect(name, cond):
            nonlocal ok
            print(("  PASS " if cond else "  FAIL ") + name)
            ok = ok and cond

        expect("valid token verifies", verify_token(dict(base), d)["verified"] is True)
        bad = dict(base); bad["output_hash"] = "deadbeef"
        expect("tampered hash fails", verify_token(bad, d)["verified"] is False)
        absent = dict(base); absent["value"] = "9.999"
        expect("absent value fails", verify_token(absent, d)["verified"] is False)
        nofile = dict(base); nofile["output_file"] = "nope.txt"
        expect("missing artifact fails", verify_token(nofile, d)["verified"] is False)
        incomplete = dict(base); incomplete.pop("output_hash")
        expect("missing field fails closed", verify_token(incomplete, d)["verified"] is False)
        # input-hash check requested but unavailable => fail closed
        expect("requested input-hash w/o data fails closed",
               verify_token(dict(base), d, data_file=os.path.join(d, "missing.csv"))["verified"] is False)
        # hash subcommand stable
        expect("sha256 is 64 hex chars", bool(re.fullmatch(r"[0-9a-f]{64}", good_hash)))
        # all 7 fields required to be present (line_or_chunk/input_data_hash may be empty)
        no_loc = {k: v for k, v in base.items() if k != "line_or_chunk"}
        expect("missing line_or_chunk fails closed", verify_token(no_loc, d)["verified"] is False)
        # substring fail-open guard: 0.08 must NOT match inside 0.083, 12 must NOT match 120
        art2 = os.path.join(d, "t2.txt")
        with open(art2, "w", encoding="utf-8") as fh:
            fh.write("coef = 0.083, N = 120, model_12 = on, file2.txt\n")
        h2 = sha256_file(art2)
        sub = dict(base); sub.update(output_file="t2.txt", output_hash=h2, value="0.08")
        expect("substring number does NOT verify (0.08 vs 0.083)", verify_token(sub, d)["verified"] is False)
        sub2 = dict(sub); sub2["value"] = "0.083"
        expect("standalone literal verifies (0.083)", verify_token(sub2, d)["verified"] is True)
        sub3 = dict(sub); sub3["value"] = "12"
        expect("substring number does NOT verify (12 vs 120)", verify_token(sub3, d)["verified"] is False)
        ident = dict(sub); ident["value"] = "2"
        expect("identifier digit does NOT verify (file2.txt)", verify_token(ident, d)["verified"] is False)
        ident2 = dict(sub); ident2["value"] = "12"
        expect("identifier suffix does NOT verify (model_12)", verify_token(ident2, d)["verified"] is False)
        # Unicode minus (U+2212) in the artifact matches an ASCII-minus token value
        art3 = os.path.join(d, "t3.txt")
        with open(art3, "w", encoding="utf-8") as fh:
            fh.write("beta_x = −0.10\n")
        h3 = sha256_file(art3)
        um = dict(base); um.update(output_file="t3.txt", output_hash=h3, value="-0.10")
        expect("unicode-minus artifact matches ascii-minus token", verify_token(um, d)["verified"] is True)
        art4 = os.path.join(d, "t4.txt")
        with open(art4, "w", encoding="utf-8") as fh:
            fh.write("p = .05, beta = -.05, se = +.05\n")
        h4 = sha256_file(art4)
        lead = dict(base); lead.update(output_file="t4.txt", output_hash=h4, value=".05")
        lead_neg = dict(base); lead_neg.update(output_file="t4.txt", output_hash=h4, value="-.05")
        lead_pos = dict(base); lead_pos.update(output_file="t4.txt", output_hash=h4, value="+.05")
        false_int = dict(base); false_int.update(output_file="t4.txt", output_hash=h4, value="05")
        expect("leading-dot decimal verifies (.05)", verify_token(lead, d)["verified"] is True)
        expect("signed leading-dot decimal verifies (-.05)", verify_token(lead_neg, d)["verified"] is True)
        expect("plus leading-dot decimal verifies (+.05)", verify_token(lead_pos, d)["verified"] is True)
        expect("leading-dot decimal does NOT verify as integer 05", verify_token(false_int, d)["verified"] is False)
        art5 = os.path.join(d, "t5.txt")
        with open(art5, "w", encoding="utf-8") as fh:
            fh.write("p = .05\n")
        h5 = sha256_file(art5)
        wrong_sign = dict(base); wrong_sign.update(output_file="t5.txt", output_hash=h5, value="-.05")
        expect("leading-dot sign is preserved", verify_token(wrong_sign, d)["verified"] is False)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic Execution-Provenance Wall checks.")
    sub = p.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("hash", help="sha256 of a file")
    h.add_argument("--file", required=True)
    h.set_defaults(func=cmd_hash)

    v = sub.add_parser("verify", help="verify a provenance token")
    v.add_argument("--token")
    v.add_argument("--token-stdin", action="store_true")
    v.add_argument("--artifact-dir", default=None)
    v.add_argument("--data-file", default=None)
    v.set_defaults(func=cmd_verify)

    s = sub.add_parser("selftest", help="run built-in tests")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
