from cubes.tutorial.sql import create_table_from_csv
from sqlalchemy import create_engine
import sys

# Setting encoding to UTF-8
reload(sys)
sys.setdefaultencoding('utf8')

# FACT table name
FACT_TABLE = "restaurant_details"
print("preparing data...")
engine = create_engine('sqlite:///restaurant.sqlite')

# Creating fact table from restaurant_details.csv
create_table_from_csv(engine,
                      "./restaurant_details.csv",
                      table_name=FACT_TABLE,
                      fields=[
                          ("id", "integer"),
                          ("number_of_reviews", "integer"),
                          ("price_range", "float"),
                          ("rating", "float"),
                          ("name", "string"),
                          ("street_city", "string"),
                          ("state", "string"),
                          ("zipcode", "integer")]
                      )

print("restaurant.sqlite created")
