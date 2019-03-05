#!/usr/bin/python3
import json
with open('arch_rc.json') as f:
    arch_release_candidates = json.load(f)
    print(arch_release_candidates)
    f.close()
