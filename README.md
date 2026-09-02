# 🛍️ Online Retail — Customer Purchasing Behavior Analysis

## 📌 Project Description

This project analyzes a real-world transactional dataset from a UK-based online gift retailer to understand customer purchasing behavior. The dataset, sourced from the **UCI Machine Learning Repository**, contains **541,909 transactions** recorded between **December 2010 and December 2011**, involving customers across 37 countries — the majority of whom are wholesale buyers rather than individual consumers.

The goal of this project is to clean, explore, and visualize the data to uncover patterns in **when**, **how much**, and **what** customers purchase, and to identify high-value customers who contribute disproportionately to revenue — insights that would typically support marketing, inventory, and customer-retention decisions in a real retail business.

---

## 🔧 Steps Performed

### 1. Data Import & Setup
- Loaded the raw Excel dataset (`Online_Retail.xlsx`) using `pandas`
- Reviewed dataset shape, structure, column types, and a preview of the data
- Converted `InvoiceDate` to proper datetime format

### 2. Data Cleaning
- Checked for and handled missing values — dropped ~135,000 rows with missing `CustomerID`
- Removed duplicate rows
- Fixed invalid values: negative `Quantity` (returns/cancellations) and zero/negative `UnitPrice` entries
- Resulted in a clean dataset of ~400,000 transactions across 4,338 unique customers

### 3. Feature Engineering
- Created `TotalPrice` = `Quantity × UnitPrice`
- Extracted `Year`, `Month`, `Day`, and `Hour` from `InvoiceDate`
- Built customer-level metrics via `groupby('CustomerID')` to derive `Customer Segment` (Low / Medium / High spenders)
- Categorized `Order Size` (Small / Medium / Large) and `Day Type` (Weekday / Weekend)

### 4. Data Exploration
- Used `describe()`, `value_counts()`, and `unique()` to understand distributions and categories
- Explored patterns using `groupby()` across country, month, and product

### 5. Data Wrangling
- Aggregated and sorted data to identify top customers and top countries by sales
- Restructured summary tables for country-wise and customer-wise analysis

### 6. Statistical Analysis
- Calculated mean, median, mode, standard deviation, variance, and percentiles for `Quantity`, `UnitPrice`, and `TotalPrice`

### 7. Data Visualization
Built a range of visualizations using `matplotlib` and `seaborn` to analyze purchasing behavior:
- **Histograms** — Quantity, UnitPrice, TotalPrice, purchases by Hour and Month
- **Box plots** — identifying high-value customers via the IQR outlier rule, transaction value by customer segment
- **Violin plots** — Quantity distribution by Day Type
- **Count plots** — orders by Day Type, top 10 products by transaction frequency
- **Heatmap** — transaction volume by Month vs Hour of day
- **Pair plot** — relationships between Quantity, UnitPrice, and TotalPrice, colored by Customer Segment
- **Line chart** — monthly sales trend
- **Bar chart** — top 10 countries by total sales

### 8. Version Control
- Tracked project files using Git and published the repository to GitHub

---

## 🛠️ Tools Used

| Tool | Purpose |
|---|---|
| **Python** | Core programming language |
| **Pandas** | Data cleaning, wrangling, and aggregation |
| **NumPy** | Numerical operations |
| **Matplotlib** | Static data visualizations |
| **Seaborn** | Statistical visualizations (violin, heatmap, pairplot, countplot) |
| **openpyxl** | Reading `.xlsx` Excel files |
| **VS Code** | Development environment |
| **Git & GitHub** | Version control and project hosting |

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 💡 Key Insights

- **UK dominates sales** — total UK sales are roughly 25x higher than the next-highest country (Netherlands), confirming this is primarily a domestic UK retailer with a smaller international footprint.
- **Strong seasonality** — sales rise sharply from September through November, peaking in **November** ahead of the holiday season, then dip slightly in December.
- **Clear daily buying pattern** — the vast majority of transactions occur between **10 AM and 3 PM**, with almost no purchasing activity before 7 AM or after 8 PM — consistent with business-hours/B2B ordering behavior.
- **Purchasing behavior is highly right-skewed** — most customers buy in small quantities and spend modestly (median quantity = 5 units), while a small number of bulk/wholesale orders and high-value customers pull the averages up significantly.
- **A small group drives outsized revenue** — using the IQR outlier method, **430 customers** were identified as high-value, with the top customer alone contributing over **£281,000** in total spend.
- **Day type has minimal effect on order size** — Weekday and Weekend purchase quantity distributions are nearly identical in shape and median.
- **Product demand is broad, not concentrated** — the top 10 best-selling products have relatively similar transaction counts, suggesting demand is spread across a wide product catalog rather than dominated by one or two items.

---

## 📂 Project Structure
```
sales_data/
├── Online_Retail.xlsx          # Raw dataset
├── notebook.py                 # Full analysis script
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## 🔗 Dataset Source
[UCI Machine Learning Repository — Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

---

*This project was built as part of my data science learning journey to practice end-to-end EDA: data cleaning, feature engineering, statistical analysis, and visualization storytelling.*
