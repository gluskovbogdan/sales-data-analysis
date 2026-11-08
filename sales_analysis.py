"""Sales Data Analysis.

Exploratory analysis of an e-commerce sales dataset (Sales_Data.xlsx):
revenue by product, region, month, weekday and sales channel, plus
distributions of price and order revenue.

Charts are saved to the ./plots folder.
"""
import calendar
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)

DATA_FILE = "Sales_Data.xlsx"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def save_and_show(filename):
    """Save the current figure to ./plots and display it."""
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename), dpi=150)
    plt.show()
    plt.close()


# ---------------------------------------------------------------- load data
print(f"Loading data from {DATA_FILE}")
df = pd.read_excel(DATA_FILE)
print(df.head())
print("\nDataset info:")
df.info()

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Revenue"] = df["Quantity"] * df["Price_per_Unit"]
df["Month"] = df["Order_Date"].dt.month
df["Weekday"] = df["Order_Date"].dt.day_name()
year = df["Order_Date"].dt.year.mode()[0]


# ------------------------------------------------- 1. Revenue by product
product_revenue = df.groupby("Product")["Revenue"].sum().sort_values() / 1e6

plt.figure(figsize=(10, 6))
plt.barh(product_revenue.index, product_revenue.values, color="steelblue")
plt.title(f"Revenue by Product, {year}")
plt.xlabel("Revenue, $ million")
plt.ylabel("Product")
save_and_show("01_revenue_by_product.png")

top, low = product_revenue.idxmax(), product_revenue.idxmin()
gap = product_revenue.max() - product_revenue.min()
print(
    f"\nInsight 1: {top} leads with ${product_revenue.max():.1f}M revenue, "
    f"{low} is lowest with ${product_revenue.min():.1f}M. "
    f"The gap is only ${gap:.1f}M, so products perform similarly."
)


# --------------------------------------------------- 2. Revenue by region
region = df.groupby("Region")["Revenue"].sum().sort_values()
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

plt.figure(figsize=(8, 8))
plt.pie(
    region.values,
    labels=region.index,
    colors=colors[: len(region)],
    autopct="%1.1f%%",
    startangle=90,
    textprops={"fontsize": 11},
)
plt.title("Share of Revenue by Region, %")
plt.axis("equal")
save_and_show("02_region_share.png")

share = region / region.sum() * 100
print(
    f"\nInsight 2: {share.idxmax()} is the top region with {share.max():.1f}% "
    f"of total revenue; {share.idxmin()} is lowest with {share.min():.1f}%. "
    "Revenue is spread almost evenly across regions."
)


# ----------------------------------------------------- 3. Monthly revenue
monthly_revenue = df.groupby("Month")["Revenue"].sum() / 1e6
monthly_revenue.index = monthly_revenue.index.map(lambda m: calendar.month_abbr[m])

plt.figure(figsize=(10, 5))
plt.plot(monthly_revenue.index, monthly_revenue.values, marker="o")
plt.title("Revenue by Month")
plt.xlabel("Month")
plt.ylabel("Revenue, $ million")
plt.grid(True, alpha=0.3)
save_and_show("03_monthly_revenue.png")

print(
    f"\nInsight 3: the strongest month is {monthly_revenue.idxmax()} "
    f"(${monthly_revenue.max():.1f}M), the weakest is {monthly_revenue.idxmin()} "
    f"(${monthly_revenue.min():.1f}M). Months have different lengths, "
    "so totals alone are not a fair comparison (see next chart)."
)


# ------------------------------------------- 4. Average daily revenue
daily_revenue = df.groupby("Order_Date")["Revenue"].sum().reset_index()
daily_revenue["Month"] = daily_revenue["Order_Date"].dt.month
avg_daily_rev = daily_revenue.groupby("Month")["Revenue"].mean() / 1e3
avg_daily_rev.index = avg_daily_rev.index.map(lambda m: calendar.month_abbr[m])

plt.figure(figsize=(10, 5))
plt.bar(avg_daily_rev.index, avg_daily_rev.values, color="steelblue")
plt.title("Average Daily Revenue by Month")
plt.xlabel("Month")
plt.ylabel("Average revenue per day, $ thousand")
save_and_show("04_avg_daily_revenue.png")

print(
    "\nInsight 4: average daily revenue is a fairer way to compare months. "
    f"Best: {avg_daily_rev.idxmax()} (${avg_daily_rev.max():.1f}K/day), "
    f"weakest: {avg_daily_rev.idxmin()} (${avg_daily_rev.min():.1f}K/day)."
)


# ----------------------------------------------------- 5. Weekday revenue
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
              "Friday", "Saturday", "Sunday"]
weekday_rev = df.groupby("Weekday")["Revenue"].sum().reindex(days_order) / 1e6

plt.figure(figsize=(10, 5))
plt.bar(weekday_rev.index, weekday_rev.values, color="rebeccapurple")
plt.title("Revenue by Day of the Week")
plt.xlabel("Day of the week")
plt.ylabel("Revenue, $ million")
plt.xticks(rotation=45)
save_and_show("05_weekday_revenue.png")

print(
    f"\nInsight 5: sales peak on {weekday_rev.idxmax()} "
    f"(${weekday_rev.max():.2f}M) and are lowest on {weekday_rev.idxmin()} "
    f"(${weekday_rev.min():.2f}M)."
)


# ---------------------------------------- 6. Region x sales channel
region_channel = (
    df.groupby(["Region", "Sales_Channel"])["Revenue"].sum().unstack() / 1e6
)

region_channel.plot(kind="bar", width=0.8, figsize=(10, 6))
plt.title("Revenue by Region and Sales Channel")
plt.xlabel("Region")
plt.ylabel("Revenue, $ million")
plt.legend(title="Channel")
plt.xticks(rotation=0)
save_and_show("06_region_channel.png")

print("\nInsight 6: leading sales channel per region:")
for reg, row in region_channel.iterrows():
    print(f"  {reg}: {row.idxmax()} (${row.max():.2f}M vs ${row.min():.2f}M)")


# --------------------------------------------- 7. Price distribution
plt.figure(figsize=(10, 5))
plt.hist(df["Price_per_Unit"], bins=20, color="teal", edgecolor="black")
plt.title("Distribution of Unit Price")
plt.xlabel("Unit price, $")
plt.ylabel("Number of orders")
save_and_show("07_price_hist.png")

print(
    f"\nInsight 7: unit prices range from ${df['Price_per_Unit'].min():.2f} "
    f"to ${df['Price_per_Unit'].max():.2f}, mean ${df['Price_per_Unit'].mean():.2f}. "
    "The histogram is close to uniform."
)


# ----------------------------------------- 8. Order revenue distribution
mean_rev = df["Revenue"].mean()
median_rev = df["Revenue"].median()

plt.figure(figsize=(10, 5))
plt.hist(df["Revenue"], bins=40, color="coral", edgecolor="black")
plt.axvline(mean_rev, color="blue", linestyle="dashed", linewidth=2,
            label=f"Mean: {mean_rev:.1f}")
plt.axvline(median_rev, color="red", linestyle="solid", linewidth=2,
            label=f"Median: {median_rev:.1f}")
plt.title("Distribution of Order Revenue")
plt.xlabel("Order revenue, $")
plt.ylabel("Number of orders")
plt.legend()
save_and_show("08_revenue_hist.png")

print(
    f"\nInsight 8: order revenue is right-skewed (it is price x quantity). "
    f"Mean ${mean_rev:.2f} > median ${median_rev:.2f}, so the median describes "
    "a typical order better; large orders pull the mean up."
)


# ----------------------------------------- 9. Price vs quantity
df_sample = df.sample(min(2000, len(df)), random_state=42)
correlation = df["Price_per_Unit"].corr(df["Quantity"])

plt.figure(figsize=(10, 5))
plt.scatter(df_sample["Price_per_Unit"], df_sample["Quantity"],
            alpha=0.5, color="magenta")
plt.title(f"Price vs Quantity (correlation: {correlation:.2f})")
plt.xlabel("Unit price, $")
plt.ylabel("Quantity")
save_and_show("09_price_vs_quantity.png")

print(
    f"\nInsight 9: correlation between price and quantity is {correlation:.4f}, "
    "i.e. no relationship. The scatter plot uses a random sample of 2,000 rows "
    "so that points do not merge into a solid blob."
)


# ------------------------------------ 10. Orders by product and category
prod_cat = (
    df.groupby(["Product", "Category"])["Order_ID"].count().unstack(fill_value=0)
)

prod_cat.plot(kind="bar", width=0.8, figsize=(12, 6))
plt.title("Number of Orders by Product and Category")
plt.xlabel("Product")
plt.ylabel("Number of orders")
plt.legend(title="Category")
plt.xticks(rotation=45)
save_and_show("10_product_category.png")

print(
    f"\nInsight 10: every product appears in every category "
    f"({prod_cat.values.min()}-{prod_cat.values.max()} orders each). "
    "The Category column does not follow real-world logic in this dataset, "
    "so it should not be trusted for category-level conclusions."
)
