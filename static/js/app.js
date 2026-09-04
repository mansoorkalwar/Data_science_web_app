let uploadedFile = null;
let datasetColumns = [];


// ==========================================
// FILE SELECTION
// ==========================================

document
    .getElementById("fileInput")
    .addEventListener("change", function () {

        uploadedFile = this.files[0];

        if (uploadedFile) {

            document
                .getElementById("fileName")
                .textContent =
                `Selected: ${uploadedFile.name}`;
        }
    });


// ==========================================
// PAGE NAVIGATION
// ==========================================

function showPage(pageName) {

    document
        .querySelectorAll(".page")
        .forEach(page => {

            page.classList.remove("active");

        });


    const targetPage =
        document.getElementById(pageName);


    if (targetPage) {

        targetPage.classList.add("active");

    }


    // Update navbar active link

    document
        .querySelectorAll(".nav-link")
        .forEach(link => {

            link.classList.toggle(
                "active-nav",
                link.dataset.page === pageName
            );

        });


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    // Resize Plotly charts when page becomes visible

    setTimeout(() => {

        document
            .querySelectorAll(".plotly-chart")
            .forEach(chart => {

                if (chart.data) {

                    Plotly.Plots.resize(chart);

                }

            });

    }, 150);

}


// ==========================================
// GENERAL DATA ANALYSIS
// ==========================================

async function analyzeFile() {

    if (!uploadedFile) {

        alert("Please select a dataset first.");

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        uploadedFile
    );


    try {

        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok || data.error) {

            alert(
                data.error ||
                "Could not analyze the dataset."
            );

            return;
        }


        // Save dataset columns

        datasetColumns =
            data.column_info.map(
                column => column.name
            );


        // ==================================
        // BASIC STATISTICS
        // ==================================

        document
            .getElementById("rows")
            .textContent =
            formatNumber(data.rows);


        document
            .getElementById("columns")
            .textContent =
            formatNumber(data.columns);


        document
            .getElementById("missing")
            .textContent =
            formatNumber(data.missing);


        document
            .getElementById("duplicates")
            .textContent =
            formatNumber(data.duplicates);


        // Create column information table

        createColumnTable(
            data.column_info
        );


        // Populate selectors

        populateSelectors(
            datasetColumns
        );


        // Open Analysis page

        showPage("analysis");

    }

    catch (error) {

        console.error(error);

        alert(
            "Something went wrong while analyzing your file."
        );

    }

}


// ==========================================
// COLUMN TABLE
// ==========================================

