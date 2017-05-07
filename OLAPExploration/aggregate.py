from __future__ import print_function
from cubes import Workspace, Cell, PointCut
import warnings

warnings.filterwarnings('ignore')
count = 1

def rollup(cell, dimension):
    global count
    """Drill-down and aggregate recursively through als levels of `dimension`.

    This function is like recursively traversing directories on a file system
    and aggregating the file sizes, for example.

    * `cell` - cube cell to drill-down
    * `dimension` - dimension to be traversed through all levels
    """


    result = browser.aggregate(cell, drilldown=[dimension])

    # for row in cubes.drilldown_rows(cell, result, dimension):
    for row in result.table_rows(dimension):
        #indent = "    " * (len(row.path) - 1)
        print (row.label)
        print ("-" * 2)
        print ("Total Number of reviews: %d" % (row.record["total_number_of_reviews"]))
        print("Price average: %d" % float(row.record["price_average"]))
        print("Rating average: %d" % float(row.record["rating_average"]))
        print ("\n")

        # new_cell = cell.drilldown(dimension, row.key)
        # if new_cell is not None:
        #     count += 1
        #     if (count >= 2):
        #         count = 1
        #         break

        # drilldown(cell, dimension)

# 1. Creating a workspace
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///restaurant.sqlite")
workspace.import_model("model.json")

# 2. Getting a browser
browser = workspace.browser("restaurant_details")

# 3. Aggregating the results
# result = browser.aggregate()

# print("Total\n-------------------------------")
#
# print("Total number of reviews: %8d" % result.summary["total_number_of_reviews"])
# print("Price Average : %8d" % result.summary["price_average"])
# print("Rating Value average : %8d" % result.summary["rating_average"])

# Drilling down by Location
print("\n"
      "Drill Down by Location\n"
      "======================")

cell = Cell(browser.cube)
rollup(cell, "location")


# result = browser.aggregate(cell, drilldown=["location"])
#
#
# for row in result.table_rows("location"):
#     print("%-70s%4d%8d%8d" % (row.label,
# 			   row.record["total_number_of_reviews"],
#                            row.record["price_average"],
# 			   row.record["rating_average"])
# 	 )
#     new_cell = cell.drilldown("location", row.key)
#
#
#
#
# print("\n"
#       "Slice where Location = CA\n"
#       "==================================================")
#
# cut = PointCut("location", ["CA"])
# cell = Cell(browser.cube,[cut])
# result = browser.aggregate(cell,drilldown=["location.state"])
#
# print(("%-20s%4s%4s%4s\n" + "-" * 84) % ("State","Number_of_reviews", "Price", "Rating"))
#
# for row in result:
#     print ( "%-20s%4d%4d%4d" % (row["location.state"], row["total_number_of_reviews"],row["price_average"],row["rating_average"]) )
#
#
#
#



