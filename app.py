from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from backend.data_loader import DataLoader
from backend.data_analyzer import DataAnalyzer
from backend.store_analyzer import StoreAnalyzer


app = Flask(__name__)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# GENERAL DATA ANALYSIS
# ==========================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_file():

    try:

        file = request.files.get("file")

        if not file:

            return jsonify({
                "error": "No file uploaded."
            }), 400

        # Load dataset

        loader = DataLoader(file)

        df = loader.load_data()

        # Analyze dataset

        analyzer = DataAnalyzer(df)

        result = {

            "rows":
                analyzer.get_rows(),

            "columns":
                analyzer.get_columns(),

            "missing":
                analyzer.get_missing_values(),

            "duplicates":
                analyzer.get_duplicates(),

            "column_info":
                analyzer.get_column_information(),

            "statistics":
                analyzer.get_statistics(),

            "numeric_columns":
                analyzer.get_numeric_columns(),

            "categorical_columns":
                analyzer.get_categorical_columns()
        }

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 400


# ==========================================
# STORE ANALYSIS
# ==========================================

@app.route(
    "/store-analysis",
    methods=["POST"]
)
def store_analysis():

    try:

        file = request.files.get("file")

        if not file:

            return jsonify({
                "error": "No file uploaded."
            }), 400

        # Get selected columns

        sales_column = request.form.get(
            "sales_column"
        )

        profit_column = request.form.get(
            "profit_column"
        )

        quantity_column = request.form.get(
            "quantity_column"
        )

        product_column = request.form.get(
            "product_column"
        )

        category_column = request.form.get(
            "category_column"
        )

        date_column = request.form.get(
            "date_column"
        )

        region_column = request.form.get(
            "region_column"
        )

        # Convert empty values to None

        sales_column = (
            sales_column
            if sales_column
            else None
        )

        profit_column = (
            profit_column
            if profit_column
            else None
        )

        quantity_column = (
            quantity_column
            if quantity_column
            else None
        )

        product_column = (
            product_column
            if product_column
            else None
        )

        category_column = (
            category_column
            if category_column
            else None
        )

        date_column = (
            date_column
            if date_column
            else None
        )

        region_column = (
            region_column
            if region_column
            else None
        )

        # Load data

        loader = DataLoader(file)

        df = loader.load_data()

        # Create StoreAnalyzer object

        store = StoreAnalyzer(
            dataframe=df,
            sales_column=sales_column,
            profit_column=profit_column,
            quantity_column=quantity_column,
            product_column=product_column,
            category_column=category_column,
            date_column=date_column,
            region_column=region_column
        )

        result = {

            "total_sales":
                store.total_sales(),

            "total_profit":
                store.total_profit(),

            "total_quantity":
                store.total_quantity(),

            "total_orders":
                store.total_orders(),

            "best_selling_products":
                store.best_selling_products(),

            "most_profitable_products":
                store.most_profitable_products(),

            "sales_by_category":
                store.sales_by_category(),

            "sales_by_region":
                store.sales_by_region(),

            "sales_over_time":
                store.sales_over_time(),

            "profit_over_time":
                store.profit_over_time(),

            "most_profitable_day":
                store.most_profitable_day(),

            "most_profitable_category":
                store.most_profitable_category()
        }

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 400


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )