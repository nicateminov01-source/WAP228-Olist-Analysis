# Olist E-Commerce Data Analysis and Reporting Project

## 1. General Summary of the Project
This project involves relational database design, data warehousing (ETL) with Python, and business intelligence analysis utilizing advanced SQL queries based on the **Brazilian E-Commerce Public Dataset by Olist** from Kaggle. The system processes multiple datasets to analyze monthly revenue trends, top-selling categories, payment methods, and delivery performances.

## 2. Development Process and Methodology
The development process was structured into three main phases:
- **Phase 1 (Database Design):** Analyzed the Kaggle datasets to understand relationships and created `schema.sql` with Primary and Foreign Keys to establish a robust relational database.
- **Phase 2 (Data Pipeline/ETL):** Developed `db_loader.py` to automate the extraction of raw CSV files and load them seamlessly into the SQLite database.
- **Phase 3 (Analytics & Visualization):** Wrote `analysis.py` to run complex SQL aggregate queries on the database and utilized Seaborn/Matplotlib to generate visual business reports.

## 3. The Roles of Technologies Used
- **SQL (SQLite3):** Acted as the core data storage and relationship management layer. It was crucial for writing complex `JOIN` and `GROUP BY` operations to filter and aggregate large volumes of data efficiently before bringing it into memory.
- **Programming Language (Python):** Served as the main orchestrator. Pandas was used for initial CSV reading, `sqlite3` for database communication, and Matplotlib/Seaborn for translating raw query results into meaningful visual graphs.
- **GitHub:** Used for version control, allowing me to track changes in my SQL scripts and Python code step-by-step, providing a safe backup and a public portfolio to showcase my development history.

## 4. Challenging Parts of the Project
- **Complex Table Joins:** Connecting 6 different tables (orders, customers, items, products, categories, payments) required careful mapping of foreign keys without losing data integrity or creating duplicate rows.
- **Date/Time Calculations in SQLite:** Calculating the actual delivery times required utilizing specific SQLite functions like `julianday()` and `strftime()` to accurately measure the difference between purchase and delivery timestamps.
- **Handling Outliers:** Ensuring the data visualizations were meaningful meant filtering out canceled orders and extreme outliers in delivery times.

## 5. What I Learned
By the end of this project, I gained hands-on experience in building a complete ETL (Extract, Transform, Load) pipeline. I learned how to bridge Python and SQL, proving that heavy data manipulation is often better handled inside the database (via SQL) rather than in computer memory. I also improved my ability to create professional documentation and manage code using Git.

---

## 🚀 Instructions on How to Run the Code

### Necessary Dependencies
Ensure you have Python installed along with the following libraries:
```bash
pip install pandas matplotlib seaborn
Execution Steps
1.Place the Dataset: Download the Olist dataset from Kaggle and place the .csv files inside a folder named data/ in the root directory.

2.Build Database: Run the following command to create the schema and load the data into olist_ecommerce.db:
python db_loader.py
3.Generate Reports: Run the analysis script to execute SQL queries and generate visualization charts inside the outputs/ folder:
python analysis.py
