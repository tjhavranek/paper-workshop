#!/usr/bin/env python3
import json
import tempfile
import os

# Test 1: What if findings.json has duplicate IDs?
print("=== Test 1: Duplicate finding IDs ===")
findings_data = [
    {"id": "F1", "quote": "text1", "finding_type": "normal"},
    {"id": "F1", "quote": "text2", "finding_type": "normal"},
]
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(findings_data, f)
    temp_file = f.name

try:
    with open(temp_file) as fh:
        data = json.load(fh)
    print(f"Loaded findings: {len(data)} items")
    print("Note: JSON allows duplicate IDs; they would be processed but batch output may confuse downstream")
finally:
    os.unlink(temp_file)

print()
print("=== Test 2: Token with null values ===")
# What if a token has null/None for required fields?
from helpers.provenance import verify_token

token_with_null = {
    "value": None,
    "script": "test.py",
    "line_or_chunk": "L1",
    "run_id": "r1",
    "input_data_hash": "",
    "output_file": "out.txt",
    "output_hash": "abc123"
}

# This should fail because value is None, but let's check
result = verify_token(token_with_null)
print(f"verify_token with null value: verified={result['verified']}")
print(f"Reason: {result['reason']}")

print()
print("=== Test 3: Encoding issues with utf-8-sig BOM ===")
# Files opened with utf-8-sig should handle BOM correctly
# But what if a file is explicitly UTF-16 or has a different BOM?
test_content = "Test content"
with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig', delete=False) as f:
    f.write(test_content)
    temp_file = f.name

try:
    # Read it back
    with open(temp_file, encoding='utf-8-sig') as f:
        content = f.read()
    print(f"UTF-8-sig BOM handling: content='{content}'")
finally:
    os.unlink(temp_file)
