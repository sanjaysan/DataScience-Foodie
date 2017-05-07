-- 1) Groupby on state
SELECT state                  AS "State",
       Sum(number_of_reviews) AS "Total Reviews",
       Avg(ratingValue)       AS "Average Rating",
       Avg(price_range)       AS "Average price"
FROM   restaurant_details
GROUP  BY state;

-- 2) Drill down on state New York

SELECT *
FROM   restaurant_details
WHERE  state = 'NY';

-- 3) Corrected groupby - groupby state only non_zero price_range values considered

SELECT state                  AS "State",
       Sum(number_of_reviews) AS "Total Reviews",
       Avg(ratingValue)       AS "Average Rating",
       Avg(price_range)       AS "Average price"
FROM   restaurant_details
WHERE  price_range <> 0
GROUP  BY state;


-- 4) Which city in New York state has maximum number of reviews

SELECT *
FROM   restaurant_details
WHERE  state = "NY"
       AND number_of_reviews
GROUP  BY city
ORDER  BY number_of_reviews DESC;

-- 5) What is the highly rated restaurant in San Jose

SELECT NAME,
       city,
       ratingValue
FROM   restaurant_details
WHERE  city = 'San Jose'
ORDER  BY ratingValue DESC;

-- 6)  What is the most expensive restaurant in Seattle ?

SELECT NAME,
       city,
       price_range
FROM   restaurant_details
WHERE  city = 'Seattle'
ORDER  BY price_range DESC;


-- 7) Highly rated restaurant restaurant in a locality
SELECT NAME,
       ratingValue
FROM   restaurant_details
WHERE  zipcode = 78701
ORDER  BY ratingValue DESC;
