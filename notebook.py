import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#Task 1 – Data Import & Setup
df = pd.read_excel(r"C:\Users\Nivetha\Downloads\Online Retail.xlsx")


print(df.head())
print(df.shape)
# First 5 rows
print(df.head())

# Last 5 rows
print(df.tail())

# Number of rows and columns
print(df.shape)

# Column names
print(df.columns)
df.info
df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])
print(df['InvoiceDate'].dtype)

#Task 2 – Data Cleaning
#checking for null values:
print(df.isnull().sum())
#sice customer id has huge number of null values we will drop it
df=df.dropna(subset=['CustomerID'])
print(df.head())
#checking duplicate values


df = df.drop_duplicates()
print(df.shape)
#Fix invalid values (negative quantity, invalid price)
# Replace negative Quantity values with 0
df.loc[df['Quantity'] < 0, 'Quantity'] = 0

# Replace invalid UnitPrice values (0 or negative) with median price
median_price = df.loc[df['UnitPrice'] > 0, 'UnitPrice'].median()
df.loc[df['UnitPrice'] <= 0, 'UnitPrice'] = median_price
print("Negative Quantity:", (df['Quantity'] < 0).sum())
print("Invalid UnitPrice:", (df['UnitPrice'] <= 0).sum())
#Task 3 – Feature Engineering
#● Create TotalPrice = Quantity × UnitPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
print(df[['Quantity', 'UnitPrice', 'TotalPrice']].head())
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Day'] = df['InvoiceDate'].dt.day
df['Hour'] = df['InvoiceDate'].dt.hour
print(df[['InvoiceDate', 'Year', 'Month', 'Day', 'Hour']].head())

#Create categories (Customer Segment, Order Size, Day Type)
customer_total = df.groupby('CustomerID')['TotalPrice'].sum()

df['Customer Segment'] = df['CustomerID'].map(
    lambda x: 'High' if customer_total[x] > 5000
    else 'Medium' if customer_total[x] > 1000
    else 'Low'
)
df['Order Size'] = df['Quantity'].apply(
    lambda x: 'Small' if x <= 10
    else 'Medium' if x <= 50
    else 'Large'
)
df['Day Type'] = df['InvoiceDate'].dt.dayofweek.apply(
    lambda x: 'Weekend' if x >= 5 else 'Weekday'
)

print(df[['CustomerID', 'TotalPrice', 'Customer Segment',
          'Quantity', 'Order Size', 'InvoiceDate', 'Day Type']].head())
#Task 4 – Data Exploration
#● Use describe() and dataset overview
print(df.describe())
print(df.describe(include='object'))
#Analyze categories (value_counts(), unique())
print(df['Customer Segment'].value_counts())
print(df['Order Size'].value_counts())
print(df['Day Type'].value_counts())

print(df['Customer Segment'].unique())
print(df['Order Size'].unique())
print(df['Day Type'].unique())
#Perform groupby() (country, month, product)
print("Sales by Country:")
print(df.groupby('Country')['TotalPrice'].sum())

print("\nSales by Month:")
print(df.groupby('Month')['TotalPrice'].sum())

print("\nSales by Product:")
print(df.groupby('Description')['TotalPrice'].sum())
#Task 5 – Data Wrangling
#Aggregate data using groupby()
print(df.groupby('Country')['TotalPrice'].sum())
print(df.groupby('Month')['TotalPrice'].sum())

#Sort to find the top customers and countries
top_customers = df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)

print(top_customers)
top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

print(top_countries)

#Restructure data if needed
country_summary = df.groupby('Country', as_index=False)['TotalPrice'].sum()

country_summary = country_summary.sort_values(
    by='TotalPrice',
    ascending=False
)

print(country_summary)
customer_summary = df.groupby('CustomerID', as_index=False)['TotalPrice'].sum()

customer_summary = customer_summary.sort_values(
    by='TotalPrice',
    ascending=False
)

print(customer_summary)
#Restructured the data by creating aggregated summary tables using groupby() for customer-wise and country-wise analysis
#Task 6 – Statistical Analysis
#● Analyze Quantity, UnitPrice, TotalPrice

print(df[['Quantity', 'UnitPrice', 'TotalPrice']].describe())

#● Calculate mean, median, and mode
#● Find standard deviation, variance, and percentiles
columns = ['Quantity', 'UnitPrice', 'TotalPrice']

print("Mean:")
print(df[columns].mean())

print("\nMedian:")
print(df[columns].median())

print("\nMode:")
print(df[columns].mode().iloc[0])

print("\nStandard Deviation:")
print(df[columns].std())

print("\nVariance:")
print(df[columns].var())

print("\nPercentiles:")
print(df[columns].quantile([0.25, 0.50, 0.75, 0.90]))

#Task 7 – Data Visualization
#1. Line Chart – Best Sales Month
#This helps identify which month has the highest sales
monthly_sales = df.groupby('Month')['TotalPrice'].sum()

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()

