from __future__ import print_function
from cubes import Workspace, Cell, PointCut
import warnings

warnings.filterwarnings('ignore')

# 1. Creating a workspace
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///restaurant.sqlite")
workspace.import_model("model.json")

# 2. Getting a browser
browser = workspace.browser("restaurant_details")

# 3. Aggregating the results
result = browser.aggregate()

print("Total\n-------------------------------")

print("Price Range sum : %8d" % result.summary["price_range_sum"])
print("Rating Value average : %8d" % result.summary["rating_average"])

# Drilling down by Location
print("\n"
      "Drill Down by Location\n"
      "======================")

result = browser.aggregate(drilldown=["location"])
browser.aggregate()

print(("%-70s%4s%8s\n" + "-" * 84) % ("Street", "Price", "Rating"))
for row in result.table_rows("location"):
    print("%-70s%4d%8d" % (row.label,
                           row.record["price_range_sum"],
                           row.record["rating_average"])
          )

print("\n"
      "Slice where Location = WA\n"
      "==================================================")

cut = [
    PointCut("location", ["WA"]),
    PointCut("location", ["TX"])
]

cell = Cell(browser.cube, cuts=cut)
result = browser.aggregate(cell, drilldown=["location"])
print(("%-20s%10s\n" + "-" * 50) % ("State", "Zipcode"))

for row in result.table_rows("location"):
    print("%-20s%4d%8d" % (row.label,
                           row.record["price_range_sum"],
                           row.record["rating_average"]
                           ))
