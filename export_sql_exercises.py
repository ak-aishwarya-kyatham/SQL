import psycopg2
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="dvdrental",
    user="postgres",
    password="root"   # Replace with your password
)

# -----------------------------
# Queries
# Replace Q1-Q11 with your actual exercise queries
# -----------------------------
queries = {
    "Q1": """SELECT title AS "Film Title", rental_rate AS "Daily Price"
             FROM film
             ORDER BY title
             LIMIT 10;""",
             
    "Q2": """SELECT title, length
             FROM film
             WHERE length BETWEEN 60 AND 120 AND title LIKE 'A%'
             ORDER BY length ASC;""",
             
    "Q3": """SELECT rating, COUNT(*) AS film_count
             FROM film
             GROUP BY rating
             ORDER BY film_count DESC;""",
             
    "Q4": """SELECT c.name AS category, COUNT(fc.film_id) AS film_count
             FROM category c
             JOIN film_category fc ON c.category_id = fc.category_id
             GROUP BY c.name
             HAVING COUNT(fc.film_id) > 65
             ORDER BY film_count DESC;""",
             
    "Q5": """SELECT f.title, c.name AS category
             FROM film f
             JOIN film_category fc ON f.film_id = fc.film_id
             JOIN category c ON fc.category_id = c.category_id
             ORDER BY c.name, f.title;""",
             
    "Q6": """SELECT UPPER(first_name || ' ' || last_name) AS customer_name,
                    split_part(email, '@', 2) AS email_domain
             FROM customer;""",
             
    "Q7": """SELECT first_name, last_name, 'Actor' AS type FROM actor
             UNION ALL
             SELECT first_name, last_name, 'Staff' AS type FROM staff;""",
             
    "Q8": """SELECT
                 CASE
                     WHEN length < 60 THEN 'Short'
                     WHEN length BETWEEN 60 AND 120 THEN 'Medium'
                     WHEN length > 120 THEN 'Long'
                 END AS length_bucket,
                 COUNT(*) AS films
             FROM film
             GROUP BY length_bucket;""",
             
    "Q9": """WITH CustomerSpend AS (
                 SELECT c.first_name || ' ' || c.last_name AS customer_name, SUM(p.amount) AS total_spent
                 FROM customer c
                 JOIN payment p ON c.customer_id = p.customer_id
                 GROUP BY c.customer_id
             ),
             AvgSpend AS (
                 SELECT AVG(total_spent) AS avg_spend FROM CustomerSpend
             )
             SELECT customer_name, total_spent
             FROM CustomerSpend, AvgSpend
             WHERE total_spent > avg_spend
             ORDER BY total_spent DESC;""",
             
    "Q10": """SELECT title, rental_rate
              FROM film
              WHERE rental_rate > (SELECT AVG(rental_rate) FROM film)
              ORDER BY rental_rate DESC;""",
              
    "Q11": """WITH FilmRentals AS (
                  SELECT c.name AS category, f.title, COUNT(r.rental_id) AS rentals
                  FROM film f
                  JOIN film_category fc ON f.film_id = fc.film_id
                  JOIN category c ON fc.category_id = c.category_id
                  JOIN inventory i ON f.film_id = i.film_id
                  JOIN rental r ON i.inventory_id = r.inventory_id
                  GROUP BY c.name, f.title
              )
              SELECT category, title, rentals, RANK() OVER (PARTITION BY category ORDER BY rentals DESC) AS rnk
              FROM FilmRentals;""",

    # -----------------------------
    # View
    # -----------------------------
    "Q12": {
        "setup": """
DROP VIEW IF EXISTS film_catalog;

CREATE VIEW film_catalog AS
SELECT
    f.title,
    c.name AS category,
    f.rental_rate,
    f.length
FROM film f
JOIN film_category fc
ON f.film_id = fc.film_id
JOIN category c
ON fc.category_id = c.category_id;
""",

        "query": """
SELECT
    title,
    rental_rate,
    length
FROM film_catalog
WHERE category='Comedy'
ORDER BY title;
"""
    },

    # -----------------------------
    # Materialized View
    # -----------------------------
    "Q13": {
        "setup": """
DROP MATERIALIZED VIEW IF EXISTS category_revenue;

CREATE MATERIALIZED VIEW category_revenue AS
SELECT
    c.name AS category,
    SUM(p.amount) AS revenue
FROM payment p
JOIN rental r
ON p.rental_id=r.rental_id
JOIN inventory i
ON r.inventory_id=i.inventory_id
JOIN film_category fc
ON i.film_id=fc.film_id
JOIN category c
ON fc.category_id=c.category_id
GROUP BY c.name;
""",

        "query": """
SELECT
    category,
    revenue
FROM category_revenue
ORDER BY revenue DESC
LIMIT 5;

-- Command to refresh the stored numbers after new data arrives:
-- REFRESH MATERIALIZED VIEW category_revenue;
""",
    },

    # -----------------------------
    # Temporary Table
    # -----------------------------
    "Q14": {
        "setup": """
DROP TABLE IF EXISTS top_10_films;

CREATE TEMP TABLE top_10_films AS
SELECT
    f.title,
    COUNT(r.rental_id) AS rentals
FROM film f
JOIN inventory i
ON f.film_id=i.film_id
JOIN rental r
ON i.inventory_id=r.inventory_id
GROUP BY f.title
ORDER BY rentals DESC
LIMIT 10;
""",

        "query": """
SELECT
    title,
    rentals
FROM top_10_films;
"""
    }
}

# -----------------------------
# Excel Export
# -----------------------------
output_file = "sql_exercise_outputs.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    cursor = conn.cursor()

    for sheet, sql in queries.items():

        if isinstance(sql, dict):
            cursor.execute(sql["setup"])
            conn.commit()

            df = pd.read_sql_query(sql["query"], conn)

        else:
            df = pd.read_sql_query(sql, conn)

        df.to_excel(writer, sheet_name=sheet, index=False)

    cursor.close()

conn.close()

print("Excel file created successfully!")
print("File name:", output_file)