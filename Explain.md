Yes. I read the entire 61-page PDF. It is essentially a complete learning + hands-on lab guide covering Data Warehousing, Data Modeling, and Snowflake SQL. 

I’ll explain it from the basics to the final Snowflake project, in simple language, so you can actually perform the lab rather than just memorize definitions.


---

1. Big Picture — What are we learning?

The whole PDF is teaching this pipeline:

Source Data → Raw/Staging → Data Warehouse → Fact & Dimensions → Data Mart → Reports/Analytics

The final page summarizes exactly this flow: data comes from source systems, lands in staging, gets integrated into the warehouse, is modeled using facts and dimensions, and is then exposed through data marts for analytics. 

Think of a company selling products.

It has data coming from:

CRM → customer information

ERP → business/transaction information

Website

CSV files


The company wants to answer questions like:

> How much did we sell?
Which customer bought the most?
Which product category made the most money?
What were our daily sales?



A Data Warehouse is built to answer these questions.


---

2. What is a Data Warehouse?

A Data Warehouse (DWH) is a centralized place where integrated historical data is stored for:

Reporting

Analytics

Business Intelligence

Dashboards

Decision-making


This is given on pages 3–4 of the PDF. 

Simple example

Suppose a company has:

CRM
 ↓
ERP       →  DATA WAREHOUSE  →  Reports / Dashboard
 ↓
Website

The operational systems are mainly concerned with running the business.

The warehouse is mainly concerned with analyzing the business.

OLTP vs Data Warehouse

OLTP	Data Warehouse

Daily transactions	Analytics
Current data	Historical data
Many INSERT/UPDATE	Mostly SELECT
Normalized	Often denormalized
Application-focused	Business/analysis-focused


So:

OLTP = Run the business

DWH = Analyze the business


---

3. Data Warehouse Architecture

The PDF divides the architecture into 3 major layers:

SOURCE SYSTEMS
      ↓
STAGING LAYER
      ↓
INTEGRATION LAYER
      ↓
ACCESS LAYER
      ↓
REPORTS / BI

The diagram on page 5 shows this complete flow. 

Layer 1 — Staging

Staging is where incoming data is temporarily placed.

For example:

CRM
ERP
Website
 ↓
STAGING

The data here can still be raw/temporary.

Think:

> "Data has arrived, but we haven't properly prepared it yet."




---

Layer 2 — Integration

The integration layer creates a consistent enterprise view of the data. 

For example, imagine:

CRM says:

Customer ID = 1001
Name = Alice

ERP might contain:

Customer ID = C1001
Name = Alice Corp

The integration layer cleans and combines these into a consistent view.


---

Layer 3 — Access

The access layer is designed for users/consumers. 

Examples:

BI dashboards

Reports

Analytics

Data marts



---

4. EDW vs Data Mart

This is important for exams.

EDW — Enterprise Data Warehouse

An EDW covers the whole organization.

Example:

EDW
        /      |      \
     Sales   Finance   HR

It integrates data across multiple business areas. 

Data Mart

A Data Mart focuses on one particular business area.

For example:

EDW
 ↓
Sales Data Mart

The PDF compares them as:

EDW	Data Mart

Enterprise-wide	Department/business area
Larger	Smaller
Many departments	Specific department
More complex	Less complex




Easy memory

EDW = Entire company

Data Mart = Particular department


---

5. ETL vs ELT

Very important.

ETL

Extract → Transform → Load

SOURCE
  ↓
EXTRACT
  ↓
TRANSFORM
  ↓
LOAD
  ↓
WAREHOUSE

Transformation happens before loading into the warehouse. 

Example:

Raw data:

"alice corp"

Transform:

"ALICE CORP"

Then load it into the warehouse.


---

ELT

Extract → Load → Transform

SOURCE
  ↓
EXTRACT
  ↓
LOAD
  ↓
CLOUD DWH
  ↓
TRANSFORM

Transformation happens inside the warehouse.

Modern cloud warehouses make this approach attractive because warehouse computing power can perform the transformations. 

Memory trick

ETL = Transform before warehouse

ELT = Transform inside warehouse


---

6. Batch vs Real-Time

Batch Processing

Data is collected and processed periodically.

Example:

8 AM ─┐
9 AM ─┤
10 AM ┤ → BATCH → DATA WAREHOUSE
11 AM ┘

