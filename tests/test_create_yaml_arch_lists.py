#!/usr/bin/python3
import json
arch_release_candidates= [ ('dynamic-graph-v3','devel'),
                           ('sot-core-v3','devel'),
                           ('py-sot-core-v3','devel'),
                           ('sot-dynamic-pinocchio-v3','devel'),
                           ('py-sot-dynamic-pinocchio-v3','devel'),
                           ('tsid','devel'),
                           ('parametric-curves','devel'),
                           ('sot-torque-control','devel'),
                           ('sot-talos','master')
]

f=open('arch_rc.json','w')
json.dumps(arch_release_candidates)
json.dump(arch_release_candidates,f)
f.close()
