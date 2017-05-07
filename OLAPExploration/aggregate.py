from __future__ import print_function
from cubes import Workspace, Cell, PointCut
import warnings

warnings.filterwarnings('ignore')
count = 1

def rollup(cell, dimension):
    result = browser.aggregate(cell, drilldown=[dimension])
    for row in result.table_rows(dimension):
        print (row.label)
        print ("-" * 2)
        print ("Total Number of reviews: %d" % (row.record["total_number_of_reviews"]))
        print("Price average: %d" % float(row.record["price_average"]))
        print("Rating average: %d" % float(row.record["rating_average"]))
        print ("\n")

"""Drill-down and aggregate recursively through als levels of `dimension`.

* `cell` - cube cell to drill-down
* `dimension` - dimension to be traversed through all levels

"""
def drilldown(cell, dimension, level):
    global count

    result = browser.aggregate(cell, drilldown=[dimension])
    for row in result.table_rows(dimension):
        indent = "    " * (len(row.path) - 1)
        print(indent, row.label)
        print(indent, "-" * 3)
        print(indent, "Total Number of reviews: %d" % (row.record["total_number_of_reviews"]))
        print(indent, "Price average: %d" % float(row.record["price_average"]))
        print(indent, "Rating average: %d" % float(row.record["rating_average"]))
        print("\n")


        count += 1
        if (count >= level):
            count = 1
            break
        new_cell = cell.drilldown(dimension, row.key)
        drilldown(new_cell, dimension, level)


# 1. Creating a workspace
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///restaurant.sqlite")
workspace.import_model("model.json")

# 2. Getting a browser
cube = workspace.cube("restaurant_details")
browser = workspace.browser(cube)

dimension = cube.dimension("location")

# Rolling up by Location
print("\n"
      "Roll up to state\n"
      "======================")

cell = Cell(browser.cube)
rollup(cell, "location")

# Drilling down by location
print("\n"
      "Drill down by state\n"
      "======================")
drilldown(cell, "location", 3)

# Drilling down by location
print("\n"
      "Slice by State\n"
      "======================")
cell = cell.slice(PointCut("location", ["CA"]))
drilldown(cell, "location",  2)