Examples:

Daily sales load

Nightly finance processing

Monthly reporting


The PDF's batch example uses CSV files such as:

sales_2025_01_01.csv
sales_2025_01_02.csv
sales_2025_01_03.csv

which can be loaded once per day. 


---

7. Snowflake Batch Loading

Now we start doing practical work.

The PDF gives this pipeline:

CSV
 ↓
STAGE
 ↓
STAGING TABLE
 ↓
DIMENSION / FACT
 ↓
ANALYTICS




---

8. Snowflake Database and Schema

First:

CREATE DATABASE SALES_DWH;

Then schemas:

CREATE SCHEMA SALES_DWH.STAGING;
CREATE SCHEMA SALES_DWH.DIMENSIONS;
CREATE SCHEMA SALES_DWH.FACTS;
CREATE SCHEMA SALES_DWH.MART;

Snowflake follows:

DATABASE
   ↓
SCHEMA
   ↓
TABLE



For example:

SALES_DWH
   |
   +-- STAGING
   +-- DIMENSIONS
   +-- FACTS
   +-- MART


---

9. File Format and Stage

For CSV:

CREATE OR REPLACE FILE FORMAT SALES_CSV_FORMAT
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1;

This tells Snowflake:

File type = CSV

Columns separated by ,

Ignore first row/header


Then create a stage:

CREATE OR REPLACE STAGE SALES_STAGE
FILE_FORMAT = SALES_CSV_FORMAT;

A stage is a location where files can be stored before loading them into tables. 

Then:

COPY INTO STG_SALES
FROM @SALES_STAGE
FILE_FORMAT = (FORMAT_NAME = SALES_CSV_FORMAT);

COPY INTO loads the staged files into a table. 


---

10. Now the Most Important Part — Data Modeling

Data modeling means deciding:

> What data should we store?
What does each row represent?
How are the tables related?



The PDF identifies these major concepts:

Grain

Fact

Dimension

Keys

Relationships

Star Schema

Snowflake Schema

SCD





---

11. Fact Table

A Fact Table stores measurable business events.

Examples:

Sales

Orders

Payments

Shipments

Website visits




Example:

FACT_SALES

sales_key
date_key
customer_key
product_key
quantity
sales_amount

The fact table contains:

Foreign Keys

date_key
customer_key
product_key

Measures

quantity
sales_amount


---

12. Dimension Table

A Dimension gives descriptive information.

Example:

DIM_CUSTOMER

customer_key
customer_name
region
segment

The PDF gives a very useful rule:

Fact answers:

> WHAT HAPPENED?



Dimension answers:

> WHO / WHAT / WHEN / WHERE?





Remember this for exams.


---

13. Fact vs Dimension

Fact	Dimension

Business events	Describes entities
Measures	Descriptive attributes
Usually large	Usually smaller
Contains foreign keys	Contains primary/surrogate keys
Sales amount	Customer name
Quantity	Product category




Best memory trick

FACT = WHAT HAPPENED?

DIMENSION = WHO / WHAT / WHEN / WHERE?


---

14. Grain — VERY IMPORTANT

Grain tells you what exactly one row represents.

Suppose:

FACT_SALES

If the grain is:

> One row = one product line in one sales transaction



then every row must follow that rule.

The PDF specifically warns that without defining grain first, the fact table can become inconsistent. 

Bad

Row 1 = order
Row 2 = product
Row 3 = customer

❌ Inconsistent.

Good

Every row = one product line in one sales transaction

✅ Consistent.


---

15. Surrogate Key

A surrogate key is an artificial key generated by the warehouse.

Example:

SOURCE CUSTOMER_ID     CUSTOMER_KEY

1001                   1
1002                   2
1003                   3

Why?

Because different source systems may have different identifiers.

For example:

CRM → 1001
ERP → C1001

The warehouse can use:

CUSTOMER_KEY = 1

as its common identifier. 

Natural Key vs Surrogate Key

Natural key

Comes from source/business

Has business meaning

Can change


Surrogate key

Created by warehouse

Usually no business meaning

Stable





---

16. Star Schema

This is one of the most important concepts.

A Star Schema has the fact table in the center and dimensions around it.

DIM_CUSTOMER
                   |
                   |
