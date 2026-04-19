# Lab 9: Building and Deploying Data Apps

## 🎯 Learning Objectives

- Understand modern data app development approaches
- Learn Streamlit for building interactive data applications
- Build a complete data app with Streamlit
- Use Streamlit components for enhanced functionality
- Visualize data using plotly in Streamlit
- Deploy Streamlit apps on the Community Cloud
- Learn Apache Superset for BI dashboards
- Understand Superset's workflow and architecture
- Create a Superset dashboard from scratch
- Create datasets from SQL queries in Superset
- Export and import Superset dashboards
- Integrate DuckDB with both Streamlit and Superset

## 📋 Prerequisites

- Completed Lab 0: Sample Database Setup
- Completed Lab 1A: Introduction to DuckDB
- Python 3.8+ installed
- DuckDB Python package installed
- Basic understanding of web applications

## ⏱️ Estimated Time

90-120 minutes

## 🎓 Conceptual Background

### Modern Data App Development

Data applications enable users to interact with data through intuitive interfaces:

```
┌─────────────────────────────────────────────────────────────┐
│              Data App Development Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Presentation Layer        Logic Layer           Data Layer │
│  ┌──────────┐             ┌──────────┐          ┌──────────┐ │
│  │Streamlit │             │  Python  │          │  DuckDB  │ │
│  │  Apps    │             │  Logic   │          │          │ │
│  └──────────┘             └──────────┘          └──────────┘ │
│                                                              │
│  ┌──────────┐             ┌──────────┐          ┌──────────┐ │
│  │ Superset │             │   SQL    │          │MotherDuck│ │
│  │Dashboards│             │ Queries  │          │          │ │
│  └──────────┘             └──────────┘          └──────────┘ │
│                                                              │
│                    Deployment & Hosting                       │
│              ┌──────────────────────────┐                    │
│              │ Streamlit Cloud          │                    │
│              │ Self-hosted              │                    │
│              │ Containerized             │                    │
│              └──────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### Streamlit vs. Superset

**Streamlit:**
- **Purpose**: Build custom data applications
- **Approach**: Python-based, code-first
- **Flexibility**: High - complete control over UI
- **Learning Curve**: Low for Python developers
- **Use Cases**: Custom analytics tools, data exploration apps

**Superset:**
- **Purpose**: Business intelligence and dashboards
- **Approach**: UI-based, drag-and-drop
- **Flexibility**: Medium - limited to available chart types
- **Learning Curve**: Low for business users
- **Use Cases**: Executive dashboards, reporting, BI

## 🚀 Step-by-Step Instructions

### Step 1: What is Streamlit?

Streamlit is an open-source Python framework for building data apps:

**Key Features:**
- **Pure Python**: No HTML, CSS, or JavaScript required
- **Fast Development**: Turn data scripts into web apps
- **Interactive**: Built-in widgets and interactivity
- **Real-time**: Automatic rerun on user interaction
- **Integration**: Works with pandas, DuckDB, and more

**Installation:**
```bash
pip install streamlit
```

### Step 2: Build Our First App

Create a basic Streamlit app:

```python
# app.py
import streamlit as st
import duckdb
import pandas as pd

st.title("DuckDB Data Explorer")

# Connect to database
@st.cache_resource
def get_connection():
    return duckdb.connect('data/duckdb_practice.db')

con = get_connection()

# Sidebar for table selection
table = st.sidebar.selectbox(
    "Select Table",
    ["sample_customers", "sample_products", "sample_orders", 
     "sample_transactions", "sample_events"]
)

# Load data
@st.cache_data
def load_data(table_name):
    return con.execute(f"SELECT * FROM {table_name}").df()

df = load_data(table)

# Display data
st.subheader(f"Data from {table}")
st.dataframe(df)

# Basic statistics
st.subheader("Statistics")
st.write(df.describe())
```

Run the app:
```bash
streamlit run app.py
```

### Step 3: Using Streamlit Components

Enhance the app with Streamlit components:

```python
import streamlit as st
import duckdb
import plotly.express as px

