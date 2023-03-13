import pytest
import numpy as np

from pipes.valid_round import (validate_filling, validate_max_velocity, validate_min_velocity,
                               validate_max_slope, validate_min_slope)


class TestMaxFilling:

    def test_max_filling_valid_values(self):
        for fill, dia in zip(
            [0.16, 0.20, 0.30, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80],
            np.arange(0.2, 1.1, 0.1),
        ):
            assert validate_filling(fill, dia)

    def test_max_filling_invalid_values(self):
        for fill, dia in zip(
            [0.19, 0.26, 0.35, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90],
            np.arange(0.2, 1.1, 0.1),
        ):
            assert not validate_filling(fill, dia)

    def test_max_filling_zero(self):
        for dia in np.arange(0.2, 1.1, 0.1):
            assert validate_filling(0, dia)

    def test_max_filling_invalid_diameter(self):
        with pytest.raises(ValueError):
            validate_filling(2, 3.0)

    def test_max_filling_invalid_value(self):
        with pytest.raises(ValueError):
            validate_filling(1, -2)
        with pytest.raises(ValueError):
            validate_filling(-1, 1)

    def test_max_filling_invalid_types(self):
        for val in ["", "four", [], {}]:
            with pytest.raises(TypeError):
                validate_filling(val, 1)  # type: ignore


class TestValidateMinSlope:

    @pytest.mark.parametrize(
        ("slope", "filling", "diameter"),
        [
            (5.0, 0.10, 0.2),
            (2.5, 0.20, 0.3),
            (2.5, 0.30, 0.4),
            (2.5, 0.40, 0.5),
            (2.5, 0.45, 0.6),
            (2.5, 0.50, 0.7),
            (2.5, 0.60, 0.8),
            (2.5, 0.70, 0.9),
            (2.5, 0.80, 1.0),
        ],
    )
    def test_valid_slope(self, slope, filling, diameter):
        """
        Test the `validate_min_slope` function with valid input.
        """
        assert validate_min_slope(slope, filling, diameter)

    @pytest.mark.parametrize(
        ("slope", "filling", "diameter"),
        [
            (-5.0, 0.10, 0.2),
            (-2.5, 0.20, 0.3),
            (-2.5, 0.30, 0.4),
            (-2.5, 0.40, 0.5),
            (-2.5, 0.45, 0.6),
            (-2.5, 0.50, 0.7),
            (-2.5, 0.60, 0.8),
            (-2.5, 0.70, 0.9),
            (-2.5, 0.80, 1.0),
        ],
    )
    def test_valid_negative_slope(self, slope, filling, diameter):
        """
        Test the `validate_min_slope` function with negative slope.
        """
        assert not validate_min_slope(slope, filling, diameter)

    def test_invalid_slope(self):
        assert not validate_min_slope(0.5, 0.3, 0.5, 1.5, 9.81)

    def test_valid_slope_with_different_theta(self):
        assert validate_min_slope(2.5, 0.2, 0.3, 1.0, 9.81)

    def test_valid_slope_with_different_diameter(self):
        assert validate_min_slope(1.2, 0.5, 0.6, 1.5, 9.81)

    def test_valid_slope_with_different_gravity(self):
        assert validate_min_slope(1.2, 0.5, 0.7, 1.5, 10)

    def test_invalid_slope_with_different_gravity(self):
        assert validate_min_slope(1.0, 0.5, 0.7, 1.5, 8.81)

    def test_invalid_slope_with_negative_filling(self):
        with pytest.raises(ValueError):
            validate_min_slope(0.5, -0.5, 0.3, 1.5, 9.81)

    def test_invalid_slope_with_negative_diameter(self):
        with pytest.raises(ValueError):
            validate_min_slope(0.5, 0.5, -0.3, 1.5, 9.81)