DIM_DATE ---- FACT_SALES ---- DIM_PRODUCT
                   |
                   |
               DIM_STORE

The fact is in the center and dimensions surround it, creating a star-like structure. 

For your lab, the main star is:

DIM_CUSTOMER
                   |
                   |
DIM_DATE ---- FACT_SALES ---- DIM_PRODUCT


---

17. Snowflake Schema

Don't confuse Snowflake the company/platform with Snowflake Schema.

A Snowflake Schema normalizes dimensions. 

Example:

FACT
 |
DIM_PRODUCT
 |
SUBCATEGORY
 |
CATEGORY

So instead of keeping everything in one dimension, the dimension is split into related tables.


---

18. Normalization vs Denormalization

Normalization

Goal:

> Reduce duplicate data.



Example:

PRODUCT
   |
CATEGORY
   |
SUBCATEGORY

Advantages:

Less duplication

Better consistency

Easier updates


Disadvantage:

More joins

More complex analytical queries





---

Denormalization

Keep related information together.

Example:

DIM_PRODUCT

product
subcategory
category
category_description

Advantages:

Fewer joins

Easier analytics

Convenient for BI


Disadvantage:

More repeated information





---

19. SCD — Slowly Changing Dimensions

Suppose:

Alice
Region = North

Later Alice moves to:

Region = South

What should the warehouse do?

That's where Slowly Changing Dimensions (SCD) come in. 

There are three types in your PDF.


---

20. SCD Type 1

Overwrite the old value.

Before:

1 | Alice | North

After:

1 | Alice | South

North is gone.

Use Type 1 when historical changes are not important. 

Memory

Type 1 = REPLACE


---

21. SCD Type 2

Type 2 preserves history.

Before:

101 | Alice | North | Y

After:

101 | Alice | North | N
205 | Alice | South | Y

Now we have two records.

The PDF also shows commonly used fields:

effective_start_date
effective_end_date
is_current



Example:

101 | Alice | North | 2025-01-01 | 2025-06-30 | N
205 | Alice | South | 2025-07-01 | NULL       | Y

Memory

Type 2 = NEW ROW


---

22. SCD Type 3

Type 3 stores current and previous values.

Example:

customer_key
customer_name
current_region
previous_region

Result:

1 | Alice | South | North

It keeps only limited history. 

Memory

Type 3 = NEW COLUMN

Remember all three

TYPE 1 → REPLACE
TYPE 2 → NEW ROW
TYPE 3 → NEW COLUMN




---

23. Now the Actual Snowflake Project

This is the most important practical section.

The PDF creates three databases:

RAW_DB
   ↓
DWH_DB
   ↓
MART_DB



RAW_DB

Contains raw source data:

CUSTOMERS
PRODUCTS
SALES

DWH_DB

Contains modeled warehouse data:

DIM_CUSTOMER
DIM_PRODUCT
DIM_DATE
FACT_SALES

MART_DB

Contains business-facing data:

SALES_SUMMARY


---

24. Create the Databases

CREATE DATABASE IF NOT EXISTS RAW_DB;

CREATE DATABASE IF NOT EXISTS DWH_DB;

CREATE DATABASE IF NOT EXISTS MART_DB;




---

25. Create Schemas

CREATE SCHEMA IF NOT EXISTS RAW_DB.RAW;

CREATE SCHEMA IF NOT EXISTS DWH_DB.STAGING;

CREATE SCHEMA IF NOT EXISTS DWH_DB.DIMENSIONS;

CREATE SCHEMA IF NOT EXISTS DWH_DB.FACTS;

CREATE SCHEMA IF NOT EXISTS MART_DB.SALES;



So the structure becomes:

RAW_DB
 └── RAW

DWH_DB
 ├── STAGING
 ├── DIMENSIONS
 └── FACTS

MART_DB
 └── SALES


---

26. Raw Customer Table

CREATE OR REPLACE TABLE RAW_DB.RAW.CUSTOMERS (
    CUSTOMER_ID INT,
    CUSTOMER_NAME VARCHAR(100),
    REGION VARCHAR(50),
    SEGMENT VARCHAR(50)
);

Then insert:

INSERT INTO RAW_DB.RAW.CUSTOMERS
VALUES
(1001, 'Alice Corp', 'North', 'Enterprise'),
(1002, 'Beta LLC', 'South', 'SMB'),
(1003, 'Gamma Inc', 'West', 'Enterprise');

