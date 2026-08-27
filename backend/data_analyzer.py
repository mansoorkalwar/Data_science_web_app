class DataAnalyzer:

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

            information.append({
                "name": column,
                "type": str(self.df[column].dtype),
                "missing": int(
                    self.df[column].isnull().sum()
                ),
                "unique": int(
                    self.df[column].nunique()
                )
            })

        return information

    def get_statistics(self):

        numeric_df = self.df.select_dtypes(
            include="number"
        )

        if numeric_df.empty:
            return {}

        statistics = {}

        for column in numeric_df.columns:

            statistics[column] = {
                "count": float(
                    numeric_df[column].count()
                ),
                "mean": float(
                    numeric_df[column].mean()
                ),
                "median": float(
                    numeric_df[column].median()
                ),
                "std": float(
                    numeric_df[column].std()
                ),
                "min": float(
                    numeric_df[column].min()
                ),
                "max": float(
                    numeric_df[column].max()
                )
            }

        return statistics

    def get_numeric_columns(self):

        return self.df.select_dtypes(
            include="number"
        ).columns.tolist()

    def get_categorical_columns(self):

        return self.df.select_dtypes(
            include="object"
        ).columns.tolist()