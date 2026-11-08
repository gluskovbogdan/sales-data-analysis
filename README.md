# Sales Data Analysis (Python, pandas, Matplotlib)

Exploratory analysis of an e-commerce sales dataset with ~50,000 orders.
The goal is to understand where revenue comes from and when customers buy.

## What this project does

- Loads and cleans sales data from Excel (`Sales_Data.xlsx`)
- Calculates revenue per order (`Quantity x Price_per_Unit`)
- Analyzes revenue by **product, region, month, weekday and sales channel**
- Compares months fairly using **average daily revenue**
- Studies distributions (unit price, order revenue) and checks the correlation between price and quantity
- Flags a data-quality issue: the `Category` column does not match real product logic
- Saves 10 charts to the `plots/` folder and prints a short insight for each

## Key findings

*(fill in with the numbers printed by your own run)*

- Revenue is spread almost evenly across products and regions
- Order revenue is right-skewed: the median describes a typical order better than the mean
- Price and quantity are not correlated
- Average daily revenue is a fairer way to compare months of different length

## Charts

![Revenue by product](plots/01_revenue_by_product.png)
![Monthly revenue](plots/03_monthly_revenue.png)
![Region and channel](plots/06_region_channel.png)

## How to run

```bash
pip install pandas matplotlib openpyxl
python sales_analysis.py
```

Put `Sales_Data.xlsx` in the same folder as the script.
Required columns: `Order_ID, Order_Date, Product, Category, Region, Sales_Channel, Quantity, Price_per_Unit`.

## Tools

Python, pandas, Matplotlib
