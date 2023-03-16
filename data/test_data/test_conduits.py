import pandas as pd
import numpy as np
import swmmio as sw
import pytest

from unittest.mock import MagicMock
from pipes.valid_round import validate_filling
from inp_manager.test_inp import TEST_FILE
from data.data import ConduitsData


desired_width = 500
pd.set_option("display.width", desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option("display.max_columns", 30)


@pytest.fixture(scope="module")
def model():
    """
    A pytest fixture that creates and provides a SWMM Model object using the TEST_FILE.

    The fixture has a module scope, meaning it will be executed only once per module,
    and the same SWMM Model object will be used across all tests within the module.

    Yields:
        sw.Model: The SWMM Model object created from the TEST_FILE.
    """
    yield sw.Model(TEST_FILE, include_rpt=True)


@pytest.fixture(scope="class")
def conduits_data(model):
    """
    A pytest fixture that creates and provides a ConduitsData object using the provided SWMM Model object.

    The fixture has a class scope, meaning it will be executed only once per class,
    and the same ConduitsData object will be used across all tests within the class.

    Args:
        model (sw.Model): The SWMM Model object created by the model fixture.

    Yields:
        ConduitsData: The ConduitsData object created using the provided SWMM Model object.
    """
    yield ConduitsData(model)


class TestConduitsData:
    """
    A test class for the ConduitsData class, containing various test cases to ensure the correct
    functionality of the methods in ConduitsData.
    """

    def test_init(self, conduits_data):
        """
        Test the initialization of the ConduitsData object and ensure that the 'conduits' attribute
        is a pandas DataFrame.
        """
        assert isinstance(conduits_data.conduits, pd.DataFrame)

    def test_drop_unused(self, conduits_data):
        """
        Test the 'drop_unused' method of the ConduitsData class to ensure that it correctly removes
        the specified columns from the 'conduits' DataFrame.
        """
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
        """
        Test the 'calculate_conduit_filling' method of the ConduitsData class to ensure that it
        correctly calculates and adds the 'Filling' column to the 'conduits' DataFrame.
        """
        conduits_data.calculate_conduit_filling()
        assert "Filling" in conduits_data.conduits.columns
        assert all(conduits_data.conduits["Filling"] >= 0)

    def test_filling_is_valid(self, conduits_data):
        """
        Test the 'filling_is_valid' method of the ConduitsData class to ensure that it correctly
        validates the conduit filling and adds the 'ValMaxFill' column to the 'conduits' DataFrame.
        """
        conduits_data.calculate_conduit_filling()
        conduits_data.filling_is_valid()
        assert "ValMaxFill" in conduits_data.conduits.columns
        assert all(conduits_data.conduits["ValMaxFill"].isin([0, 1]))

    def test_validate_filling(self):
        """
        Test the 'validate_filling' function to ensure it correctly validates the filling value based
        on the provided diameter.
        """
        assert validate_filling(0, 1)
        assert validate_filling(0.5, 1)
        assert not validate_filling(1, 1)
        assert not validate_filling(1.1, 1)

    def test_velocity_is_valid_column(self, conduits_data):
        """
        Test the 'velocity_is_valid' method of the ConduitsData class to ensure that it correctly
        adds the 'ValMaxV' column to the 'conduits' DataFrame.
        """
        assert "ValMaxV" not in conduits_data.conduits.columns
        conduits_data.velocity_is_valid()
        assert "ValMaxV" in conduits_data.conduits.columns

    def test_velocity_is_valid(self, conduits_data):
        """
        Test the 'velocity_is_valid' method of the ConduitsData class to ensure that it correctly
        validates the conduit velocities and updates the 'ValMaxV' and 'ValMinV' columns in the
        'conduits' DataFrame.
        """
        conduits_data.velocity_is_valid()
        expected_values = [1, 1]
        assert list(conduits_data.conduits["ValMaxV"]) == expected_values
        assert list(conduits_data.conduits["ValMinV"]) == expected_values

    def test_slope_per_mile_column_added(self, conduits_data):
        """
        Test if the 'SlopePerMile' column is added to the conduits dataframe after calling the slope_per_mile() method.
        """
        conduits_data.slope_per_mile()
        assert 'SlopePerMile' in conduits_data.conduits.columns

    def test_slope_per_mile_calculation(self, conduits_data):
        """
        Test if the calculated values in the 'SlopePerMile' column are correct after calling the slope_per_mile() method.
        """
        conduits_data.slope_per_mile()
        expected_values = [1.80,  6.40]  # SlopeFtPerFt * 1000
        assert list(conduits_data.conduits['SlopePerMile']) == pytest.approx(expected_values, abs=1e-9)

    def test_slopes_is_valid_columns_added(self, conduits_data):
        """
        Test if the 'ValMaxSlope' and 'ValMinSlope' columns are added to the conduits dataframe after calling slopes_is_valid() method.
        """
        conduits_data.calculate_conduit_filling()
        conduits_data.slopes_is_valid()
        assert 'ValMaxSlope' in conduits_data.conduits.columns
        assert 'ValMinSlope' in conduits_data.conduits.columns

    def test_slopes_is_valid_max_slope(self, conduits_data):
        """
        Test if the maximum slope validation is correct after calling the slopes_is_valid() method.
        """
        conduits_data.calculate_conduit_filling()
        conduits_data.slopes_is_valid()
        expected_values = [1, 1]  # Assuming both conduits have valid maximum slopes
        assert list(conduits_data.conduits['ValMaxSlope']) == expected_values

    def test_slopes_is_valid_min_slope(self, conduits_data):
        """
        Test if the minimum slope validation is correct after calling the slopes_is_valid() method.
        """
        conduits_data.calculate_conduit_filling()
        conduits_data.slopes_is_valid()
        expected_values = [1, 1]  # Assuming both conduits have valid minimum slopes
        assert list(conduits_data.conduits['ValMinSlope']) == expected_values

    def test_max_depth_columns_added(self, conduits_data):
        """
        Test if the 'InletMaxDepth' and 'OutletMaxDepth' columns are added to the conduits DataFrame after
        calling the `max_depth()` method.
        """
        conduits_data.max_depth()
        assert 'InletMaxDepth' in conduits_data.conduits.columns
        assert 'OutletMaxDepth' in conduits_data.conduits.columns

    def test_max_depth_inlet_values_match(self, conduits_data, model):
        """
        Test if the 'InletMaxDepth' values in the conduits DataFrame match the corresponding 'MaxDepth' values
        in the nodes DataFrame, using the 'InletNode' as a reference.
        """
        conduits_data.max_depth()
        nodes_data = model.nodes.dataframe
        for _, conduit in conduits_data.conduits.iterrows():
            inlet_node = conduit['InletNode']
            node_max_depth = nodes_data.loc[inlet_node, 'MaxDepth']
            conduit_inlet_max_depth = conduit['InletMaxDepth']
            assert conduit_inlet_max_depth == node_max_depth

    def test_max_depth_outlet_values_match(self, conduits_data, model):
        """
        Test if the 'OutletMaxDepth' values in the conduits DataFrame match the corresponding 'MaxDepth' values
        in the nodes DataFrame, using the 'OutletNode' as a reference.
        """
        conduits_data.max_depth()
        nodes_data = model.nodes.dataframe
        for _, conduit in conduits_data.conduits.iterrows():
            outlet_node = conduit['OutletNode']
            node_max_depth = nodes_data.loc[outlet_node, 'MaxDepth']
            conduit_outlet_max_depth = conduit['OutletMaxDepth']
            assert conduit_outlet_max_depth == node_max_depth

    def test_set_frost_zone_valid_categories(self, conduits_data):
        """
        Test the set_frost_zone method with valid frost zone categories.
        """
        valid_categories = ["I", "II", "III", "IV"]

        expected_values = [1, 1.2, 1.4, 1.6]

        for category, expected_value in zip(valid_categories, expected_values):
            conduits_data.set_frost_zone(category)
            assert conduits_data.frost_zone == pytest.approx(expected_value, abs=1e-9)

    def test_set_frost_zone_invalid_category(self, conduits_data):
        """
        Test the set_frost_zone method with an invalid frost zone category.
        """
        invalid_category = "INVALID"

        default_value = 1.2

        conduits_data.set_frost_zone(invalid_category)
        assert conduits_data.frost_zone == pytest.approx(default_value, abs=1e-9)

    def test_set_frost_zone_case_insensitivity(self, conduits_data):
        """
        Test the set_frost_zone method with mixed case frost zone categories.
        """
        mixed_case_categories = ["i", "Ii", "iii", "iV"]

        expected_values = [1, 1.2, 1.4, 1.6]

        for category, expected_value in zip(mixed_case_categories, expected_values):
            conduits_data.set_frost_zone(category)
            assert conduits_data.frost_zone == pytest.approx(expected_value, abs=1e-9)
