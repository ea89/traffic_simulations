#!/usr/bin/env python
"""
@file    runner.py
@author  Lena Kalleske
@author  Daniel Krajzewicz
@author  Michael Behrisch
@author  Jakob Erdmann
@date    2009-03-26
@version $Id: runner.py 18096 2015-03-17 09:50:59Z behrisch $

Tutorial for traffic light control via the TraCI interface.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2009-2015 DLR/TS, Germany

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import os
import sys
import optparse
import subprocess
import random
from ParkingConstants import *

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
# the port used for communicating with your sumo instance
PORT = 8873


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1. / 1000
    pEW = 1. / 1100
    pNS = 1. / 3000
    with open("data/cross.rou.xml", "w") as routes:
        print >> routes, """<routes>"""

        print >> routes, "</routes>"


def run():
    """execute the TraCI control loop"""
    traci.init(PORT)
    step = 0

    num_cars = -1
    parkable_lanes = []
    parked_cars = []

    for lane_id in traci.lane.getIDList():
        if PARKING_EDGE_TWO_LABEL in lane_id:
            parkable_lanes.append(lane_id)

    while traci.simulation.getMinExpectedNumber() > 0:
        num_cars += 1
        traci.simulationStep()

        traci.vehicle.add("parking_{}".format(num_cars), "right")
        if len(parkable_lanes) >0:
            parking_target = ""
            parking_target = random.choice(parkable_lanes)
            print parking_target
            traci.vehicle.changeTarget("parking_{}".format(num_cars), "1i_parking_lane_2_2")#parking_target[:-2])
            parkable_lanes.remove(parking_target)
            parked_cars.append("parking_{}".format(num_cars))





        step += 1
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "data/cross.sumocfg", "--tripinfo-output",
                                    "tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)
    run()
    sumoProcess.wait()
