import math
import pytest
import numpy as np
from pipes.round import (max_filling, max_velocity, min_velocity)


class TestMaxFilling:

    def test_valid_input(self):
        assert math.isclose(max_filling(0.2), 0.1654, rel_tol=1e-4)
        assert math.isclose(max_filling(1.0), 0.827, rel_tol=1e-4)
        assert math.isclose(max_filling(2.0), 1.654, rel_tol=1e-4)

    def test_max_filling_valid_values(self):
        for val, dia in zip([0.165, 0.248, 0.331, 0.414, 0.496, 0.579, 0.662, 0.744, 0.827], np.arange(0.2, 1, 0.1)):
            assert pytest.approx(val) == round(max_filling(dia), 3)

    def test_invalid_input(self):
        with pytest.raises(TypeError):
            max_filling("invalid")
        with pytest.raises(ValueError):
            max_filling(0.1)
        with pytest.raises(ValueError):
            max_filling(3.0)

    def test_max_velocity(self):
        assert max_velocity() == 3

    def test_min_velocity(self):
        assert min_velocity() == 0.7
