from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file
)
from io import BytesIO
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

from backend.data_loader import DataLoader
from backend.data_analyzer import DataAnalyzer
from backend.store_analyzer import StoreAnalyzer

from xml.sax.saxutils import escape
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import KeepTogether
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
# PDF REPORT GENERATOR
# ==========================================

@app.route("/download-report", methods=["POST"])
def download_report():
    """Generate a professionally formatted DataSense Analytics PDF report."""
    import pandas as pd

    # Professional color palette
    NAVY = colors.HexColor("#172B4D")
    BLUE = colors.HexColor("#315EFB")
    TEAL = colors.HexColor("#0D9488")
    TEXT = colors.HexColor("#344054")
    MUTED = colors.HexColor("#667085")
    LIGHT = colors.HexColor("#F3F6FA")
    BORDER = colors.HexColor("#E0E6EF")
    WHITE = colors.white

    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "Please upload a dataset first."}), 400

        column_keys = (
            "sales_column", "profit_column", "quantity_column",
            "product_column", "category_column", "date_column",
            "region_column"
        )
        selected = {
            key: request.form.get(key) or None
            for key in column_keys
        }

        df = DataLoader(file).load_data()

        for key, column in selected.items():
            if column and column not in df.columns:
                return jsonify({
                    "error": f"Selected column '{column}' was not found."
                }), 400

        # ---------- DATA CALCULATIONS ----------

        def numeric(column):
            if not column:
                return None
            return pd.to_numeric(df[column], errors="coerce")

        sales = numeric(selected["sales_column"])
        profit = numeric(selected["profit_column"])
        quantity = numeric(selected["quantity_column"])

        def total(series):
            return (
                float(series.sum())
                if series is not None and series.notna().any()
                else None
            )

        def average(series):
            return (
                float(series.mean())
                if series is not None and series.notna().any()
                else None
            )

        total_sales = total(sales)
        total_profit = total(profit)
        total_quantity = total(quantity)
        average_sales = average(sales)

        def fmt(value):
            if value is None or pd.isna(value):
                return "Not available"
            return f"{value:,.2f}"

        def grouped(column, metric):
            if not column or metric is None:
                return None

            frame = pd.DataFrame({
                "label": df[column].fillna("Missing").astype(str),
                "value": metric
            })

            return (
                frame.groupby("label", dropna=False)["value"]
                .sum()
                .sort_values(ascending=False)
            )

        product_col = selected["product_column"]
        product_sales = grouped(product_col, sales)
        product_profit = grouped(product_col, profit)
        product_quantity = grouped(product_col, quantity)

        most_selling = (
            str(product_quantity.index[0])
            if product_quantity is not None and len(product_quantity)
            else None
        )

        most_profitable_day = None
        date_col = selected["date_column"]

        if date_col and profit is not None:
            dates = pd.to_datetime(df[date_col], errors="coerce")
            temp = pd.DataFrame({
                "date": dates,
                "profit": profit
            }).dropna(subset=["date", "profit"])

            if not temp.empty:
                daily = temp.groupby(temp["date"].dt.date)["profit"].sum()
                most_profitable_day = (
                    f"{daily.idxmax()} (profit {fmt(float(daily.max()))})"
                )

        # ---------- PDF DOCUMENT ----------

        buffer = BytesIO()
        page_width, page_height = A4
        margin = 18 * mm
        usable_width = page_width - 2 * margin

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=margin,
            leftMargin=margin,
            topMargin=19 * mm,
            bottomMargin=19 * mm,
            title="DataSense Analytics | Business Report",
            author="DataSense Analytics",
            subject="Dataset analysis and business insights"
        )

        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name="DS_Title",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=29,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=7
        ))

        styles.add(ParagraphStyle(
            name="DS_Subtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=15
        ))

        styles.add(ParagraphStyle(
            name="DS_Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=13,
            spaceAfter=7,
            keepWithNext=True
        ))

        styles.add(ParagraphStyle(
            name="DS_Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=TEXT,
            spaceAfter=5
        ))

        styles.add(ParagraphStyle(
            name="DS_TableHeader",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=WHITE,
            alignment=TA_LEFT,
            wordWrap="CJK"
        ))

        styles.add(ParagraphStyle(
            name="DS_TableCell",
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=TEXT,
            alignment=TA_LEFT,
            wordWrap="CJK"
        ))

        styles.add(ParagraphStyle(
            name="DS_TableNumber",
            parent=styles["DS_TableCell"],
            alignment=TA_RIGHT
        ))

        styles.add(ParagraphStyle(
            name="DS_Insight",
            parent=styles["DS_Body"],
            leftIndent=10,
            firstLineIndent=-8,
            spaceAfter=7
        ))

        def cell(value, style="DS_TableCell"):
            """Safely escape dynamic text and wrap it inside table cells."""
            return Paragraph(escape(str(value)), styles[style])

        def make_table(data, widths, numeric_columns=()):
            """Create consistently styled, readable PDF tables."""
            formatted = []

            for row_index, row in enumerate(data):
                formatted_row = []

                for col_index, value in enumerate(row):
                    if row_index == 0:
                        style = "DS_TableHeader"
                    elif col_index in numeric_columns:
                        style = "DS_TableNumber"
                    else:
                        style = "DS_TableCell"

                    formatted_row.append(cell(value, style))

                formatted.append(formatted_row)

            table = Table(
                formatted,
                colWidths=widths,
                repeatRows=1,
                hAlign="LEFT"
            )

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.45, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))

            return table

        story = [
            Spacer(1, 5 * mm),
            Paragraph("DataSense Analytics", styles["DS_Title"]),
            Paragraph(
                "BUSINESS INTELLIGENCE &amp; DATA ANALYSIS REPORT",
                styles["DS_Subtitle"]
            ),
            Paragraph(
                f"Generated {datetime.now().strftime('%d %B %Y at %H:%M')}",
                styles["DS_Subtitle"]
            ),
            Paragraph("01  Dataset Overview", styles["DS_Section"])
        ]

        # ---------- DATASET OVERVIEW ----------

        overview = [
            ["Metric", "Value", "Metric", "Value"],
            ["Total rows", f"{len(df):,}",
             "Total columns", f"{len(df.columns):,}"],
            ["Missing values", f"{int(df.isna().sum().sum()):,}",
             "Duplicate records", f"{int(df.duplicated().sum()):,}"]
        ]

        story.append(make_table(
            overview,
            [38 * mm, 49 * mm, 38 * mm, 49 * mm]
        ))

        # ---------- SALES KPIs ----------

        story.append(Paragraph("02  Business Performance", styles["DS_Section"]))

        kpis = [
            ["Performance Indicator", "Value",
             "Performance Indicator", "Value"],
            ["Total Sales", fmt(total_sales),
             "Total Profit", fmt(total_profit)],
            ["Average Sales", fmt(average_sales),
             "Total Quantity", fmt(total_quantity)],
            ["Top-selling Product", most_selling or "Not available",
             "Most-profitable Day", most_profitable_day or "Not available"]
        ]

        story.append(make_table(
            kpis,
            [39 * mm, 48 * mm, 39 * mm, 48 * mm]
        ))

        # ---------- PRODUCT SUMMARY ----------

        story.append(Paragraph("03  Product Performance", styles["DS_Section"]))

        summary_rows = [["Product", "Quantity", "Sales", "Profit"]]

        if product_quantity is not None:
            ranked = list(product_quantity.index[:15])
        elif product_sales is not None:
            ranked = list(product_sales.index[:15])
        elif product_profit is not None:
            ranked = list(product_profit.index[:15])
        else:
            ranked = []

        if not ranked:
            summary_rows.append([
                "No product data available", "—", "—", "—"
            ])
        else:
            for product in ranked:
                summary_rows.append([
                    str(product),
                    fmt(float(product_quantity.get(product, 0)))
                    if product_quantity is not None else "—",
                    fmt(float(product_sales.get(product, 0)))
                    if product_sales is not None else "—",
                    fmt(float(product_profit.get(product, 0)))
                    if product_profit is not None else "—"
                ])

        story.append(make_table(
            summary_rows,
            [66 * mm, 36 * mm, 36 * mm, 36 * mm],
            numeric_columns=(1, 2, 3)
        ))

        # ---------- PROFESSIONAL CHARTS ----------

        def add_chart(series, title, color):
            if series is None or series.empty:
                return

            values = series.head(10).sort_values()

            fig, ax = plt.subplots(figsize=(8.0, 3.6))
            fig.patch.set_facecolor("white")
            ax.set_facecolor("white")

            labels = [str(x)[:32] for x in values.index]
            bars = ax.barh(
                labels,
                values.values,
                color=color,
                height=0.62
            )

            ax.set_title(
                title,
                loc="left",
                fontsize=12,
                fontweight="bold",
                color="#172B4D",
                pad=14
            )

            ax.set_xlabel("Value", fontsize=8, color="#667085")
            ax.tick_params(axis="both", labelsize=8, colors="#475467")

            ax.grid(
                axis="x",
                color="#E0E6EF",
                linestyle="--",
                linewidth=0.7
            )
            ax.set_axisbelow(True)

            for spine in ax.spines.values():
                spine.set_visible(False)

            ax.tick_params(axis="y", length=0)
            ax.margins(x=0.15)

            fig.tight_layout(pad=1.5)

            img_buffer = BytesIO()
            fig.savefig(
                img_buffer,
                format="png",
                dpi=190,
                bbox_inches="tight",
                facecolor="white"
            )
            plt.close(fig)
            img_buffer.seek(0)

            story.append(Paragraph(title, styles["DS_Section"]))
            story.append(Image(
                img_buffer,
                width=usable_width,
                height=usable_width * 0.43,
                kind="proportional"
            ))
            story.append(Spacer(1, 3 * mm))

        story.append(PageBreak())
        story.append(Paragraph("04  Visual Analytics", styles["DS_Section"]))

        add_chart(product_sales, "Sales by Product — Top 10", "#315EFB")
        add_chart(product_profit, "Profit by Product — Top 10", "#0D9488")

        # ---------- SALES TREND ----------

        if date_col and sales is not None:
            date_values = pd.to_datetime(df[date_col], errors="coerce")
            temp = pd.DataFrame({
                "date": date_values,
                "sales": sales
            }).dropna(subset=["date", "sales"])

            if not temp.empty:
                trend = (
                    temp.groupby(temp["date"].dt.date)["sales"]
                    .sum()
                    .sort_index()
                    .tail(30)
                )

                fig, ax = plt.subplots(figsize=(8.0, 3.6))
                fig.patch.set_facecolor("white")
                ax.set_facecolor("white")

                ax.plot(
                    range(len(trend)),
                    trend.values,
                    color="#315EFB",
                    marker="o",
                    markersize=3.5,
                    linewidth=2
                )

                ax.set_title(
                    "Sales Trend — Latest 30 Dates",
                    loc="left",
                    fontsize=12,
                    fontweight="bold",
                    color="#172B4D",
                    pad=14
                )

                # Show fewer date labels to prevent crowding.
                step = max(1, len(trend) // 8)
                ticks = list(range(0, len(trend), step))
                if len(trend) - 1 not in ticks:
                    ticks.append(len(trend) - 1)

                ax.set_xticks(ticks)
                ax.set_xticklabels(
                    [str(trend.index[i]) for i in ticks],
                    rotation=35,
                    ha="right",
                    fontsize=7
                )

                ax.tick_params(axis="y", labelsize=8, colors="#475467")
                ax.grid(axis="y", color="#E0E6EF", linestyle="--", linewidth=0.7)

                for spine in ax.spines.values():
                    spine.set_visible(False)

                fig.tight_layout(pad=1.5)

                img_buffer = BytesIO()
                fig.savefig(
                    img_buffer,
                    format="png",
                    dpi=190,
                    bbox_inches="tight",
                    facecolor="white"
                )
                plt.close(fig)
                img_buffer.seek(0)

                story.append(Paragraph(
                    "Sales Trend Over Time",
                    styles["DS_Section"]
                ))
                story.append(Image(
                    img_buffer,
                    width=usable_width,
                    height=usable_width * 0.43,
                    kind="proportional"
                ))

        # ---------- CONCLUSIONS AND INSIGHTS ----------

        story.append(Paragraph(
            "05  Key Findings &amp; Insights",
            styles["DS_Section"]
        ))

        insights = []

        if most_selling:
            insights.append(
                f"Top-selling product by quantity: {most_selling}."
            )

        if product_sales is not None and len(product_sales):
            insights.append(
                f"Highest-sales product: {product_sales.index[0]} "
                f"({fmt(float(product_sales.iloc[0]))})."
            )

        if product_profit is not None and len(product_profit):
            insights.append(
                f"Highest-profit product: {product_profit.index[0]} "
                f"({fmt(float(product_profit.iloc[0]))})."
            )

        if most_profitable_day:
            insights.append(f"Most-profitable day: {most_profitable_day}.")

        if total_sales is not None:
            insights.append(
                f"Total recorded sales: {fmt(total_sales)}. "
                f"Average sales per non-missing row: {fmt(average_sales)}."
            )

        if not insights:
            insights.append(
                "Select relevant sales, profit, quantity, product, and date "
                "columns in the dashboard to generate more detailed insights."
            )

        for insight in insights:
            story.append(Paragraph(
                "•  " + escape(insight),
                styles["DS_Insight"]
            ))

        # ---------- PAGE HEADER AND FOOTER ----------

        def decorate_page(canvas, document):
            canvas.saveState()

            # Slim teal accent at the top
            canvas.setFillColor(TEAL)
            canvas.rect(
                0,
                page_height - 3 * mm,
                page_width,
                3 * mm,
                stroke=0,
                fill=1
            )

            # Footer separator
            canvas.setStrokeColor(BORDER)
            canvas.setLineWidth(0.6)
            canvas.line(
                margin,
                14 * mm,
                page_width - margin,
                14 * mm
            )

            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(MUTED)
            canvas.drawString(
                margin,
                9 * mm,
                "DataSense Analytics  |  Business Report"
            )
            canvas.drawRightString(
                page_width - margin,
                9 * mm,
                f"Page {document.page}"
            )

            canvas.restoreState()

        doc.build(
            story,
            onFirstPage=decorate_page,
            onLaterPages=decorate_page
        )

        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="DataSense_Analytics_Report.pdf"
        )

    except Exception as error:
        app.logger.exception("PDF report generation failed")
        return jsonify({
            "error": f"Could not generate PDF report: {error}"
        }), 400

# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )