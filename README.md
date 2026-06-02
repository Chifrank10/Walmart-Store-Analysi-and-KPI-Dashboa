# Walmart Sales Analytics Dashboard

## Overview

This project is an end-to-end sales analytics solution that transforms raw Walmart sales data into actionable business insights. The project demonstrates the complete analytics workflow from data cleaning and database integration to business analysis, dashboard development, and deployment.

### Analytics Workflow

Raw Data → Data Cleaning (Pandas) → MySQL Database → SQL Analysis → Streamlit Dashboard → Docker Deployment

---

## Project Objectives

The goal of this project is to:

* Clean and prepare raw sales data for analysis.
* Load the cleaned dataset into a MySQL database.
* Answer key business questions using SQL.
* Build an interactive dashboard for business users.
* Containerize the application using Docker.
* Publish the application to Docker Hub for easy deployment.

---

## Technologies Used

### Data Cleaning & Processing

* Python
* Pandas

### Database

* MySQL
* PyMySQL
* SQLAlchemy

### Data Analysis

* MySQL Workbench
* SQL

### Dashboard Development

* Streamlit
* Plotly

### Deployment & Version Control

* Docker
* Docker Hub
* Git
* GitHub

---

## Data Cleaning Process

The raw Walmart sales dataset was cleaned and transformed using Pandas.

Data preparation tasks included:

* Handling missing values
* Removing duplicate records
* Standardizing column names
* Correcting data types
* Creating date-based fields for analysis
* Preparing the dataset for database loading

After cleaning, the dataset was loaded into MySQL using:

* **PyMySQL** as the database connector
* **SQLAlchemy** as the database engine

---

## Business Questions Answered

The project uses SQL queries to answer key business questions such as:

### Sales Performance

* Which city generated the highest revenue?
* Which branch recorded the highest sales?
* What are the monthly sales trends?

### Customer Behavior

* What payment methods are most frequently used?
* Which product categories generate the most revenue?

### Operational Insights

* Which branches consistently outperform others?
* How do sales vary across cities and time periods?

---

## Dashboard Features

### Executive Summary

* Total Sales
* Total Transactions
* Average Transaction Value

### Sales Analysis

* Sales by City
* Sales by Branch
* Sales by Product Category

### Trend Analysis

* Daily Sales Trends
* Weekly Sales Trends
* Monthly Sales Trends
* Yearly Sales Trends

### Interactive Filters

* City
* Branch
* Product Category
* Payment Method

### Business Insights

* Top Performing Cities
* Top Performing Branches
* Best Selling Categories
* Most Popular Payment Methods

---

## Dashboard Preview

### Sales Overview

![Sales Overview](assets/sales_overview.png)

### Monthly Sales Trend

![Monthly Trend](assets/monthly_trend.png)

### Business Insights

![Business Insights](assets/business_insights.png)

---

## Project Structure

```text
project_walmart/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   └── walmart_analysis.ipynb
│
├── sql/
│   └── business_queries.sql
│
├── app/
│   └── streamlit_app.py
│
├── assets/
│   └── dashboard_images/
│
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore
```

---

## Running the Project Locally

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/walmart-sales-dashboard.git
cd walmart-sales-dashboard
```

### Create a Virtual Environment

```bash
python -m venv myenv
```

### Activate the Environment

**Windows**

```bash
myenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch the Dashboard

```bash
streamlit run app/streamlit_app.py
```

Open your browser and navigate to:

```text
http://localhost:8501
```

---

## Docker Deployment

### Build Docker Image

```bash
docker build -t walmart-dashboard .
```

### Run Docker Container

```bash
docker run -p 8501:8501 walmart-dashboard
```

Access the dashboard at:

```text
http://localhost:8501
```

---

## Docker Hub

Pull the published Docker image:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/walmart-dashboard:latest
```

Run the container:

```bash
docker run -p 8501:8501 YOUR_DOCKERHUB_USERNAME/walmart-dashboard:latest
```

---

## Skills Demonstrated

* Data Cleaning and Transformation
* Exploratory Data Analysis
* SQL Querying and Business Analysis
* Database Integration
* Data Visualization
* Dashboard Development
* Streamlit Application Development
* Docker Containerization
* Version Control with Git and GitHub

---

## Author

**Chisom Ogbulie**

Data Analyst | Business Intelligence Professional

### Technical Skills

* Python
* SQL
* MySQL
* Power BI
* Excel
* Streamlit
* Docker

Feel free to connect with me and explore my other analytics projects.