function createColumnTable(columns) {

    const table =
        document.getElementById(
            "columnTable"
        );


    table.innerHTML = "";


    columns.forEach(column => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                <strong>
                    ${escapeHtml(column.name)}
                </strong>
            </td>

            <td>
                ${escapeHtml(column.type)}
            </td>

            <td>
                ${formatNumber(column.missing)}
            </td>

            <td>
                ${formatNumber(column.unique)}
            </td>

        `;


        table.appendChild(row);

    });

}


// ==========================================
// COLUMN SELECTORS
// ==========================================

function populateSelectors(columns) {

    const selectors = [

        "salesColumn",
        "profitColumn",
        "quantityColumn",
        "productColumn",
        "categoryColumn",
        "dateColumn",
        "regionColumn"

    ];


    selectors.forEach(selectorId => {

        const select =
            document.getElementById(
                selectorId
            );


        select.innerHTML = `
            <option value="">
                Not selected
            </option>
        `;


        columns.forEach(column => {

            const option =
                document.createElement(
                    "option"
                );


            option.value = column;

            option.textContent = column;


            select.appendChild(option);

        });

    });

}


// ==========================================
// STORE ANALYSIS
// ==========================================

async function analyzeStore() {

    if (!uploadedFile) {

        alert(
            "Please upload a dataset first."
        );

        showPage("home");

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        uploadedFile
    );


    formData.append(
        "sales_column",
        document
            .getElementById("salesColumn")
            .value
    );


    formData.append(
        "profit_column",
        document
            .getElementById("profitColumn")
            .value
    );


    formData.append(
        "quantity_column",
        document
            .getElementById("quantityColumn")
            .value
    );


    formData.append(
        "product_column",
        document
            .getElementById("productColumn")
            .value
    );


    formData.append(
        "category_column",
        document
            .getElementById("categoryColumn")
            .value
    );


    formData.append(
        "date_column",
        document
            .getElementById("dateColumn")
            .value
    );


    formData.append(
        "region_column",
        document
            .getElementById("regionColumn")
            .value
    );


    try {

        const response =
            await fetch(
                "/store-analysis",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok || data.error) {

            alert(
                data.error ||
                "Could not generate the dashboard."
            );

            return;
        }


        // ==================================
        // KPIs
        // ==================================

        document
            .getElementById("totalSales")
            .textContent =
            formatNumber(data.total_sales);


        document
            .getElementById("totalProfit")
            .textContent =
            formatNumber(data.total_profit);


        document
            .getElementById("totalQuantity")
            .textContent =
            formatNumber(data.total_quantity);


        document
            .getElementById("totalOrders")
            .textContent =
            formatNumber(data.total_orders);


        // ==================================
        // INSIGHTS
        // ==================================

        showBestProduct(
            data.best_selling_products
        );


        showProfitableProduct(
            data.most_profitable_products
        );


        showProfitableDay(
            data.most_profitable_day
        );


        showBestCategory(
            data.most_profitable_category
        );


        // ==================================
        // PLOTLY CHARTS
        // ==================================

        createSalesChart(
            data.sales_over_time
        );


        createProductsChart(
            data.best_selling_products
        );


        createProfitChart(
            data.most_profitable_products
        );


        createCategoryChart(
            data.sales_by_category
        );


        createRegionChart(
            data.sales_by_region
        );


        // Show dashboard

        showPage("dashboard");

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not generate the dashboard."
        );

    }

}


// ==========================================
// HELPER FUNCTIONS
// ==========================================

function formatNumber(number) {

    const value =
        Number(number);


    if (!Number.isFinite(value)) {

        return "0";

    }


    return value.toLocaleString(
        undefined,
        {
            maximumFractionDigits: 2
        }
    );

}


function escapeHtml(value) {

    const div =
        document.createElement("div");


    div.textContent =
        String(value ?? "");


    return div.innerHTML;

}


function firstKey(object) {

    const keys =
        Object.keys(object || {});


    if (keys.length > 0) {

        return keys[0];

    }


    return null;

}


// ==========================================
// INSIGHTS
// ==========================================

function showBestProduct(products) {

    const product =
        firstKey(products);


    document
        .getElementById("bestProduct")
        .textContent =
        product || "Not available";

}


function showProfitableProduct(products) {

    const product =
        firstKey(products);


    document
        .getElementById("profitableProduct")
        .textContent =
        product || "Not available";

}


function showProfitableDay(day) {

    document
        .getElementById("profitableDay")
        .textContent =
        day
            ? `${day.date} (${formatNumber(day.profit)})`
            : "Not available";

}


function showBestCategory(category) {

    document
        .getElementById("bestCategory")
        .textContent =
        category?.category ||
        "Not available";

}


// ==========================================
// PLOTLY CONFIGURATION
// ==========================================

const plotlyConfig = {

    responsive: true,

    displaylogo: false,

    scrollZoom: true,

    modeBarButtonsToRemove: [

        "select2d",
        "lasso2d",
        "autoScale2d"

    ]

};


// ==========================================
// COMMON PLOTLY LAYOUT
// ==========================================

function getPlotLayout(title, extra = {}) {

    return {

        title: {

            text: title,

            font: {

                family:
                    "Plus Jakarta Sans, sans-serif",

                size: 18,

                color: "#172033"

            },

            x: 0.03,

            xanchor: "left"

        },


        paper_bgcolor:
            "rgba(0,0,0,0)",


        plot_bgcolor:
            "rgba(0,0,0,0)",


        font: {

            family:
                "DM Sans, sans-serif",

            color:
                "#667085"

        },


        margin: {

            l: 70,
            r: 35,
            t: 70,
            b: 60

        },


        hoverlabel: {

            bgcolor:
                "#172033",

            font: {

                color:
                    "#ffffff",

                family:
                    "DM Sans, sans-serif"

            }

        },


        ...extra

    };

}


// ==========================================
// EMPTY CHART
// ==========================================

function renderEmptyChart(
    elementId,
    title,
    message
) {

    Plotly.react(

        elementId,

        [],

        getPlotLayout(
            title,
            {

                annotations: [{

                    text: message,

                    showarrow: false,

                    font: {

                        size: 15,

                        color: "#98a2b3"

                    },

                    x: 0.5,

                    y: 0.5

                }],


                xaxis: {

                    visible: false

                },


                yaxis: {

                    visible: false

                }

            }
        ),

        plotlyConfig

    );

}


// ==========================================
// SALES OVER TIME CHART
// ==========================================

function createSalesChart(salesData) {

    const labels =
        Object.keys(salesData || {});


    const values =
        Object.values(salesData || {});


    if (!labels.length) {

        renderEmptyChart(

            "salesChart",

            "Sales Over Time",

            "Select both a Date and Sales column to view this chart."

        );

        return;
    }


    const trace = {

        x: labels,

        y: values,

        type: "scatter",

        mode: "lines+markers",

        name: "Sales",


        line: {

            color: "#315efb",

            width: 3,

            shape: "spline"

        },


        marker: {

            color: "#315efb",

            size: 7

        },


        fill: "tozeroy",

        fillcolor:
            "rgba(49,94,251,0.10)",


        hovertemplate:

            "<b>Date:</b> %{x}<br>" +

            "<b>Sales:</b> %{y:,.2f}" +

            "<extra></extra>"

    };


    const layout =

        getPlotLayout(
            "Sales Over Time",
            {

                hovermode:
                    "x unified",


                xaxis: {

                    title:
                        "Date",

                    gridcolor:
                        "rgba(148,163,184,0.12)",

                    zeroline: false

                },


                yaxis: {

                    title:
                        "Sales",

                    tickformat:
                        ",",

                    gridcolor:
                        "rgba(148,163,184,0.15)",

                    zeroline: false

                },


                showlegend: false

            }
        );


    Plotly.react(

        "salesChart",

        [trace],

        layout,

        plotlyConfig

    );

}


// ==========================================
// TOP SELLING PRODUCTS CHART
// ==========================================

function createProductsChart(products) {

    const names =
        Object.keys(products || {});


    const values =
        Object.values(products || {});


    if (!names.length) {

        renderEmptyChart(

            "productsChart",

            "Top Selling Products",

            "Select Product and Quantity columns to view this chart."

        );

        return;
    }


    const trace = {

        x:
            values.slice().reverse(),

        y:
            names.slice().reverse(),

        type:
            "bar",

        orientation:
            "h",


        marker: {

            color:
                "#315efb"

        },


        hovertemplate:

            "<b>%{y}</b><br>" +

            "Quantity: %{x:,.0f}" +

            "<extra></extra>"

    };


    const layout =

        getPlotLayout(
            "Top Selling Products",
            {

                margin: {

                    l: 150,
                    r: 30,
                    t: 70,
                    b: 55

                },


                xaxis: {

                    title:
                        "Quantity",

                    gridcolor:
                        "rgba(148,163,184,0.15)"

                },


                yaxis: {

                    automargin: true

                },


                showlegend: false

            }
        );


    Plotly.react(

        "productsChart",

        [trace],

        layout,

        plotlyConfig

    );

}


// ==========================================
// MOST PROFITABLE PRODUCTS CHART
// ==========================================

function createProfitChart(products) {

    const names =
        Object.keys(products || {});


    const values =
        Object.values(products || {});


    if (!names.length) {

        renderEmptyChart(

            "profitChart",

            "Most Profitable Products",

            "Select Product and Profit columns to view this chart."

        );

        return;
    }


    const trace = {

        x:
            values.slice().reverse(),

        y:
            names.slice().reverse(),

        type:
            "bar",

        orientation:
            "h",


        marker: {

            color:
                "#16a34a"

        },


        hovertemplate:

            "<b>%{y}</b><br>" +

            "Profit: %{x:,.2f}" +

            "<extra></extra>"

    };


    const layout =

        getPlotLayout(
            "Most Profitable Products",
            {

                margin: {

                    l: 150,
                    r: 30,
                    t: 70,
                    b: 55

                },


                xaxis: {

                    title:
                        "Profit",

                    tickformat:
                        ",",

                    gridcolor:
                        "rgba(148,163,184,0.15)"

                },


                yaxis: {

                    automargin: true

                },


                showlegend: false

            }
        );


    Plotly.react(

        "profitChart",

        [trace],

        layout,

        plotlyConfig

    );

}


// ==========================================
// SALES BY CATEGORY CHART
// ==========================================

function createCategoryChart(categories) {

    const labels =
        Object.keys(categories || {});


    const values =
        Object.values(categories || {});


    if (!labels.length) {

        renderEmptyChart(

            "categoryChart",

            "Sales by Category",

            "Select Category and Sales columns to view this chart."

        );

        return;
    }


    const trace = {

        labels: labels,

        values: values,

        type: "pie",

        hole: 0.62,


        textinfo:
            "percent",


        textposition:
            "inside",


        marker: {

            colors: [

                "#315efb",
                "#7c3aed",
                "#06b6d4",
                "#16a34a",
                "#f59e0b",
                "#ec4899",
                "#64748b"

            ],


            line: {

                color:
                    "#ffffff",

                width: 3

            }

        },


        hovertemplate:

            "<b>%{label}</b><br>" +

            "Sales: %{value:,.2f}<br>" +

            "Share: %{percent}" +

            "<extra></extra>"

    };


    const layout =

        getPlotLayout(
            "Sales by Category",
            {

                showlegend: true,


                legend: {

                    orientation:
                        "h",

                    y:
                        -0.15

                },


                margin: {

                    l: 25,
                    r: 25,
                    t: 70,
                    b: 80

                }

            }
        );


    Plotly.react(

        "categoryChart",

        [trace],

        layout,

        plotlyConfig

    );

}


// ==========================================
// SALES BY REGION CHART
// ==========================================

function createRegionChart(regions) {

    const labels =
        Object.keys(regions || {});


    const values =
        Object.values(regions || {});


    if (!labels.length) {

        renderEmptyChart(

            "regionChart",

            "Sales by Region",

            "Select Region and Sales columns to view this chart."

        );

        return;
    }


    const trace = {

        x: labels,

        y: values,

        type: "bar",


        marker: {

            color:
                "#7c3aed",


            line: {

                color:
                    "#6d28d9",

                width: 1

            }

        },


        hovertemplate:

            "<b>%{x}</b><br>" +

            "Sales: %{y:,.2f}" +

            "<extra></extra>"

    };


    const layout =

        getPlotLayout(
            "Sales by Region",
            {

                xaxis: {

                    title:
                        "Region",

                    gridcolor:
                        "rgba(148,163,184,0.08)"

                },


                yaxis: {

                    title:
                        "Sales",

                    tickformat:
                        ",",

                    gridcolor:
                        "rgba(148,163,184,0.15)"

                },


                showlegend: false

            }
        );


    Plotly.react(

        "regionChart",

        [trace],

        layout,

        plotlyConfig

    );

}