These are the exact customer examples used in the PDF. 


---

27. Raw Product Table

CREATE OR REPLACE TABLE RAW_DB.RAW.PRODUCTS (
    PRODUCT_ID INT,
    PRODUCT_NAME VARCHAR(100),
    CATEGORY VARCHAR(50),
    SUB_CATEGORY VARCHAR(50)
);

Data:

501 | Laptop Pro   | Electronics | Computers
502 | Office Chair | Furniture   | Chairs
503 | Monitor X    | Electronics | Monitors




---

28. Raw Sales Table

CREATE OR REPLACE TABLE RAW_DB.RAW.SALES (
    SALES_ID INT,
    SALE_DATE DATE,
    CUSTOMER_ID INT,
    PRODUCT_ID INT,
    QUANTITY INT,
    SALES_AMOUNT DECIMAL(12,2)
);

Data:

1 | 2025-01-01 | 1001 | 501 | 10 | 15000
2 | 2025-01-01 | 1002 | 502 |  5 |  1000
3 | 2025-01-02 | 1001 | 503 |  3 |  1200
4 | 2025-01-02 | 1003 | 501 |  4 |  6000
5 | 2025-01-03 | 1002 | 502 |  2 |   400




---

29. Create DIM_CUSTOMER

CREATE OR REPLACE TABLE DWH_DB.DIMENSIONS.DIM_CUSTOMER (
    CUSTOMER_KEY INT,
    CUSTOMER_ID INT,
    CUSTOMER_NAME VARCHAR(100),
    REGION VARCHAR(50),
    SEGMENT VARCHAR(50),
    PRIMARY KEY (CUSTOMER_KEY)
);

Then load it:

INSERT INTO DWH_DB.DIMENSIONS.DIM_CUSTOMER
SELECT
    ROW_NUMBER() OVER (ORDER BY CUSTOMER_ID) AS CUSTOMER_KEY,
    CUSTOMER_ID,
    CUSTOMER_NAME,
    REGION,
    SEGMENT
FROM RAW_DB.RAW.CUSTOMERS;

Notice this:

ROW_NUMBER()

It generates the warehouse's surrogate key.




---

30. DIM_PRODUCT

CREATE OR REPLACE TABLE DWH_DB.DIMENSIONS.DIM_PRODUCT (
    PRODUCT_KEY INT,
    PRODUCT_ID INT,
    PRODUCT_NAME VARCHAR(100),
    CATEGORY VARCHAR(50),
    SUB_CATEGORY VARCHAR(50),
    PRIMARY KEY (PRODUCT_KEY)
);

Load:

INSERT INTO DWH_DB.DIMENSIONS.DIM_PRODUCT
SELECT
    ROW_NUMBER() OVER (ORDER BY PRODUCT_ID) AS PRODUCT_KEY,
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    SUB_CATEGORY
FROM RAW_DB.RAW.PRODUCTS;




---

31. DIM_DATE

This is another important dimension.

CREATE OR REPLACE TABLE DWH_DB.DIMENSIONS.DIM_DATE (
    DATE_KEY INT,
    FULL_DATE DATE,
    DAY INT,
    MONTH INT,
    QUARTER INT,
    YEAR INT,
    PRIMARY KEY (DATE_KEY)
);

The PDF generates DATE_KEY like:

2025-01-01
     ↓
20250101

using:

TO_NUMBER(TO_CHAR(SALE_DATE, 'YYYYMMDD'))




---

32. FACT_SALES

Now we create the center of our Star Schema.

CREATE OR REPLACE TABLE DWH_DB.FACTS.FACT_SALES (
    SALES_KEY INT,
    DATE_KEY INT,
    CUSTOMER_KEY INT,
    PRODUCT_KEY INT,
    QUANTITY_SOLD INT,
    SALES_AMOUNT DECIMAL(12,2),
    PRIMARY KEY (SALES_KEY)
);




---

33. Load FACT_SALES

This is where everything gets connected.

INSERT INTO DWH_DB.FACTS.FACT_SALES
SELECT
    s.SALES_ID AS SALES_KEY,
    d.DATE_KEY,
    c.CUSTOMER_KEY,
    p.PRODUCT_KEY,
    s.QUANTITY,
    s.SALES_AMOUNT
