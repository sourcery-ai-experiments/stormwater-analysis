import pyswmm as ps
from main import model
from data import ConduitsData

from inp_manager.test_inp import TEST_FILE

# with ps.Simulation(TEST_FILE) as sim:
#      for _ in sim:
#          pass


if __name__ == "__main__":
    conduits_data = ConduitsData(model)
    conduits_data.set_frost_zone("II")\
        .drop_unused() \
        .calculate_conduit_filling() \
        .filling_is_valid() \
        .velocity_is_valid() \
        .slope_per_mile() \
        .slopes_is_valid() \
        .max_depth() \
        .calculate_max_depth() \
        .inlet_ground_cover() \
        .depth_is_valid() \
        .coverage_is_valid()

    print(conduits_data.conduits)
