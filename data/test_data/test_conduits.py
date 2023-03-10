import pandas as pd
import numpy as np
import swmmio as sw
import pytest

from pipes.valid_round import validate_filling
from inp_manager.test_inp import TEST_FILE, RPT_TEST_FILE
from data.data import ConduitsData


desired_width = 500
pd.set_option("display.width", desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option("display.max_columns", 30)


@pytest.fixture(scope="module")
def model():
    yield sw.Model(TEST_FILE, include_rpt=True)


@pytest.fixture(scope="class")
def conduits_data(model):
    yield ConduitsData(model)


class TestConduitsData:

    def test_init(self, conduits_data):
        assert isinstance(conduits_data.conduits, pd.DataFrame)

    def test_drop_unused(self, conduits_data):
        assert "InletNode" in conduits_data.conduits.columns
        assert "OutletNode" in conduits_data.conduits.columns
        assert "coords" in conduits_data.conduits.columns
        assert "Geom2" in conduits_data.conduits.columns
        assert "Geom3" in conduits_data.conduits.columns
        assert "Geom4" in conduits_data.conduits.columns

        conduits_data.drop_unused()

        assert "InletNode" not in conduits_data.conduits.columns
        assert "OutletNode" not in conduits_data.conduits.columns
        assert "coords" not in conduits_data.conduits.columns
        assert "Geom2" not in conduits_data.conduits.columns
        assert "Geom3" not in conduits_data.conduits.columns
        assert "Geom4" not in conduits_data.conduits.columns

    def test_calculate_conduit_filling(self, conduits_data):
        conduits_data.calculate_conduit_filling()
        assert "Filling" in conduits_data.conduits.columns
        assert all(conduits_data.conduits["Filling"] >= 0)

    def test_filling_is_valid(self, conduits_data):
        conduits_data.calculate_conduit_filling()
        conduits_data.filling_is_valid()
        assert "ValMaxFill" in conduits_data.conduits.columns
        assert all(conduits_data.conduits["ValMaxFill"].isin([0, 1]))

    def test_validate_filling(self):
        assert validate_filling(0, 1) == True
        assert validate_filling(0.5, 1) == True
        assert validate_filling(1, 1) == False
        assert validate_filling(1.1, 1) == False

    def test_velocity_is_valid_column(self, conduits_data):
        assert "ValMaxV" not in conduits_data.conduits.columns
        conduits_data.velocity_is_valid()
        assert "ValMaxV" in conduits_data.conduits.columns

    def test_velocity_is_valid(self, conduits_data):
        conduits_data.velocity_is_valid()
        expected_values = [1, 1]
        assert list(conduits_data.conduits["ValMaxV"]) == expected_values
        assert list(conduits_data.conduits["ValMinV"]) == expected_values