#Business insight: The month with the highest point is the best sales month
#2. Bar Chart – Top Countries
#This directly supports your Top Country insight
country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
country_sales.plot(kind='bar')
plt.title('Top 10 Countries by Sales')
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

#3. Histogram – Quantity Distribution
# 7.1 Histogram: Quantity distribution
# ------------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.hist(df['Quantity'], bins=40, range=(0, df['Quantity'].quantile(0.99)),
         color='#4C72B0', edgecolor='white')
plt.title('Distribution of Quantity Purchased per Transaction')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('hist_quantity.png', dpi=150)
plt.show()

# 7.4 Histogram: Purchases by Hour of Day
# ------------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.hist(df['Hour'], bins=24, color='#64B5CD', edgecolor='white')
plt.title('Distribution of Purchases by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Transactions')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig('hist_purchase_hour.png', dpi=150)
plt.show()


# 7.5 Histogram: Purchases by Month

plt.figure(figsize=(8, 5))
plt.hist(df['Month'], bins=12, color='#8172B2', edgecolor='white')
plt.title('Distribution of Purchases by Month')
plt.xlabel('Month')
plt.ylabel('Number of Transactions')
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig('hist_purchase_month.png', dpi=150)
plt.show()
#4. Box Plot – Total Price
#This is useful for identifying high-value transactions and outliers
# 8.2 Box plot: Total Price per Transaction by Customer Segment
# ------------------------------------------------------------------
plt.figure(figsize=(8, 5))
segment_order = ['Low', 'Medium', 'High']
data_by_segment = [df.loc[df['Customer Segment'] == seg, 'TotalPrice'] for seg in segment_order]
plt.boxplot(data_by_segment, tick_labels=segment_order, patch_artist=True,
            boxprops=dict(facecolor='#DD8452'),
            medianprops=dict(color='black'),
            flierprops=dict(marker='o', markerfacecolor='red', markersize=3, alpha=0.4))
plt.title('Transaction Value by Customer Segment')
plt.xlabel('Customer Segment')
plt.ylabel('Total Price')
plt.tight_layout()
plt.savefig('box_segment_totalprice.png', dpi=150)
plt.show()


 
top_products = df['Description'].value_counts().head(10)
#5. Count Plot – Top 10 Products by Number of Transactions
 
plt.figure(figsize=(10, 6))
sns.countplot(data=df[df['Description'].isin(top_products.index)],
              y='Description', order=top_products.index,
              hue='Description', palette='viridis', legend=False)
plt.title('Top 10 Products by Number of Transactions')
plt.xlabel('Number of Transactions')
plt.ylabel('Product Description')
plt.tight_layout()
plt.savefig('countplot_top_products.png', dpi=150)
plt.show()
plt.show()

#6. Violin Plot – Quantity by Day Type

plt.figure(figsize=(8, 6))
sns.violinplot(data=df[df['Quantity'] <= df['Quantity'].quantile(0.99)],
                x='Day Type', y='Quantity', order=['Weekday', 'Weekend'],
                hue='Day Type', palette={'Weekday': '#4C72B0', 'Weekend': '#C44E52'},
                legend=False)
plt.title('Quantity Distribution by Day Type')
plt.xlabel('Day Type')
plt.ylabel('Quantity')
plt.tight_layout()
plt.savefig('violin_quantity_daytype.png', dpi=150)
plt.show()
#7. Heatmap – Transaction Volume by Month vs Hour of Day (seaborn)
 
heatmap_data = pd.crosstab(df['Month'], df['Hour'])
 
plt.figure(figsize=(14, 7))
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.3, linecolor='white')
plt.title('Number of Transactions by Month and Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Month')
plt.tight_layout()
plt.savefig('heatmap_month_hour.png', dpi=150)
plt.show()

 #8. Pair Plot – Quantity, UnitPrice, TotalPrice (colored by Customer Segment) using seaborn
sample_df = df[['Quantity', 'UnitPrice', 'TotalPrice', 'Customer Segment']].sample(
    n=2000, random_state=42)
 
# Clip extreme outliers so the plot isn't dominated by a few huge values
for col in ['Quantity', 'UnitPrice', 'TotalPrice']:
    cap = df[col].quantile(0.99)
    sample_df = sample_df[sample_df[col] <= cap]
 
sns.pairplot(sample_df, hue='Customer Segment', hue_order=['Low', 'Medium', 'High'],
             palette={'Low': '#4C72B0', 'Medium': '#DD8452', 'High': '#C44E52'},
             diag_kind='hist', plot_kws=dict(alpha=0.5, s=20))
plt.suptitle('Pair Plot of Quantity, UnitPrice, TotalPrice by Customer Segment', y=1.02)
plt.savefig('pairplot_features.png', dpi=150, bbox_inches='tight')
plt.show()