st.title("Advanced DuckDB Explorer")

# Database connection
@st.cache_resource
def get_connection():
    return duckdb.connect('data/duckdb_practice.db')

con = get_connection()

# Multi-page navigation
page = st.sidebar.radio("Navigate", ["Data Explorer", "Analytics", "SQL Query"])

if page == "Data Explorer":
    st.header("Data Explorer")
    
    # Table selection with multiselect
    tables = con.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    selected_tables = st.multiselect("Select Tables", table_names)
    
    for table in selected_tables:
        st.subheader(table)
        df = con.execute(f"SELECT * FROM {table} LIMIT 100").df()
        st.dataframe(df)
        
        # Column selection
        columns = st.multiselect(f"Select columns from {table}", df.columns, df.columns[:3])
        if columns:
            st.dataframe(df[columns])

elif page == "Analytics":
    st.header("Analytics Dashboard")
    
    # Date range selector
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # Metric cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_customers = con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()[0]
        st.metric("Total Customers", total_customers)
    
    with col2:
        total_products = con.execute("SELECT COUNT(*) FROM sample_products").fetchone()[0]
        st.metric("Total Products", total_products)
    
    with col3:
        total_orders = con.execute("SELECT COUNT(*) FROM sample_orders").fetchone()[0]
        st.metric("Total Orders", total_orders)

elif page == "SQL Query":
    st.header("SQL Query Interface")
    
    # SQL editor
    query = st.text_area("Enter SQL Query", height=200)
    
    if st.button("Execute Query"):
        try:
            result = con.execute(query).df()
            st.dataframe(result)
            st.download_button("Download CSV", result.to_csv(), "query_result.csv")
        except Exception as e:
            st.error(f"Error: {e}")
```

### Step 4: Visualizing Data Using Plotly

Add interactive visualizations:

```python
import streamlit as st
import duckdb
import plotly.express as px
import plotly.graph_objects as go

st.title("DuckDB Visual Analytics")

con = duckdb.connect('data/duckdb_practice.db')

# Customer segment distribution
st.header("Customer Segments")
segment_data = con.execute("""
    SELECT segment, COUNT(*) as count 
    FROM sample_customers 
    GROUP BY segment
""").df()

fig_pie = px.pie(segment_data, values='count', names='segment', 
                 title='Customer Segment Distribution')
st.plotly_chart(fig_pie, use_container_width=True)

# Sales over time
st.header("Sales Over Time")
sales_data = con.execute("""
    SELECT 
        order_date, 
        SUM(total_amount) as daily_sales,
        COUNT(*) as daily_orders
    FROM sample_orders
    GROUP BY order_date
    ORDER BY order_date
""").df()

fig_line = px.line(sales_data, x='order_date', y='daily_sales',
                   title='Daily Sales Trend')
st.plotly_chart(fig_line, use_container_width=True)

# Product category performance
st.header("Product Category Performance")
category_data = con.execute("""
    SELECT 
        p.category,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_revenue
    FROM sample_products p
    JOIN sample_orders o ON p.product_id = o.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
""").df()

fig_bar = px.bar(category_data, x='category', y='total_revenue',
                 title='Revenue by Category',
                 color='order_count')
st.plotly_chart(fig_bar, use_container_width=True)

# Interactive scatter plot
st.header("Customer Analysis")
customer_data = con.execute("""
    SELECT 
        customer_id,
        loyalty_points,
        segment
    FROM sample_customers
""").df()

fig_scatter = px.scatter(customer_data, x='customer_id', y='loyalty_points',
                        color='segment', title='Customer Loyalty Distribution',
                        hover_data=['segment'])
