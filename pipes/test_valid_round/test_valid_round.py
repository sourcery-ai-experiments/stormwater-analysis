import pytest
import numpy as np
from pipes import valid_round


class TestMaxFilling:

    def test_max_filling_valid_values(self):
        for val, dia in zip([0.165, 0.248, 0.331, 0.414, 0.496, 0.579, 0.662, 0.744, 0.827], np.arange(0.2, 1, 0.1)):
            assert pytest.approx(val) == round(valid_round.max_filling(dia), 3)

    def test_max_filling_min_diameter(self):
        assert valid_round.max_filling(0.2) == pytest.approx(0.1654)

    def test_max_filling_max_diameter(self):
        assert valid_round.max_filling(2.0) == pytest.approx(1.654)

    def test_max_filling_invalid_diameter(self):
        with pytest.raises(ValueError):
            valid_round.max_filling(3.0)

    def test_max_filling_invalid_values(self):
        with pytest.raises(ValueError):
            valid_round.max_filling(-2)

    def test_max_filling_invalid_types(self):
        for val in ["", "four", [], {}]:
            with pytest.raises(TypeError):
                valid_round.max_filling(val)
