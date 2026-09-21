#!/usr/bin/env python3
"""Verify every file declared in the release manifest; stdlib only."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root/'MANIFEST.json').read_text())
seen = set()
for entry in manifest['files']:
    name = entry['path']
    path = (root/name).resolve()
    if name in seen or not path.is_relative_to(root):
        raise ValueError('Duplicate or escaping manifest entry: '+name)
    seen.add(name)
    raw = path.read_bytes()
    if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
        raise ValueError('Release file mismatch: '+name)
print('PASS: '+str(len(seen))+' release files match their SHA-256 manifest.')
