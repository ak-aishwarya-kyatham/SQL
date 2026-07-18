# SQL Exercises

This repository contains Python scripts to run SQL queries against a PostgreSQL database and export the results to an Excel file.

## Prerequisites

- PostgreSQL installed and running locally on port `5432`.
- A database named `dvdrental` (the standard PostgreSQL sample database).
- Python 3.x installed.
- Required Python packages:
  - `psycopg2`
  - `pandas`
  - `openpyxl`

You can install the required Python packages using pip:
```bash
pip install psycopg2 pandas openpyxl
```

## Setup

1. Ensure your PostgreSQL server is running.
2. If you don't have the `dvdrental` database, download and restore it to your local PostgreSQL server.
3. Open `export_sql_exercises.py` and verify/update the database connection parameters (host, port, database, user, password) as needed to match your local setup.

## Usage

Run the script to execute the queries and generate the Excel report:

```bash
python export_sql_exercises.py
```

Upon successful execution, a new file named `sql_exercise_outputs.xlsx` will be created in the same directory. Each sheet in the Excel file corresponds to a different SQL query (e.g., Q1, Q2, etc.).

## Queries Included

The script runs a variety of SQL exercises, including:
- Basic `SELECT` queries with `LIMIT`.
- Creation and querying of a standard `VIEW`.
- Creation and querying of a `MATERIALIZED VIEW`.
- Creation and querying of a `TEMP TABLE`.