st.plotly_chart(fig_scatter, use_container_width=True)
```

### Step 5: Deploying Our App on Community Cloud

Deploy the Streamlit app:

1. **Prepare for deployment:**
```bash
# Create requirements.txt
echo "streamlit
duckdb
pandas
plotly" > requirements.txt
```

2. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial Streamlit app"
git branch -M main
git remote add origin https://github.com/yourusername/yourapp.git
git push -u origin main
```

3. **Deploy to Streamlit Community Cloud:**
- Go to https://share.streamlit.io
- Click "New app"
- Connect your GitHub repository
- Select your app file (app.py)
- Click "Deploy"

4. **Access your app:**
- Your app will be available at: https://yourapp-yourusername.streamlit.app

### Step 6: What is Apache Superset?

Apache Superset is an open-source BI platform:

**Key Features:**
- **Rich Visualizations**: 40+ chart types
- **SQL Editor**: Built-in SQL query editor
- **Dashboards**: Interactive dashboard builder
- **Caching**: Performance optimization
- **Security**: Row-level security and authentication
- **Integration**: Works with many databases including DuckDB

**Installation (Docker recommended):**
```bash
docker-compose -f docker-compose-non-dev.yml up
```

### Step 7: Superset's Workflow

Superset workflow overview:

1. **Connect to Database**: Add DuckDB as a data source
2. **Create Dataset**: Define tables/views for analysis
3. **Build Charts**: Create visualizations
4. **Create Dashboard**: Combine charts into dashboards
5. **Share**: Distribute dashboards to users

### Step 8: Creating Our First Dashboard

Set up DuckDB connection in Superset:

1. **Add Database Connection:**
   - Go to Data → Databases → + Database
   - Select "DuckDB" from the list
   - Configure connection string: `duckdb:///path/to/database.db`
   - Test connection and save

2. **Create Dataset:**
   - Go to Data → Datasets → + Dataset
   - Select your DuckDB database
   - Choose a table (e.g., sample_orders)
   - Configure columns and metrics
   - Save the dataset

3. **Create First Chart:**
   - Go to Charts → + Chart
   - Select your dataset
   - Choose chart type (e.g., Line Chart)
   - Configure dimensions and metrics
   - Customize appearance
   - Save the chart

4. **Create Dashboard:**
   - Go to Dashboards → + Dashboard
   - Give it a name and description
   - Add your charts
   - Arrange layout
   - Save dashboard

### Step 9: Creating a Dataset from SQL Query

Create a dataset using a custom SQL query:

1. **Create SQL Dataset:**
   - Go to Data → Datasets → + Dataset
   - Select "SQL Lab" tab
   - Enter your SQL query:
   ```sql
   SELECT 
       c.segment,
       COUNT(DISTINCT o.customer_id) as customer_count,
       SUM(o.total_amount) as total_revenue,
       AVG(o.total_amount) as avg_order_value
   FROM sample_customers c
   JOIN sample_orders o ON c.customer_id = o.customer_id
   GROUP BY c.segment
   ```
   - Validate SQL
   - Save as dataset

2. **Use SQL Dataset in Charts:**
   - Create charts using this dataset
   - Build visualizations based on the SQL query results

### Step 10: Exporting and Importing Dashboards

Share Superset dashboards:

1. **Export Dashboard:**
   - Go to your dashboard
   - Click "Actions" → "Export"
   - Choose export format (JSON)
   - Download the file

2. **Import Dashboard:**
   - Go to Dashboards → + Dashboard
   - Select "Import Dashboard"
   - Upload the JSON file
   - Review and configure
   - Save imported dashboard

### Step 11: Advanced Streamlit Features

Implement advanced Streamlit features:

```python
import streamlit as st
import duckdb
import time

# Session state for persistence
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

# Progress indicators
with st.spinner("Loading data..."):
    time.sleep(2)
    st.success("Data loaded!")

# File upload
uploaded_file = st.file_uploader("Upload a file", type=['csv', 'parquet'])
if uploaded_file:
    # Process uploaded file
    st.write(f"Uploaded: {uploaded_file.name}")

# Status messages
st.info("This is an informational message")
st.warning("This is a warning message")
st.error("This is an error message")

# Expander for additional content
with st.expander("Show more details"):
    st.write("Additional information here")

# Tabs for organizing content
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Settings"])
with tab1:
    st.write("Overview content")
with tab2:
    st.write("Details content")
with tab3:
    st.write("Settings content")
```

