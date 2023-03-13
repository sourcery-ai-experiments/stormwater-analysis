import pandas as pd
import numpy as np
import swmmio as sw
import pyswmm

from pipes.valid_round import (validate_filling, validate_max_velocity, validate_min_velocity, validate_max_slope, validate_min_slope)

from inp_manager.test_inp import TEST_FILE, RPT_TEST_FILE


desired_width = 500
pd.set_option("display.width", desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option("display.max_columns", 30)


# model = sw.Model(TEST_FILE, include_rpt=True)

# with pyswmm.Simulation(model.inp.path) as sim:
#     for _ in sim:
#         pass


class ConduitsData:

    def __init__(self, model: sw.Model) -> None:
        self.conduits = model.conduits().copy()

    def drop_unused(self):
        self.conduits = self.conduits.drop(columns=["InletNode", "OutletNode", "coords", "Geom2", "Geom3", "Geom4"])

    def calculate_conduit_filling(self) -> None:
        """
        Calculates the conduit filling for a given SWMM model input file.
        Adding values unit is meter.
        """
        self.conduits["Filling"] = self.conduits.MaxDPerc * self.conduits.Geom1

    def filling_is_valid(self):
        """Checks if the conduit filling is valid."""
        self.conduits["ValMaxFill"] = self.conduits.apply(lambda df: validate_filling(float(df.Filling), float(df.Geom1)), axis=1).astype(int)

    def velocity_is_valid(self):
        self.conduits["ValMaxV"] = self.conduits.apply(lambda df: validate_max_velocity(float(df.MaxV)), axis=1).astype(int)
        self.conduits["ValMinV"] = self.conduits.apply(lambda df: validate_min_velocity(float(df.MaxV)), axis=1).astype(int)

    def slope_per_mile(self):
        self.conduits["SlopePerMile"] = self.conduits.SlopeFtPerFt * 1000

    def slopes_is_valid(self):
        self.conduits["ValMaxSlope"] = self.conduits.apply(lambda df: validate_max_slope(slope=df.SlopeFtPerFt * 1000, diameter=df.Geom1), axis=1).astype(int)
        self.conduits["ValMinSlope"] = self.conduits.apply(lambda df: validate_min_slope(slope=df.SlopeFtPerFt * 1000, filling=df.Filling, diameter=df.Geom1), axis=1).astype(int)
