import pandas as pd


class StoreAnalyzer:
    """Calculate sales, profit, product, category, and date insights."""

    def __init__(
        self,
        dataframe,
        sales_column=None,
        profit_column=None,
        quantity_column=None,
        product_column=None,
        category_column=None,
        date_column=None,
        region_column=None,
    ):
        self.df = dataframe
        self.sales_column = sales_column
        self.profit_column = profit_column
        self.quantity_column = quantity_column
        self.product_column = product_column
        self.category_column = category_column
        self.date_column = date_column
        self.region_column = region_column

    def total_sales(self):
        if not self.sales_column:
            return 0
        return float(self.df[self.sales_column].sum())

    def total_profit(self):
        if not self.profit_column:
            return 0
        return float(self.df[self.profit_column].sum())

    def total_quantity(self):
        if not self.quantity_column:
            return 0
        return float(self.df[self.quantity_column].sum())

    def total_orders(self):
        return len(self.df)

    def _group_sum(self, group_column, value_column, limit=None):
        if not group_column or not value_column:
            return {}

        result = (
            self.df.groupby(group_column)[value_column]
            .sum()
            .sort_values(ascending=False)
        )

        if limit is not None:
            result = result.head(limit)

        return {
            str(key): float(value)
            for key, value in result.items()
        }

    def best_selling_products(self):
        return self._group_sum(
            self.product_column, self.quantity_column, limit=10
        )

    def most_profitable_products(self):
        return self._group_sum(
            self.product_column, self.profit_column, limit=10
        )

    def sales_by_category(self):
        return self._group_sum(self.category_column, self.sales_column)

    def sales_by_region(self):
        return self._group_sum(self.region_column, self.sales_column)

    def _time_series(self, value_column):
        if not self.date_column or not value_column:
            return {}

        data = self.df.copy()
        data[self.date_column] = pd.to_datetime(
            data[self.date_column], errors="coerce"
        )
        data = data.dropna(subset=[self.date_column])

        result = (
            data.groupby(self.date_column)[value_column]
            .sum()
            .sort_index()
        )

        return {
            str(date.date()): float(value)
            for date, value in result.items()
        }

    def sales_over_time(self):
        return self._time_series(self.sales_column)

    def profit_over_time(self):
        return self._time_series(self.profit_column)

    def most_profitable_day(self):
        if not self.date_column or not self.profit_column:
            return None

        data = self.df.copy()
        data[self.date_column] = pd.to_datetime(
            data[self.date_column], errors="coerce"
        )
        data = data.dropna(subset=[self.date_column])

        daily_profit = data.groupby(self.date_column)[self.profit_column].sum()
        if daily_profit.empty:
            return None

        best_day = daily_profit.idxmax()
        return {
            "date": str(best_day.date()),
            "profit": float(daily_profit.max()),
        }

    def most_profitable_category(self):
        if not self.category_column or not self.profit_column:
            return None

        category_profit = self.df.groupby(self.category_column)[
            self.profit_column
        ].sum()
        if category_profit.empty:
            return None

        return {
            "category": str(category_profit.idxmax()),
            "profit": float(category_profit.max()),
        }
