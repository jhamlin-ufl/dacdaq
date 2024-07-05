"""
A quick test of reading data from a prema 6000

Note: stdout will produce a bunch of "invalid query" warnings.
That's not an issue.
"""

import pyvisa

rm = pyvisa.ResourceManager()
inst_addr = rm.list_resources()[0]
prema = rm.open_resource(inst_addr)
print(prema.query("*IDN?"))
prema.write("T1;R1;VD")  # 100 ms integration, smallest range, voltage mode
print(prema.query("P0"))
