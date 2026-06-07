#!/usr/bin/env python3
from helpers.quote_gate import dehyphenate, check

# Test edge cases of dehyphenate function
# The function: r"(\w)-\s+(\w)" with condition:
# if (m.group(1).isdigit() and m.group(2).isdigit()) else m.group(1) + m.group(2)

test_cases = [
    ("inter- national", "international"),  # letter-letter: should join
    ("covid- 19", "covid19"),  # letter-digit: should join
    ("5- 10", "5-10"),  # digit-digit: should NOT join (numeric range)
    ("5- a", "5a"),  # digit-letter: should join
    ("a- 5", "a5"),  # letter-digit: should join
    ("x--  y", "x--  y"),  # non-matching pattern (no hyphen between)
    ("word-\nline", "word-\nline"),  # newline not space
    ("test--word", "test--word"),  # double hyphen
]

print("=== dehyphenate tests ===")
for input_text, expected in test_cases:
    result = dehyphenate(input_text)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}: dehyphenate('{input_text}') = '{result}' (expected '{expected}')")

print()
print("=== Check for substring matching with dehyphenated text ===")
# The issue: does dehyphenate allow a false positive substring match?
# Example: "international" could match if looking for "inter" from "inter- national"
src = "The corrected mean effect is close to zero. We use inter- national\nevidence."
quote = "inter"
matched, level = check(quote, src)
print(f"check('inter', 'inter- national...') = {(matched, level)}")
print("Note: 'inter' is a substring of 'international', so it matches via dehyphenation")

# More problematic: what if the dehyphenation creates an unintended match?
src2 = "value 5- 10 percent"
quote2 = "510"
matched2, level2 = check(quote2, src2)
print(f"check('510', 'value 5- 10...') = {(matched2, level2)}")
print("Expected: False (numeric range should NOT be joined)")