FROM RAW_DB.RAW.SALES s
JOIN DWH_DB.DIMENSIONS.DIM_DATE d
    ON s.SALE_DATE = d.FULL_DATE
JOIN DWH_DB.DIMENSIONS.DIM_CUSTOMER c
    ON s.CUSTOMER_ID = c.CUSTOMER_ID
JOIN DWH_DB.DIMENSIONS.DIM_PRODUCT p
    ON s.PRODUCT_ID = p.PRODUCT_ID;



Understand this carefully

Raw sales contains:

CUSTOMER_ID
PRODUCT_ID
SALE_DATE

We use those to find:

CUSTOMER_KEY
PRODUCT_KEY
DATE_KEY

Then the fact table stores those keys.

So:

DIM_CUSTOMER ──┐
DIM_PRODUCT  ──┼── FACT_SALES
DIM_DATE     ──┘

That's your Star Schema.


---

34. Analytical Queries

Now we use SQL to analyze the warehouse.

Query 1 — Total Sales

SELECT
    SUM(SALES_AMOUNT) AS TOTAL_SALES
FROM DWH_DB.FACTS.FACT_SALES;

Result:

TOTAL_SALES
23600.00




---

35. Sales by Customer

SELECT
    c.CUSTOMER_NAME,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES
FROM DWH_DB.FACTS.FACT_SALES f
JOIN DWH_DB.DIMENSIONS.DIM_CUSTOMER c
    ON f.CUSTOMER_KEY = c.CUSTOMER_KEY
GROUP BY c.CUSTOMER_NAME
ORDER BY TOTAL_SALES DESC;

Output:

Alice Corp    16200.00
Gamma Inc      6000.00
Beta LLC       1400.00



So:

Alice Corp is the highest-selling customer.


---

36. Sales by Category

SELECT
    p.CATEGORY,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES
FROM DWH_DB.FACTS.FACT_SALES f
JOIN DWH_DB.DIMENSIONS.DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY
GROUP BY p.CATEGORY
ORDER BY TOTAL_SALES DESC;

Output:

Electronics    22200.00
Furniture       1400.00



Therefore:

Electronics generated the most revenue.


---

37. Daily Sales

SELECT
    d.FULL_DATE,
    SUM(f.SALES_AMOUNT) AS DAILY_SALES
FROM DWH_DB.FACTS.FACT_SALES f
JOIN DWH_DB.DIMENSIONS.DIM_DATE d
    ON f.DATE_KEY = d.DATE_KEY
GROUP BY d.FULL_DATE
ORDER BY d.FULL_DATE;

Output:

2025-01-01    16000.00
2025-01-02     7200.00
2025-01-03      400.00



This gives us the sales trend by date.


---

38. Customer + Product Analysis

We can combine multiple dimensions:

SELECT
    c.CUSTOMER_NAME,
    p.PRODUCT_NAME,
    SUM(f.QUANTITY_SOLD) AS TOTAL_QUANTITY,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES
FROM DWH_DB.FACTS.FACT_SALES f
JOIN DWH_DB.DIMENSIONS.DIM_CUSTOMER c
    ON f.CUSTOMER_KEY = c.CUSTOMER_KEY
JOIN DWH_DB.DIMENSIONS.DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY
GROUP BY
    c.CUSTOMER_NAME,
    p.PRODUCT_NAME
ORDER BY TOTAL_SALES DESC;

This demonstrates the main advantage of the Star Schema:

FACT
            /   |   \
       Customer Product Date
              ↓
       Business Analysis




---

39. Data Mart

After creating the warehouse, we create a business-facing view.

CREATE OR REPLACE VIEW MART_DB.SALES.SALES_SUMMARY AS
SELECT
    d.FULL_DATE,
    c.CUSTOMER_NAME,
    c.REGION,
    c.SEGMENT,
    p.PRODUCT_NAME,
    p.CATEGORY,
    p.SUB_CATEGORY,
    f.QUANTITY_SOLD,
    f.SALES_AMOUNT
FROM DWH_DB.FACTS.FACT_SALES f
JOIN DWH_DB.DIMENSIONS.DIM_DATE d
    ON f.DATE_KEY = d.DATE_KEY
