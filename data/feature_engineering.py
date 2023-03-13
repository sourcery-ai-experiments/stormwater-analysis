from main import model
from data import ConduitsData


o = ConduitsData(model)
o.drop_unused()
o.calculate_conduit_filling()
o.filling_is_valid()
o.velocity_is_valid()
o.slope_per_mile()
o.slopes_is_valid()
print(o.conduits)
