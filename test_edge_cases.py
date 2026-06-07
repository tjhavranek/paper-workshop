#!/usr/bin/env python3
from helpers.provenance import _num_literals, _value_present
from helpers.consistency import value_literals, numbers_in

# PROBLEMATIC CASE: space in token value
# If token value='1 200' (space-separated), and artifact has '1' and '200' separately,
# should this match? The regex treats spaces as separators.
print("=== TEST: Space in token value ===")
result = _value_present('1 200', 'The values are 1 and 200 separately')
print(f'value_present("1 200", "...1 and 200 separately"): {result}')
print('Expected: False (these arent the same number)')
print()

# Same test with consistency module
print("=== TEST: consistency.value_literals with space ===")
lits = value_literals('1 200')
print(f'value_literals("1 200"): {lits}')
rev_set, _ = numbers_in('The values are 1 and 200 separately')
print(f'numbers_in text: {rev_set}')
all_present = all(l in rev_set for l in lits)
print(f'All literals present? {all_present}')
print('Expected: False (these shouldnt be treated as components of a single value)')
print()

# Test: what if the regex finds numbers with internal spaces?
print("=== TEST: Regex pattern with spaces ===")
import re
_NUM_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?(?:[eE][-+]?\d+)?%?")
text = "1 200 with spaces"
found = _NUM_RE.findall(text)
print(f'_NUM_RE.findall("1 200 with spaces"): {found}')
print('The regex correctly finds 1 and 200 separately, NOT as a combined "1 200"')
