#!/usr/bin/env python3
from helpers.reproduces import compare, CLASSES

# Test: what if there's a per-number class override but that class is not in CLASSES dict?
# Looking at line 71: if cls in CLASSES else (tol_abs, tol_rel)

baseline = {
    "a": {"value": 0.345, "class": "nonexistent_class"}
}
rerun = {
    "a": 0.345
}

ta, tr = CLASSES["exact"]["tol_abs"], CLASSES["exact"]["tol_rel"]
result = compare(baseline, rerun, ta, tr)
print("Test: per-number class with nonexistent class name")
print(f"Result: {result['per_value'][0]}")
print("Expected: should fail or handle gracefully")
print()

# Test: edge case with very large/small numbers and tolerance
baseline2 = {"a": 1e-308}  # near float min
rerun2 = {"a": 1e-308 + 1e-315}  # tiny perturbation
result2 = compare(baseline2, rerun2, 1e-9, 1e-6)
print("Test: very small number with floating point precision")
print(f"Result reproduced: {result2['reproduced']}")
print(f"Per-value: {result2['per_value'][0]}")
print()

# Test: edge case with infinity/NaN
try:
    baseline3 = {"a": float('inf')}
    rerun3 = {"a": float('inf')}
    result3 = compare(baseline3, rerun3, 1e-9, 1e-6)
    print("Test: infinity handling")
    print(f"Result: {result3['per_value'][0]}")
except Exception as e:
    print(f"Exception with infinity: {e}")
