# FlowState Analytics Dashboard
Python based dashboard for E commerce, product sales and revenue data using the libraries:
# list
- streamlit
- pandas
- matplotlib
- seaborn
- linear regression




A multi-page Streamlit dashboard with a clean **day theme** using Seaborn + Matplotlib.

## Setup

### Folder Structure
```
your_project/
├── Home.py
├── style_utils.py
├── Product_Sales.csv
└── pages/
    ├── Overview.py
    ├── Product.py
    ├── Regions.py
    └── Shipping.py
```

### Install dependencies
```bash
pip install streamlit pandas seaborn matplotlib scikit-learn
```

### Run the dashboard
```bash
streamlit run Home.py
```

## CSV Column Requirements
Your `Product_Sales.csv` must have these columns:
- `Date`, `Region`, `Product`, `Quantity`, `UnitPrice`
- `StoreLocation`, `CustomerType`, `Discount`, `Salesperson`
- `TotalPrice`, `PaymentMethod`, `Promotion`, `Returned`
- `OrderID`, `CustomerName`, `ShippingCost`
- `OrderDate`, `DeliveryDate`, `RegionManager`

## Pages
- **Home** — Portal landing with KPIs and navigation
- **Overview** — Revenue trends, profit distribution, top products, region share
- **Products** — Product performance, heatmap, return rates, profitability table
- **Regions** — Regional breakdown, manager performance, product mix heatmap
- **Shipping** — Delivery times, shipping costs, payment mix, salesperson performance

