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

print("Total number of reviews: %8d" % result.summary["total_number_of_reviews"])
print("Price Average : %8d" % result.summary["price_average"])
print("Rating Value average : %8d" % result.summary["rating_average"])

# Drilling down by Location
print("\n"
      "Drill Down by Location\n"
      "======================")


result = browser.aggregate(drilldown=["location:state"])

result = browser.aggregate(drilldown=["location:state"])

for row in result.table_rows("location"):
    print("%-70s%4d%8d%8d" % (row.label,
			   row.record["total_number_of_reviews"],
                           row.record["price_average"],
			   row.record["rating_average"])

	 )




print("\n"
      "Slice where Location = CA\n"
      "==================================================")

cut = PointCut("location", ["CA"])
cell = Cell(browser.cube,[cut])
result = browser.aggregate(cell,drilldown=["location.state"])

print(("%-20s%4s%4s%4s\n" + "-" * 84) % ("State","Number_of_reviews", "Price", "Rating"))

for row in result:
    print ( "%-20s%4d%4d%4d" % (row["location.state"], row["total_number_of_reviews"],row["price_average"],row["rating_average"]) )