## 💻 Hands-On Exercises

### Exercise 1: Build Complete Streamlit App

Build a comprehensive Streamlit application:

```python
# Your complete Streamlit app here:
# 1. Database connection with caching
# 2. Multiple pages/sections
# 3. Interactive widgets
# 4. Data visualizations
# 5. Export functionality
```

### Exercise 2: Advanced Streamlit Components

Use advanced Streamlit features:

```python
# Your advanced features here:
# 1. Session state management
# 2. File uploads
# 3. Progress indicators
# 4. Custom themes
# 5. Authentication (optional)
```

### Exercise 3: Superset Dashboard Creation

Create a complete Superset dashboard:

```sql
-- Your SQL queries for Superset datasets:
-- 1. Customer analytics
-- 2. Product performance
-- 3. Sales trends
-- 4. Geographic analysis
```

### Exercise 4: DuckDB Integration

Integrate DuckDB with both tools:

```python
# Your integration code here:
# 1. Streamlit + DuckDB connection
# 2. Superset + DuckDB setup
# 3. Performance optimization
# 4. Error handling
```

### Exercise 5: Deploy and Share

Deploy your applications:

```bash
# Your deployment steps here:
# 1. Prepare Streamlit app for deployment
# 2. Deploy to Streamlit Cloud
# 3. Share Superset dashboard
# 4. Document usage
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Understand the difference between Streamlit and Superset
2. ✅ Be able to build interactive Streamlit apps
3. ✅ Know how to use Streamlit components effectively
4. ✅ Be able to create data visualizations with plotly
5. ✅ Have deployed a Streamlit app to the cloud
6. ✅ Understand Superset's workflow and architecture
7. ✅ Be able to create Superset dashboards
8. ✅ Know how to create datasets from SQL queries
9. ✅ Be able to export and import dashboards
10. ✅ Have integrated DuckDB with both tools

## 🔍 Verification

Verify your applications:

```python
# Streamlit app verification
import streamlit as st
import duckdb

# Test 1: Database connection
con = duckdb.connect('data/duckdb_practice.db')
tables = con.execute("SHOW TABLES").fetchall()
print(f"✓ Connected to database with {len(tables)} tables")

# Test 2: Data loading
df = con.execute("SELECT * FROM sample_customers LIMIT 10").df()
print(f"✓ Data loading works: {len(df)} rows")

# Test 3: Visualization
import plotly.express as px
fig = px.scatter(df, x='customer_id', y='loyalty_points')
print("✓ Plotly visualization works")

print("=== Streamlit App Verified ===")

# Superset verification (manual check)
print("Superset verification:")
print("1. Check DuckDB connection in Superset UI")
print("2. Verify dataset creation")
print("3. Test chart rendering")
print("4. Confirm dashboard functionality")
```

## 🆘 Troubleshooting

### Issue: Streamlit app won't start

**Solution**: Check dependencies and port:
```bash
# Check if port is in use
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Superset cannot connect to DuckDB

**Solution**: Verify database path and permissions:
```python
import duckdb
# Test connection locally
con = duckdb.connect('data/duckdb_practice.db')
print("Local connection works")
```

### Issue: Deployment fails

**Solution**: Check requirements.txt and repository structure:
```bash
# Verify requirements
cat requirements.txt

# Test locally
streamlit run app.py
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 10**: Performance Considerations
2. **Practice more**: Build more complex apps
3. **Explore advanced features**: Look into Streamlit theming and Superset caching
4. **Real-world deployment**: Set up production hosting

---

**You now have the skills to build and deploy modern data applications using Streamlit and Apache Superset with DuckDB!**