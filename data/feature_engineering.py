import pyswmm as ps
from main import model
from data import ConduitsData

from inp_manager.test_inp import TEST_FILE

# with ps.Simulation(TEST_FILE) as sim:
#      for _ in sim:
#          pass


o = ConduitsData(model)
o.set_frost_zone("II")
o.drop_unused()
o.calculate_conduit_filling()
o.filling_is_valid()
o.velocity_is_valid()
o.slope_per_mile()
o.slopes_is_valid()
o.max_depth()
o.calculate_max_depth()
o.inlet_ground_cover()
o.depth_is_valid()

print(o.conduits)

# print("\n")
# print(model.nodes.dataframe)
