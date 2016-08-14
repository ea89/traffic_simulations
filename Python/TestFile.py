import os
import sys
import optparse
import subprocess
import random
import heapq

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    os.environ["SUMO_HOME"] = "C:\sumo-win32-0.24.0\sumo-0.24.0"
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory"
        " of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci

def get_options(self):
    """
    This method allows the class to get the options invoked by the command line.
    :param self: The class invoking the method
    :return: A Values object to indicate the options passed in to the system.
    """
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == '__main__':
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    NETCONVERT = checkBinary("netconvert")
    PREFIX = "cross"
    os.system("%s --no-internal-links -n %s.nod.xml -e %s.edg.xml -x %s.con.xml -o %s.net.xml" %
              (NETCONVERT, PREFIX, PREFIX, PREFIX, PREFIX))