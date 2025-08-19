import json

# Define the notebook structure
notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Retail Sales Exploratory Data Analysis\n",
                "\n",
                "This notebook analyzes online retail sales data to uncover insights about customer behavior, product performance, and sales patterns."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Setup and Imports"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ========================\n",
                "# 1. Setup\n",
                "# ========================\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "# Set styles\n",
                "sns.set(style=\"whitegrid\", palette=\"muted\")\n",
                "plt.rcParams[\"figure.figsize\"] = (12,6)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Load Data"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ========================\n",
                "# 2. Load Data\n",
                "# ========================\n",
                "# Download dataset from UCI/Kaggle and adjust path accordingly\n",
                "df = pd.read_excel(\"Online Retail.xlsx\")\n",
                "\n",
                "# Quick look\n",
                "print(df.shape)\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Cleaning"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ========================\n",
                "# 3. Data Cleaning\n",
                "# ========================\n",
                "# Drop rows with missing CustomerID\n",
                "df = df.dropna(subset=[\"CustomerID\"])\n",
                "\n",
                "# Remove cancellations (InvoiceNo starting with 'C')\n",
                "df = df[~df[\"InvoiceNo\"].astype(str).str.startswith(\"C\")]\n",
                "\n",
                "# Create TotalPrice column\n",
                "df[\"TotalPrice\"] = df[\"Quantity\"] * df[\"UnitPrice\"]\n",
                "\n",
                "# Parse dates\n",
                "df[\"InvoiceDate\"] = pd.to_datetime(df[\"InvoiceDate\"])\n",
                "df[\"Year\"] = df[\"InvoiceDate\"].dt.year\n",
                "df[\"Month\"] = df[\"InvoiceDate\"].dt.month\n",
                "df[\"DayOfWeek\"] = df[\"InvoiceDate\"].dt.day_name()\n",
                "df[\"Hour\"] = df[\"InvoiceDate\"].dt.hour"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Exploratory Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ========================\n",
                "# 4. Exploratory Analysis\n",
                "# ========================\n",
                "\n",
                "# --- Basic stats ---\n",
                "print(\"Unique customers:\", df[\"CustomerID\"].nunique())\n",
                "print(\"Unique products:\", df[\"StockCode\"].nunique())\n",
                "print(\"Unique countries:\", df[\"Country\"].nunique())"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# --- Revenue by Month ---\n",
                "monthly_sales = df.groupby([\"Year\",\"Month\"])[\"TotalPrice\"].sum().reset_index()\n",
                "sns.lineplot(data=monthly_sales, x=\"Month\", y=\"TotalPrice\", hue=\"Year\", marker=\"o\")\n",
                "plt.title(\"Monthly Revenue Trend\")\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# --- Revenue by Day of Week ---\n",
                "dow_sales = df.groupby(\"DayOfWeek\")[\"TotalPrice\"].sum().reindex(\n",
                "    [\"Monday\",\"Tuesday\",\"Wednesday\",\"Thursday\",\"Friday\",\"Saturday\",\"Sunday\"]\n",
                ")\n",
                "sns.barplot(x=dow_sales.index, y=dow_sales.values)\n",
                "plt.title(\"Revenue by Day of Week\")\n",
                "plt.xticks(rotation=45)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# --- Top 10 Products ---\n",
                "top_products = df.groupby(\"Description\")[\"TotalPrice\"].sum().sort_values(ascending=False).head(10)\n",
                "sns.barplot(y=top_products.index, x=top_products.values)\n",
                "plt.title(\"Top 10 Products by Revenue\")\n",
                "plt.xlabel(\"Revenue\")\n",
                "plt.ylabel(\"Product\")\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# --- Sales by Country (excluding UK) ---\n",
                "country_sales = df.groupby(\"Country\")[\"TotalPrice\"].sum().sort_values(ascending=False).drop(\"United Kingdom\").head(10)\n",
                "sns.barplot(y=country_sales.index, x=country_sales.values)\n",
                "plt.title(\"Top Countries by Revenue (Excluding UK)\")\n",
                "plt.xlabel(\"Revenue\")\n",
                "plt.ylabel(\"Country\")\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Insights and Conclusions"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ========================\n",
                "# 5. Insights (to write in README)\n",
                "# ========================\n",
                "# Example insights you might find:\n",
                "# - UK dominates revenue, but Netherlands/Germany are key international markets\n",
                "# - Revenue spikes during Q4 → holiday effect\n",
                "# - Small % of products generate majority of revenue (Pareto effect)\n",
                "\n",
                "print(\"Analysis complete! Check the visualizations above for insights.\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write the notebook to file
with open('retail-sales-eda.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("Notebook created successfully!") 