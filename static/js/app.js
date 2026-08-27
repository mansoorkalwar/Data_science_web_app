let uploadedFile = null;

let datasetColumns = [];

let salesChart = null;
let productsChart = null;
let profitChart = null;
let categoryChart = null;
let regionChart = null;


// ==========================================
// FILE SELECTION
// ==========================================

document
    .getElementById("fileInput")
    .addEventListener(
        "change",
        function () {

            uploadedFile =
                this.files[0];

            if (uploadedFile) {

                document
                    .getElementById("fileName")
                    .textContent =
                    uploadedFile.name;
            }
        }
    );


// ==========================================
// PAGE NAVIGATION
// ==========================================

function showPage(pageName) {

    const pages =
        document.querySelectorAll(
            ".page"
        );

    pages.forEach(
        page => {
            page.classList.remove(
                "active"
            );
        }
    );


    document
        .getElementById(pageName)
        .classList.add("active");
}


// ==========================================
// GENERAL DATA ANALYSIS
// ==========================================

async function analyzeFile() {

    if (!uploadedFile) {

        alert(
            "Please select a file first."
        );

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


        if (data.error) {

            alert(data.error);

            return;
        }


        // Save columns

        datasetColumns =
            data.column_info.map(
                column => column.name
            );


        // Basic statistics

        document
            .getElementById("rows")
            .textContent =
            data.rows;


        document
            .getElementById("columns")
            .textContent =
            data.columns;


        document
            .getElementById("missing")
            .textContent =
            data.missing;


        document
            .getElementById("duplicates")
            .textContent =
            data.duplicates;


        // Column table

        createColumnTable(
            data.column_info
        );


        // Populate column selectors

        populateSelectors(
            datasetColumns
        );


        // Go to Analysis

        showPage("analysis");

    }

    catch (error) {

        console.error(error);

        alert(
            "Something went wrong."
        );
    }
}


// ==========================================
// COLUMN TABLE
// ==========================================

function createColumnTable(
    columns
) {

    const table =
        document.getElementById(
            "columnTable"
        );


    table.innerHTML = "";


    columns.forEach(
        column => {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `

                <td>
                    ${column.name}
                </td>

                <td>
                    ${column.type}
                </td>

                <td>
                    ${column.missing}
                </td>

                <td>
                    ${column.unique}
                </td>

            `;


            table.appendChild(row);

        }
    );
}


// ==========================================
// COLUMN SELECTORS
// ==========================================

function populateSelectors(
    columns
) {

    const selectors = [

        "salesColumn",
        "profitColumn",
        "quantityColumn",
        "productColumn",
        "categoryColumn",
        "dateColumn",
        "regionColumn"

    ];


    selectors.forEach(
        selectorId => {

            const select =
                document.getElementById(
                    selectorId
                );


            select.innerHTML =
                `<option value="">
                    Not Selected
                </option>`;


            columns.forEach(
                column => {

                    const option =
                        document.createElement(
                            "option"
                        );


                    option.value =
                        column;


                    option.textContent =
                        column;


                    select.appendChild(
                        option
                    );

                }
            );

        }
    );
}


// ==========================================
// STORE ANALYSIS
// ==========================================

async function analyzeStore() {

    if (!uploadedFile) {

        alert(
            "Please upload a dataset first."
        );

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
        document.getElementById(
            "salesColumn"
        ).value
    );


    formData.append(
        "profit_column",
        document.getElementById(
            "profitColumn"
        ).value
    );


    formData.append(
        "quantity_column",
        document.getElementById(
            "quantityColumn"
        ).value
    );


    formData.append(
        "product_column",
        document.getElementById(
            "productColumn"
        ).value
    );


    formData.append(
        "category_column",
        document.getElementById(
            "categoryColumn"
        ).value
    );


    formData.append(
        "date_column",
        document.getElementById(
            "dateColumn"
        ).value
    );


    formData.append(
        "region_column",
        document.getElementById(
            "regionColumn"
        ).value
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


        if (data.error) {

            alert(data.error);

            return;
        }


        // ==================================
        // KPIs
        // ==================================

        document
            .getElementById("totalSales")
            .textContent =
            formatNumber(
                data.total_sales
            );


        document
            .getElementById("totalProfit")
            .textContent =
            formatNumber(
                data.total_profit
            );


        document
            .getElementById("totalQuantity")
            .textContent =
            formatNumber(
                data.total_quantity
            );


        document
            .getElementById("totalOrders")
            .textContent =
            formatNumber(
                data.total_orders
            );


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
        // CHARTS
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
            "Could not generate dashboard."
        );
    }
}


