from __future__ import print_function
from cubes import Workspace, Cell, PointCut

# 1. Create a workspace
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///restaurant.sqlite")
workspace.import_model("model.json")

# 2. Get a browser
browser = workspace.browser("irbd_balance")

# 3. Play with aggregates
result = browser.aggregate()

print("Total\n"
      "----------------------")

print("Record count : %8d" % result.summary["record_count"])
print("Total amount : %8d" % result.summary["amount_sum"])
print("Double amount: %8d" % result.summary["double_amount_sum"])