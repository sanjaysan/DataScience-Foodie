README

matched_data_original: take sample tuples from DataMerging/matchdata.csv

Address is present as a single string 

Created a python script to process this table and split the address fields into street,city,state,zipcode

Show sample tuples from this CSV OLAPExploration/restaurant_details.csv

We wanted to do OLAP style exploration for data analysis
Tried CUBES framework
 -- Able to create sqlite db from CSV table ( taken as fact table)
 -- Created a model.json detailing schema of dimension table and also aggregate functions on dimension attributes
 -- Created a python script to parse model.json file and was able to aggregate over entire table


However ran into issues while trying to rollup/drilldown and couldnt proceed with this framework

Hence used sqlite3 database engine to analyze the sqlite db. Wrote SQL queries for analysis purposes

Measure attributes : Sum(number_of_reviews), Average( price_range ), Average( ratingValue )


--State based analysis

1) Groupby on state

Query -

SELECT state                  AS "State",
       Sum(number_of_reviews) AS "Total Reviews",
       Avg(ratingValue)       AS "Average Rating",
       Avg(price_range)       AS "Average price"
FROM   restaurant_details
GROUP  BY state;

Rollup_on_state.png


Observed that newyork had a high average price average


2) Drill down on state new york

Query -

SELECT *
FROM   restaurant_details
WHERE  state = 'NY';

drilldown_on_State.png


Found that many price_range values were zero


NY total 106, 82 non-zero
CA total 241, 180 non-zeros
WA total 296, 229 non-zeros
TX total 279, 224 non-zeros 
 

3) Corrected groupby - groupby state only non_zero price_range values considered

Query -

SELECT state                  AS "State",
       Sum(number_of_reviews) AS "Total Reviews",
       Avg(ratingValue)       AS "Average Rating",
       Avg(price_range)       AS "Average price"
FROM   restaurant_details
WHERE  price_range <> 0
GROUP  BY state;

Corrected_Group_By.png


4) Which city in Newyork state has maximum number of reviews

We expected Newyork city to have most number of reviews. 

Surprise....

Query -

SELECT *
FROM   restaurant_details
WHERE  state = "NY"
       AND number_of_reviews
GROUP  BY city
ORDER  BY number_of_reviews DESC;

See Image highest_review_city_NY_State.jpg


--City based analysis

5) What is the highly rated restaurant in San Jose ?

Query -

SELECT NAME,
       city,
       ratingValue
FROM   restaurant_details
WHERE  city = 'San Jose'
ORDER  BY ratingValue DESC;

drilldown_sanjose_rating.png

6) What is the most expensive restaurant in Seattle ?

Query-

SELECT NAME,
       city,
       price_range
FROM   restaurant_details
WHERE  city = 'Seattle'
ORDER  BY price_range DESC;

drilldown_seattle_pricerange.png


--locatity based (zipcode) analysis

7) Highly rated restaurant restaurant in a locality

Query -

SELECT NAME,
       ratingValue
FROM   restaurant_details
WHERE  zipcode = 78701
ORDER  BY ratingValue DESC;

drilldown_austin_zipcode_rating.png
