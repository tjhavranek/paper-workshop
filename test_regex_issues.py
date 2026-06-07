#!/usr/bin/env python3
from helpers.provenance import _NUM_RE

# Test: can the regex be exploited or cause ReDoS?
import re

# Test edge cases with the numeric regex
test_cases = [
    "---",  # multiple signs
    "1.2.3.4",  # multiple decimals
    "1e2e3",  # multiple exponents
    "1" * 1000 + ".5",  # very long integer
    "1e999",  # huge exponent
]

for test in test_cases:
    result = _NUM_RE.findall(test)
    print(f"_NUM_RE.findall('{test[:30]}...'): {result}")

print()
print("=== Test: Sign handling ===")
# The pattern is: [-+]?\d[\d,]*...
# Note: it requires at least ONE digit right after the optional sign
# So "+" and "-" alone won't match (good!)
tests = ["+", "-", "+-123", "-+456"]
for test in tests:
    result = _NUM_RE.findall(test)
    print(f"_NUM_RE.findall('{test}'): {result}")

print()
print("=== Test: Thousands separator edge cases ===")
# The pattern has [\d,]* which means digit or comma in any order
# This could allow weird patterns like "1,2,3" or "1,,2"
invalid_thousand = ["1,2,3", "1,,2", "1,", ",1"]
for test in invalid_thousand:
    result = _NUM_RE.findall(test)
    print(f"_NUM_RE.findall('{test}'): {result}")
