#!/usr/bin/env python3
import os
import sys

# Test: os.path.isabs() behavior on Windows with forward slashes
print(f"Platform: {sys.platform}")
print()

# In provenance.py line 99-100:
# if artifact_dir and not os.path.isabs(out):
#     out = os.path.join(artifact_dir, out)

# What happens if 'out' (output_file) is a relative path with forward slashes on Windows?
test_path = "results/table1.csv"
test_artifact_dir = "C:\\Users\\test\\data"

print(f"os.path.isabs('{test_path}'): {os.path.isabs(test_path)}")
print(f"os.path.join('{test_artifact_dir}', '{test_path}'): {os.path.join(test_artifact_dir, test_path)}")
print()

# What about mixed slashes?
mixed_path = "results\\table1.csv"
print(f"os.path.isabs('{mixed_path}'): {os.path.isabs(mixed_path)}")
print()

# The bigger question: what if output_file contains ./ or ../ ?
# Is there a path traversal risk?
traversal = "../../../etc/passwd"
artifact_dir = "/safe/artifacts"
result = os.path.join(artifact_dir, traversal)
print(f"Path traversal test:")
print(f"  os.path.join('{artifact_dir}', '{traversal}') = {result}")
print(f"  Normalized: {os.path.normpath(result)}")
print()

# On Windows, what if someone uses \\ in the JSON?
win_path = "..\\..\\..\\windows\\system32\\config\\sam"
result2 = os.path.join("C:\\artifacts", win_path)
print(f"Windows traversal test:")
print(f"  os.path.join('C:\\artifacts', '{win_path}') = {result2}")
print(f"  Normalized: {os.path.normpath(result2)}")
