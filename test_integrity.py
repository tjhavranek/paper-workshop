#!/usr/bin/env python3
from helpers.integrity_diff import diff

# Test: what if coefficients dict contains non-numeric values?
print("=== Test: Non-numeric coefficient values ===")
before = {"coefficients": {"beta": 0.34, "gamma": "not a number"}}
after = {"coefficients": {"beta": 0.34, "gamma": "n/a"}}
result = diff(before, after)
print(f"Result: {result}")
print()

# Test: what if N is not an integer?
print("=== Test: N with float/string ===")
before2 = {"N": 1200.5}
after2 = {"N": 1000.5}
result2 = diff(before2, after2)
print(f"Narrowed float N: {any(f['kind'] == 'sample-narrowed' for f in result2['flags'])}")
print()

# Test: attenuation_rel edge case - what if it's negative?
print("=== Test: Negative attenuation threshold ===")
before3 = {"coefficients": {"b": 0.34}}
after3 = {"coefficients": {"b": 0.40}}
result3 = diff(before3, after3, attenuation_rel=-0.05)  # negative threshold
print(f"With attenuation_rel=-0.05, coefficient increased from 0.34 to 0.40:")
print(f"  Flags: {result3['flags']}")
print()

# Test: what if before value is 0?
print("=== Test: Coefficient was 0, now 0.1 ===")
before4 = {"coefficients": {"b": 0.0}}
after4 = {"coefficients": {"b": 0.1}}
result4 = diff(before4, after4)
print(f"Result: {result4['flags']}")
print("Expected: no 'attenuated' flag (increased from 0)")
