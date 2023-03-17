import pandas as pd
import numpy as np
import swmmio as sw
import pyswmm

from pipes.valid_round import (validate_filling, validate_max_velocity, validate_min_velocity, validate_max_slope, validate_min_slope, max_depth_value)

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
        self.model = model
        self.conduits = model.conduits().copy()
        self.frost_zone = None

    def set_frost_zone(self, frost_zone: str) -> None:
        """
        Set the frost zone value for the ConduitsData instance.

        According to several standards (BN-83/8836-02, PN-81/B-03020, and others),
        the depth of the pipeline and tanks should be such that its cover from
        the external edge (upper edge) of the pipe (tank) to the elevation of
        the terrain is greater than the freezing depth by 20 cm (table).

        Args:
            frost_zone (str): A string representing the frost zone category, e.g., "I", "II", "III", "IV".

        """
        categories = {
            "I": 1,
            "II": 1.2,
            "III": 1.4,
            "IV": 1.6,
        }
        self.frost_zone = categories.get(frost_zone.upper(), 1.2)

    def drop_unused(self) -> None:
        """
        Drops unused columns from the conduits dataframe.
        """
        self.conduits = self.conduits.drop(columns=["coords", "Geom2", "Geom3", "Geom4"])

    def calculate_conduit_filling(self) -> None:
        """
        Calculates the conduit filling for a given SWMM model input file.
        Adding values unit is meter.
        """
        self.conduits["Filling"] = self.conduits.MaxDPerc * self.conduits.Geom1

    def filling_is_valid(self) -> None:
        """
        Check if the conduit filling is valid.
        Checks the filling of each conduit in the dataframe against its corresponding diameter.
        Adds a new column "ValMaxFill" to the dataframe indicating if the filling is valid (1) or invalid (0).
        """
        self.conduits["ValMaxFill"] = self.conduits.apply(lambda df: validate_filling(df.Filling, df.Geom1), axis=1).astype(int)

    def velocity_is_valid(self) -> None:
        """
        Validate maximum and minimum velocities in conduits.
        The results are stored as integer values (0 or 1) in two new columns:
        ValMaxV (1 if MaxV <= max_velocity_value, 0 otherwise) and
        ValMinV (1 if MaxV >= min_velocity_value, 0 otherwise).
        """
        self.conduits["ValMaxV"] = self.conduits.apply(lambda df: validate_max_velocity(df.MaxV), axis=1).astype(int)
        self.conduits["ValMinV"] = self.conduits.apply(lambda df: validate_min_velocity(df.MaxV), axis=1).astype(int)

    def slope_per_mile(self) -> None:
        """
        Calculate the slope per mile for each conduit in the network.
        """
        self.conduits["SlopePerMile"] = self.conduits.SlopeFtPerFt * 1000

    def slopes_is_valid(self) -> None:
        """
        Validates the maximum and minimum slopes of the conduits in the system by applying
        the `validate_max_slope` and `validate_min_slope` functions to the `conduits` DataFrame.

        The `ValMaxSlope` and `ValMinSlope` columns of the `conduits` DataFrame are updated
        with the validation results, with `1` indicating a valid slope and `0` indicating an invalid slope.
        """
        self.conduits["ValMaxSlope"] = self.conduits.apply(lambda df: validate_max_slope(slope=df.SlopeFtPerFt * 1000, diameter=df.Geom1), axis=1).astype(int)
        self.conduits["ValMinSlope"] = self.conduits.apply(lambda df: validate_min_slope(slope=df.SlopeFtPerFt * 1000, filling=df.Filling, diameter=df.Geom1), axis=1).astype(int)

    def max_depth(self):
        """
        Copies the 'MaxDepth' values from the model's nodes DataFrame to the 'conduits' DataFrame,
        using the 'InletNode' values to match the corresponding rows. A new 'MaxDepth' column is
        added to the 'conduits' DataFrame containing the copied values.
        """
        self.conduits['InletMaxDepth'] = self.conduits['InletNode'].map(self.model.nodes.dataframe['MaxDepth'])
        self.conduits['OutletMaxDepth'] = self.conduits['OutletNode'].map(self.model.nodes.dataframe['MaxDepth'])

    def calculate_max_depth(self):
        nan_rows = pd.isna(self.conduits.OutletMaxDepth)
        self.conduits.loc[nan_rows, 'OutletMaxDepth'] = self.conduits.loc[nan_rows, 'InletMaxDepth'] - (
                self.conduits.loc[nan_rows, 'Length'] * self.conduits.loc[nan_rows, 'SlopeFtPerFt'])

    def inlet_ground_cover(self):
        self.conduits['InletGroundCover'] = self.conduits.InletNodeInvert - self.conduits.InletMaxDepth
        self.conduits['OutletGroundCover'] = self.conduits.OutletNodeInvert - self.conduits.OutletMaxDepth

    def depth_is_valid(self):
        self.conduits["ValDepth"] = ((max_depth_value >= self.conduits.InletGroundCover) & (
                    self.conduits.InletGroundCover >= self.frost_zone) & (
                                                 max_depth_value <= self.conduits.OutletGroundCover) & (
                                                 self.conduits.OutletGroundCover >= self.frost_zone)).astype(int)

