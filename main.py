import os
import swmmio as sw
import pyswmm as ps
import pandas as pd
import numpy as np

desired_width = 500
pd.set_option("display.width", desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option("display.max_columns", 30)

file = 'inp_manager/test_inp/test_file.inp'

from inp_manager.test_inp import TEST_FILE, RPT_TEST_FILE


# with ps.Simulation(TEST_FILE) as sim:
#      for _ in sim:
#          pass

model = sw.Model(TEST_FILE, include_rpt=True)
