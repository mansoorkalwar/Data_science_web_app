import pandas as pd


class StoreAnalyzer:

    def __init__(
        self,
        dataframe,
        sales_column=None,
        profit_column=None,
        quantity_column=None,
        product_column=None,
        category_column=None,
        date_column=None,
        region_column=None
    ):

        self.df = dataframe

        self.sales_column = sales_column
        self.profit_column = profit_column
        self.quantity_column = quantity_column
        self.product_column = product_column
        self.category_column = category_column
        self.date_column = date_column
        self.region_column = region_column

    # ==========================================
    # KPI
    # ==========================================

    def total_sales(self):

        if not self.sales_column:
            return 0

        return float(
            self.df[self.sales_column].sum()
        )

    def total_profit(self):

        if not self.profit_column:
            return 0

        return float(
            self.df[self.profit_column].sum()
        )

    def total_quantity(self):

        if not self.quantity_column:
            return 0

        return float(
            self.df[self.quantity_column].sum()
        )

    def total_orders(self):

        return len(self.df)

    # ==========================================
    # TOP PRODUCTS
    # ==========================================

    def best_selling_products(self):

        if not self.product_column:
            return {}

        if not self.quantity_column:
            return {}

        result = (
            self.df
            .groupby(self.product_column)
            [self.quantity_column]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        return {
            str(key): float(value)
            for key, value in result.items()
        }

    # ==========================================
    # PROFITABLE PRODUCTS
    # ==========================================

    def most_profitable_products(self):

        if not self.product_column:
            return {}

        if not self.profit_column:
            return {}

        result = (
            self.df
            .groupby(self.product_column)
            [self.profit_column]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        return {
            str(key): float(value)
            for key, value in result.items()
        }

    # ==========================================
    # CATEGORY
    # ==========================================

    def sales_by_category(self):

        if not self.category_column:
            return {}

        if not self.sales_column:
            return {}

        result = (
            self.df
            .groupby(self.category_column)
            [self.sales_column]
            .sum()
            .sort_values(ascending=False)
        )

        return {
            str(key): float(value)
            for key, value in result.items()
        }

    # ==========================================
    # REGION
    # ==========================================

    def sales_by_region(self):

        if not self.region_column:
            return {}

        if not self.sales_column:
            return {}

        result = (
            self.df
            .groupby(self.region_column)
            [self.sales_column]
            .sum()
            .sort_values(ascending=False)
        )

        return {
            str(key): float(value)
            for key, value in result.items()
        }

    # ==========================================
    # SALES OVER TIME
    # ==========================================

    def sales_over_time(self):

        if not self.date_column:
            return {}

        if not self.sales_column:
            return {}

        data = self.df.copy()

        data[self.date_column] = pd.to_datetime(
            data[self.date_column],
            errors="coerce"
        )

        data = data.dropna(
            subset=[self.date_column]
        )

        result = (
            data
            .groupby(self.date_column)
            [self.sales_column]
            .sum()
            .sort_index()
        )

        return {
            str(date.date()): float(value)
            for date, value in result.items()
        }

    # ==========================================
    # PROFIT OVER TIME
    # ==========================================

    def profit_over_time(self):

        if not self.date_column:
            return {}

        if not self.profit_column:
            return {}

        data = self.df.copy()

        data[self.date_column] = pd.to_datetime(
            data[self.date_column],
            errors="coerce"
        )

        data = data.dropna(
            subset=[self.date_column]
        )

        result = (
            data
            .groupby(self.date_column)
            [self.profit_column]
            .sum()
            .sort_index()
        )

        return {
            str(date.date()): float(value)
            for date, value in result.items()
        }

    # ==========================================
    # MOST PROFITABLE DAY
    # ==========================================

    def most_profitable_day(self):

        if not self.date_column:
            return None

        if not self.profit_column:
            return None

        data = self.df.copy()

        data[self.date_column] = pd.to_datetime(
            data[self.date_column],
            errors="coerce"
        )

        data = data.dropna(
            subset=[self.date_column]
        )

        result = (
            data
            .groupby(self.date_column)
            [self.profit_column]
            .sum()
        )

        if result.empty:
            return None

        best_day = result.idxmax()

        return {
            "date": str(best_day.date()),
            "profit": float(result.max())
        }

    # ==========================================
    # MOST PROFITABLE CATEGORY
    # ==========================================

    def most_profitable_category(self):

        if not self.category_column:
            return None

        if not self.profit_column:
            return None

        result = (
            self.df
            .groupby(self.category_column)
            [self.profit_column]
            .sum()
        )

        if result.empty:
            return None

        return {
            "category": str(result.idxmax()),
            "profit": float(result.max())
        }