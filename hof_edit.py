import sys

import HOF

if len(sys.argv) != 2:
    raise SystemExit("Usage: python hof_edit.py MAP_PATH")
hof = HOF.HOF_Hanover()
hof.new_from_map(sys.argv[1])