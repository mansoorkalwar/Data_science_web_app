import pandas as pd


class DataLoader:

    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def load_data(self):

        file_name = self.uploaded_file.filename.lower()

        if file_name.endswith(".csv"):

            encodings = [
                "utf-8",
                "utf-8-sig",
                "latin1",
                "cp1252"
            ]

            for encoding in encodings:

                try:

                    self.uploaded_file.seek(0)

                    return pd.read_csv(
                        self.uploaded_file,
                        encoding=encoding
                    )

                except UnicodeDecodeError:
                    continue

            raise ValueError(
                "Could not determine CSV encoding."
            )

        elif file_name.endswith((".xlsx", ".xls")):

            return pd.read_excel(
                self.uploaded_file
            )

        elif file_name.endswith(".json"):

            return pd.read_json(
                self.uploaded_file
            )

        else:

            raise ValueError(
                "Unsupported file format."
            )