# Getting Started Guide

This guide will help you get started with the DuckDB Code Practice environment, from installation to running your first query.

## 🎯 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **pip**: Python package manager (included with Python)
- **4GB RAM minimum**: 8GB recommended for better performance
- **2GB disk space**: For sample data and databases

## 📥 Installation

### Option 1: Python Environment (Recommended)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/nellaivijay/duckdb-code-practice.git
cd duckdb-code-practice
```

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- DuckDB
- Pandas
- Jupyter
- NumPy
- PyArrow
- Other required packages

#### Step 4: Verify Installation

```bash
python3 -c "import duckdb; print(duckdb.__version__)"
```

Expected output: DuckDB version number (e.g., 0.9.0)

### Option 2: Docker Environment

#### Step 1: Clone the Repository

```bash
git clone https://github.com/nellaivijay/duckdb-code-practice.git
cd duckdb-code-practice
```

#### Step 2: Start Docker Compose

```bash
docker-compose up -d
```

#### Step 3: Access Jupyter

Open your browser and navigate to: http://localhost:8888

Use the token: `duckdb_practice` (or check your `.env` file)

## 🚀 Quick Start

### Step 1: Run Setup Script

```bash
python3 scripts/setup.py
```

This will:
- Check your Python environment
- Verify dependencies
- Create necessary directories
- Prompt you to generate sample data

### Step 2: Generate Sample Data

```bash
python3 scripts/generate_sample_data.py
```

This creates realistic business data for learning:
- 1,000 customers
- 200 products
- 5,000 orders
- 10,000 transactions
- 20,000 events

### Step 3: Load Sample Data

```bash
python3 scripts/load_sample_data.py
```

This loads the data into DuckDB database and creates indexes.

### Step 4: Start Jupyter Notebook

```bash
jupyter notebook
```

This will open Jupyter in your browser.

## 🎯 Your First Query

### Using Python API

```python
import duckdb

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Run your first query
result = con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()
print(f"Total customers: {result[0]}")

# Close connection
con.close()
```

### Using SQL Shell

```bash
# Start DuckDB shell
duckdb data/duckdb_practice.db

# Run a query
SELECT COUNT(*) FROM sample_customers;

# Exit
.exit
```

### Using Jupyter Notebook

In a Jupyter cell:

```python
import duckdb
import pandas as pd

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Query and display as DataFrame
df = con.execute("SELECT * FROM sample_customers LIMIT 10").df()
display(df)

# Close connection
con.close()
```

## 📚 Next Steps

### Learning Path

1. **Lab 0: Sample Database Setup** - Understand the sample data
2. **Lab 1: Environment Setup** - Verify your installation
3. **Lab 2: Basic Operations** - Learn CRUD operations
4. **Progressive Labs** - Build skills step by step

### Documentation

- [DuckDB Fundamentals](DuckDB-Fundamentals.md) - Core concepts
- [Learning Path](Learning-Path.md) - Recommended sequence
- [Lab Guides](Lab-Guides.md) - Detailed lab walkthroughs
- [Troubleshooting](Troubleshooting.md) - Common issues

## 🔧 Configuration

### Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` to customize:

```bash
# DuckDB Configuration
DUCKDB_MEMORY_LIMIT=4GB
DUCKDB_THREADS=4

# Database Configuration
DATABASE_NAME=duckdb_practice
DATABASE_PATH=./data/duckdb_practice.db

# Jupyter Configuration
JUPYTER_PORT=8888
JUPYTER_TOKEN=duckdb_practice
```

### DuckDB Settings

Configure DuckDB in Python:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Set memory limit
con.execute("SET memory_limit='4GB'")

# Set thread count
con.execute("SET threads=4")

# Enable progress bar
con.execute("SET enable_progress_bar=true")
```

## 🆘 Troubleshooting

### Installation Issues

**Problem**: `pip install` fails

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Try specific version
pip install duckdb==0.9.0
```

**Problem**: Import error for duckdb

**Solution**:
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Reinstall
pip install --force-reinstall duckdb
```

### Database Issues

**Problem**: Cannot connect to database

**Solution**:
```bash
# Check if database file exists
ls -la data/

# Create data directory if needed
mkdir -p data

# Regenerate sample data
python3 scripts/generate_sample_data.py
python3 scripts/load_sample_data.py
```

### Jupyter Issues

**Problem**: Jupyter won't start

**Solution**:
```bash
# Check if port is in use
lsof -i :8888

# Use different port
jupyter notebook --port=8889

# Install Jupyter
pip install jupyter notebook
```

### Docker Issues

**Problem**: Docker containers won't start

**Solution**:
```bash
# Check Docker status
docker ps

# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build
docker-compose up -d
```

## 📖 Learning Resources

### Official Documentation

- [DuckDB Docs](https://duckdb.org/docs/)
- [Python API](https://duckdb.org/docs/api/python/)
- [SQL Reference](https://duckdb.org/docs/sql/)

### Community

- [DuckDB GitHub](https://github.com/duckdb/duckdb)
- [DuckDB Discord](https://discord.gg/duckdb)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/duckdb)

## 🎓 Best Practices

### Development Workflow

1. **Always use virtual environments** for Python projects
2. **Generate fresh sample data** when starting new labs
3. **Close database connections** when done
4. **Use meaningful variable names** in your code
5. **Comment your code** for future reference

### Query Best Practices

1. **Use LIMIT** when exploring data
2. **Use EXPLAIN** to understand query plans
3. **Create indexes** on frequently queried columns
4. **Use appropriate data types** for columns
5. **Test queries** on small samples first

## 🚀 Ready to Learn?

Now that you're set up, start your learning journey:

1. **Read**: [DuckDB Fundamentals](DuckDB-Fundamentals.md)
2. **Practice**: [Lab 0: Sample Database Setup](../labs/lab-00-sample-database.md)
3. **Explore**: Try different queries on sample data
4. **Build**: Create your own analysis projects

---

**Happy learning! 🎉**