// ==========================================
// FORMAT NUMBERS
// ==========================================

function formatNumber(
    number
) {

    return Number(number)
        .toLocaleString(
            undefined,
            {
                maximumFractionDigits: 2
            }
        );
}


// ==========================================
// BEST PRODUCT
// ==========================================

function showBestProduct(
    products
) {

    const keys =
        Object.keys(products);


    if (keys.length === 0) {

        document
            .getElementById(
                "bestProduct"
            )
            .textContent =
            "Not available";

        return;
    }


    const product =
        keys[0];


    document
        .getElementById(
            "bestProduct"
        )
        .textContent =
        product;
}


// ==========================================
// PROFITABLE PRODUCT
// ==========================================

function showProfitableProduct(
    products
) {

    const keys =
        Object.keys(products);


    if (keys.length === 0) {

        document
            .getElementById(
                "profitableProduct"
            )
            .textContent =
            "Not available";

        return;
    }


    const product =
        keys[0];


    document
        .getElementById(
            "profitableProduct"
        )
        .textContent =
        product;
}


// ==========================================
// PROFITABLE DAY
// ==========================================

function showProfitableDay(
    day
) {

    if (!day) {

        document
            .getElementById(
                "profitableDay"
            )
            .textContent =
            "Not available";

        return;
    }


    document
        .getElementById(
            "profitableDay"
        )
        .textContent =
        `${day.date}
        (${formatNumber(day.profit)})`;
}


// ==========================================
// BEST CATEGORY
// ==========================================

function showBestCategory(
    category
) {

    if (!category) {

        document
            .getElementById(
                "bestCategory"
            )
            .textContent =
            "Not available";

        return;
    }


    document
        .getElementById(
            "bestCategory"
        )
        .textContent =
        category.category;
}


// ==========================================
// SALES CHART
// ==========================================

function createSalesChart(
    salesData
) {

    const canvas =
        document.getElementById(
            "salesChart"
        );


    if (salesChart) {

        salesChart.destroy();
    }


    salesChart =
        new Chart(
            canvas,
            {

                type: "line",

                data: {

                    labels:
                        Object.keys(
                            salesData
                        ),

                    datasets: [{

                        label:
                            "Sales",

                        data:
                            Object.values(
                                salesData
                            ),

                        tension: 0.3,

                        fill: true

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }
        );
}


// ==========================================
// PRODUCTS CHART
// ==========================================

function createProductsChart(
    products
) {

    const canvas =
        document.getElementById(
            "productsChart"
        );


    if (productsChart) {

        productsChart.destroy();
    }


    productsChart =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels:
                        Object.keys(
                            products
                        ),

                    datasets: [{

                        label:
                            "Quantity",

                        data:
                            Object.values(
                                products
                            )

                    }]

                },

                options: {

                    indexAxis: "y",

                    responsive: true,

                    maintainAspectRatio: false

                }

            }
        );
}


// ==========================================
// PROFIT CHART
// ==========================================

function createProfitChart(
    products
) {

    const canvas =
        document.getElementById(
            "profitChart"
        );


    if (profitChart) {

        profitChart.destroy();
    }


    profitChart =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels:
                        Object.keys(
                            products
                        ),

                    datasets: [{

                        label:
                            "Profit",

                        data:
                            Object.values(
                                products
                            )

                    }]

                },

                options: {

                    indexAxis: "y",

                    responsive: true,

                    maintainAspectRatio: false

                }

            }
        );
}


// ==========================================
// CATEGORY CHART
// ==========================================

function createCategoryChart(
    categories
) {

    const canvas =
        document.getElementById(
            "categoryChart"
        );


    if (categoryChart) {

        categoryChart.destroy();
    }


    categoryChart =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(
                            categories
                        ),

                    datasets: [{

                        data:
                            Object.values(
                                categories
                            )

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }
        );
}


// ==========================================
// REGION CHART
// ==========================================

function createRegionChart(
    regions
) {

    const canvas =
        document.getElementById(
            "regionChart"
        );


    if (regionChart) {

        regionChart.destroy();
    }


    regionChart =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels:
                        Object.keys(
                            regions
                        ),

                    datasets: [{

                        label:
                            "Sales",

                        data:
                            Object.values(
                                regions
                            )

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }
        );
}