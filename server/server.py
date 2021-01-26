import sys
import os.path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import gaurabda as G
import gaurabda.TServer as GS



GS.run_server()
