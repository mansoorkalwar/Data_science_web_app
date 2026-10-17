class DataAnalyzer:
    """Calculate basic data-quality metrics and column statistics."""

    def __init__(self, dataframe):
        self.df = dataframe

    def get_rows(self):
        return len(self.df)

    def get_columns(self):
        return len(self.df.columns)

    def get_missing_values(self):
        return int(self.df.isnull().sum().sum())

    def get_duplicates(self):
        return int(self.df.duplicated().sum())

    def get_column_information(self):
        information = []

        for column in self.df.columns:
            series = self.df[column]
            information.append({
                "name": column,
                "type": str(series.dtype),
                "missing": int(series.isnull().sum()),
                "unique": int(series.nunique()),
            })

        return information

    def get_statistics(self):
        numeric_data = self.df.select_dtypes(include="number")

        if numeric_data.empty:
            return {}

        statistics = {}

        for column in numeric_data.columns:
            series = numeric_data[column]
            statistics[column] = {
                "count": float(series.count()),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
            }

        return statistics

    def get_numeric_columns(self):
        return self.df.select_dtypes(include="number").columns.tolist()

    def get_categorical_columns(self):
        return self.df.select_dtypes(include="object").columns.tolist()
