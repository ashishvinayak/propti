import sys
import os
import numpy as np
import copy
import pandas as pd
import shutil as sh
import pickle

import propti as pr

import logging

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("root_dir", type=str,
                    help="optimisation root directory")
cmdl_args = parser.parse_args()

setups = None  # type: pr.SimulationSetupSet
ops = None  # type: pr.ParameterSet
optimiser = None  # type: pr.OptimiserProperties

in_file = open('propti.pickle.init', 'rb')
ver, setups, ops, optimiser = pickle.load(in_file)
in_file.close()

# check if propti version is same as in pickle file
# else upgrade files to new values using defaults.
dict_of_upgrades = {}
if ver.ver_propti != pr.Version().ver_propti:
    temp = setups.upgrade()
    dict_of_upgrades["setups"] = temp
    temp = ops.upgrade()
    dict_of_upgrades["ops"] = temp
    temp = optimiser.upgrade()
    dict_of_upgrades["optimiser"] = temp
    ver = pr.Version()
    logging.warning("Pickle init file is old. Upgrading...")
    logging.warning("Optimization run with defaults for missing parameters.")
    logging.warning("Following data was upgraded: " + str(dict_of_upgrades))  # TODO: pPRINT?
    # Create new pickle file
    out_file = open('new_propti.pickle.init', 'wb')
    pickle.dump((ver, setups, ops, optimiser), out_file)
    out_file.close()

if ver.flag_propti != 0:
    logging.warning("No git. Propti version is represented as a hash.")
if ops is None:
    logging.critical("optimisation parameter are not defined")
if setups is None:
    logging.critical("simulation setups are not defined")
if optimiser is None:
    logging.critical("optimiser properties are not defined")

print(ver, setups, ops, optimiser)

res = pr.run_optimisation(ops, setups, optimiser)

print(ops)

out_file = open('propti.pickle.finished', 'wb')
pickle.dump((ver, setups, ops, optimiser), out_file)
out_file.close()
