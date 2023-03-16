import pyswmm as ps
from main import model
from data import ConduitsData

from inp_manager.test_inp import TEST_FILE

# with ps.Simulation(TEST_FILE) as sim:
#      for _ in sim:
#          pass


o = ConduitsData(model)
o.drop_unused()
o.calculate_conduit_filling()
o.filling_is_valid()
o.velocity_is_valid()
o.slope_per_mile()
o.slopes_is_valid()
o.max_depth()

print(o.conduits)

print("\n")
print(model.nodes.dataframe)