JOIN DWH_DB.DIMENSIONS.DIM_CUSTOMER c
    ON f.CUSTOMER_KEY = c.CUSTOMER_KEY
JOIN DWH_DB.DIMENSIONS.DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY;

Then:

SELECT *
FROM MART_DB.SALES.SALES_SUMMARY;



The idea is:

RAW_DB
   ↓
DWH_DB
   ↓
FACT + DIMENSIONS
   ↓
MART_DB
   ↓
BI / REPORTS


---

40. Cross-Database Query

Snowflake lets you reference tables using:

DATABASE.SCHEMA.TABLE

For example:

SELECT *
FROM RAW_DB.RAW.CUSTOMERS;

or:

SELECT *
FROM DWH_DB.DIMENSIONS.DIM_CUSTOMER;

or:

SELECT *
FROM MART_DB.SALES.SALES_SUMMARY;



This is very important for your Snowflake lab.


---

41. SCD Type 1 Lab

If Alice changes:

North → South

Type 1:

UPDATE DWH_DB.DIMENSIONS.DIM_CUSTOMER
SET REGION = 'South'
WHERE CUSTOMER_ID = 1001;

Old North is lost. 


---

42. SCD Type 2 Lab

Create:

CUSTOMER_KEY
CUSTOMER_ID
CUSTOMER_NAME
REGION
SEGMENT
EFFECTIVE_START_DATE
EFFECTIVE_END_DATE
IS_CURRENT



Initial:

1 | 1001 | Alice Corp | North | Enterprise
  |      |            |       |
2025-01-01             NULL    TRUE

When she moves:

Step 1 — Close old record

UPDATE DWH_DB.DIMENSIONS.DIM_CUSTOMER_SCD2
SET
    EFFECTIVE_END_DATE = '2025-06-30',
    IS_CURRENT = FALSE
WHERE CUSTOMER_ID = 1001
AND IS_CURRENT = TRUE;

Step 2 — Insert new record

INSERT INTO DWH_DB.DIMENSIONS.DIM_CUSTOMER_SCD2
VALUES
(
    2,
    1001,
    'Alice Corp',
    'South',
    'Enterprise',
    '2025-07-01',
    NULL,
    TRUE
);

Now:

Version 1
North
2025-01-01 → 2025-06-30

Version 2
South
2025-07-01 → Current



That's SCD Type 2.


---

43. Modern Cloud Data Warehouse

The PDF then shows a more complete architecture:

SOURCE SYSTEMS
      ↓
DATA LAKE / RAW STORAGE
      ↓
STAGING
      ↓
ENTERPRISE DATA WAREHOUSE
      ↓
 ┌────┼────┐
Sales Finance HR
 Mart   Mart  Mart
      ↓
BI / ANALYTICS

This architecture is illustrated in the PDF's cloud DWH section. 

It also compares:

Platform	Main idea

Snowflake	Cloud-native data platform / warehouse
BigQuery	Serverless analytics warehouse
Redshift	AWS data warehouse
Databricks	Lakehouse/data + AI platform





---

44. Recommended Learning Order

The PDF recommends not jumping directly into complex pipelines.

The sequence is approximately:

1. Snowflake UI
2. Warehouse
3. Database
4. Schema
5. Table
6. INSERT / SELECT
7. Multiple databases
8. Staging tables
9. File formats
10. Stages
11. COPY INTO
12. Fact + Dimensions
13. Star Schema
14. SCD
15. Data Mart
16. Analytical SQL
17. Batch Pipeline



This is also the order I recommend you learn it.


---

45. Final End-to-End Project

The PDF's final exercise asks you to build:

CSV
 ↓
STAGE
 ↓
RAW TABLE
 ↓
DIMENSIONS
 ↓
FACT
 ↓
SALES MART
 ↓
REPORT



You need to create:

Databases

RAW_DB
DWH_DB
MART_DB

Schemas

RAW_DB.RAW

DWH_DB.STAGING
DWH_DB.DIMENSIONS
DWH_DB.FACTS

MART_DB.SALES

Raw tables

CUSTOMERS
PRODUCTS
SALES

Dimension tables

DIM_CUSTOMER
DIM_PRODUCT
DIM_DATE

Fact

FACT_SALES

Data Mart

SALES_SUMMARY




---

46. Questions You Should Be Able t
