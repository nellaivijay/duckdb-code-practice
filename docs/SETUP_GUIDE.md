# DuckDB Practice Environment - Setup Guide

## 🚀 Quick Start

This guide will help you set up the DuckDB practice environment using either Python virtual environment or Docker.

## 📋 Prerequisites

### System Requirements
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB minimum
- **CPU**: 2 cores minimum
- **OS**: Linux, macOS, or Windows with WSL2

### Software Requirements
- **Python** - version 3.8 or higher
- **pip** - Python package manager
- **Docker** (optional, for Docker setup) - version 20.10+

## 🎯 Setup Options

### Option 1: Python Virtual Environment (Recommended)

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
# venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your preferences (optional)
# nano .env
```

#### Step 5: Generate Sample Data

```bash
python3 scripts/generate_sample_data.py
python3 scripts/load_sample_data.py
```

#### Step 6: Start Jupyter Notebook

```bash
jupyter notebook
```

This will start Jupyter and open it in your browser.

### Option 2: Docker Environment

#### Step 1: Clone the Repository

```bash
git clone https://github.com/nellaivijay/duckdb-code-practice.git
cd duckdb-code-practice
```

#### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your preferences (optional)
# nano .env
```

#### Step 3: Start Docker Compose

```bash
docker-compose up -d
```

#### Step 4: Access Jupyter

Open your browser and navigate to: http://localhost:8888

Use the token specified in your `.env` file (default: `duckdb_practice`)

#### Step 5: Generate Sample Data

```bash
# Access the Jupyter container
docker-compose exec jupyter bash

# Generate sample data
python scripts/generate_sample_data.py
python scripts/load_sample_data.py
```

#### Step 6: Stop Services

```bash
docker-compose down
```

## 🔧 Configuration

### Python Environment Configuration

```bash
# Set memory limit for DuckDB
export DUCKDB_MEMORY_LIMIT=4GB

# Set number of threads
export DUCKDB_THREADS=4

# Set database path
export DATABASE_PATH=./data/duckdb_practice.db
```

### DuckDB Configuration in Python

```python
import duckdb

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Configure DuckDB settings
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=4")
con.execute("SET enable_progress_bar=true")
```

### Docker Configuration

Edit the `.env` file to customize:

```bash
# Jupyter configuration
JUPYTER_PORT=8888
JUPYTER_TOKEN=your_secure_token

# DuckDB configuration
DUCKDB_MEMORY_LIMIT=4GB
DUCKDB_THREADS=4

# Sample data configuration
SAMPLE_DATA_SIZE=medium
SAMPLE_DATA_SEED=42
```

## 🧪 Verification Steps

### 1. Verify Python Installation

```bash
python3 --version
# Expected: Python 3.8 or higher
```

### 2. Verify DuckDB Installation

```bash
python3 -c "import duckdb; print(duckdb.__version__)"
# Expected: DuckDB version number
```

### 3. Verify Jupyter Installation

```bash
jupyter --version
# Expected: Jupyter version number
```

### 4. Test Database Connection

```bash
python3 -c "
import duckdb
con = duckdb.connect(':memory:')
con.execute('SELECT 1 as test').fetchall()
print('Database connection successful!')
"
# Expected: Database connection successful!
```

### 5. Verify Sample Data

```bash
python3 -c "
import duckdb
con = duckdb.connect('data/duckdb_practice.db')
result = con.execute('SELECT COUNT(*) FROM sample_customers').fetchone()
print(f'Customers: {result[0]}')
"
# Expected: Customers: 1000
```

## 🔍 Troubleshooting

### Issue: Python Version Too Old

**Solution**:
```bash
# Install Python 3.8+ using pyenv (macOS/Linux)
curl https://pyenv.run | bash
pyenv install 3.9.0
pyenv global 3.9.0
```

### Issue: Pip Install Fails

**Solution**:
```bash
# Upgrade pip
pip install --upgrade pip

# Install with specific version
pip install duckdb==0.9.0
```

### Issue: Jupyter Won't Start

**Solution**:
```bash
# Check if port is already in use
lsof -i :8888

# Use different port
jupyter notebook --port=8889
```

### Issue: Docker Compose Fails

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

### Issue: Sample Data Generation Fails

**Solution**:
```bash
# Check Python dependencies
pip install -r requirements.txt

# Check disk space
df -h

# Run with verbose output
python3 scripts/generate_sample_data.py --verbose
```

### Issue: Database Connection Errors

**Solution**:
```bash
# Check if database file exists
ls -la data/

# Check file permissions
chmod 644 data/*.db

# Recreate database
rm data/*.db
python3 scripts/load_sample_data.py
```

## 📚 Next Steps

After successful setup:

1. **Start with Lab 1**: Environment Setup and Validation
2. **Progress through Labs 2-9**: Learn DuckDB operations and features
3. **Explore Jupyter Notebooks**: Interactive learning environment
4. **Experiment**: Try different queries and optimizations

## 🎓 Learning Path

1. **Lab 1**: Environment Setup → Verify all components
2. **Lab 2**: Basic Operations → Tables, queries, data types
3. **Lab 3**: Advanced Features → Window functions, joins, aggregations
4. **Lab 4**: Python Integration → Python API and pandas integration
5. **Lab 5**: Data Format Operations → Parquet, Arrow, format conversions
6. **Lab 6**: Performance & Optimization → Query optimization and performance
7. **Lab 7**: Extensions & Advanced Features → Extensions and advanced capabilities
8. **Lab 8**: Real-World Patterns → ETL patterns and data processing
9. **Lab 9**: Integration & Production → Production deployment and integration

## 🆘 Support

For issues or questions:

1. Check the main README.md
2. Review specific lab documentation
3. Consult troubleshooting section
4. Check logs for error messages
5. Open an issue on GitHub

---

**Your DuckDB practice environment is ready for learning and experimentation!**