# Troubleshooting Guide

This guide covers common issues and solutions for the DuckDB Code Practice environment.

## 🔧 Installation Issues

### Problem: Python Version Too Old

**Error**: `SyntaxError` or import errors when running scripts

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.8+ using pyenv (macOS/Linux)
curl https://pyenv.run | bash
pyenv install 3.9.0
pyenv global 3.9.0

# Or download from python.org
# https://www.python.org/downloads/
```

### Problem: pip Install Fails

**Error**: `pip install` command fails with dependency errors

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing with specific versions
pip install duckdb==0.9.0 pandas==2.0.0

# Use virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Problem: DuckDB Import Error

**Error**: `ModuleNotFoundError: No module named 'duckdb'`

**Solution**:
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Reinstall DuckDB
pip install --force-reinstall duckdb

# Verify installation
python3 -c "import duckdb; print(duckdb.__version__)"
```

## 🗄️ Database Issues

### Problem: Database Connection Fails

**Error**: `duckdb.IOException: IO Error: Cannot open file`

**Solution**:
```bash
# Check if data directory exists
ls -la data/

# Create data directory if needed
mkdir -p data

# Check file permissions
chmod 755 data

# Regenerate sample data
python3 scripts/generate_sample_data.py
python3 scripts/load_sample_data.py
```

### Problem: Database Locked

**Error**: `duckdb.IOException: Database is locked`

**Solution**:
```python
# Ensure you close connections properly
import duckdb
con = duckdb.connect('database.db')
# ... your code ...
con.close()  # Always close connections

# Use context manager
with duckdb.connect('database.db') as con:
    result = con.execute("SELECT * FROM table").fetchall()
# Connection automatically closed
```

### Problem: Out of Memory

**Error**: `OutOfMemoryError` or performance issues

**Solution**:
```python
# Increase memory limit
con.execute("SET memory_limit='8GB'")

# Reduce data size
python3 scripts/generate_sample_data.py --size small

# Process data in batches
for batch in con.execute("SELECT * FROM large_table").fetchmany(1000):
    # Process batch
    pass
```

## 📊 Data Loading Issues

### Problem: Sample Data Generation Fails

**Error**: Sample data script fails with pandas/numpy errors

**Solution**:
```bash
# Install required packages
pip install pandas numpy

# Check disk space
df -h

# Run with verbose output
python3 scripts/generate_sample_data.py --verbose

# Try smaller dataset
python3 scripts/generate_sample_data.py --size small
```

### Problem: Data Loading Fails

**Error**: `COPY command failed` or data loading errors

**Solution**:
```bash
# Check if sample data files exist
ls -la data/sample/

# Verify file format
file data/sample/*.parquet

# Try loading from CSV instead
python3 scripts/load_sample_data.py --format csv

# Check database schema
python3 -c "
import duckdb
con = duckdb.connect('data/duckdb_practice.db')
print(con.execute('SHOW TABLES').fetchall())
"
```

### Problem: Missing Tables After Loading

**Error**: Queries fail with `Table does not exist`

**Solution**:
```python
import duckdb

# Check what tables exist
con = duckdb.connect('data/duckdb_practice.db')
tables = con.execute("SHOW TABLES").fetchall()
print("Available tables:", tables)

# Recreate schema if needed
python3 scripts/load_sample_data.py

# Verify data
for table in tables:
    count = con.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
    print(f"{table[0]}: {count} rows")
```

## 🔌 Jupyter Issues

### Problem: Jupyter Won't Start

**Error**: Jupyter server fails to start or port conflicts

**Solution**:
```bash
# Check if port is in use
lsof -i :8888

# Use different port
jupyter notebook --port=8889

# Kill existing process
kill -9 <PID>

# Reinstall Jupyter
pip install --force-reinstall jupyter notebook
```

### Problem: Kernel Connection Issues

**Error**: Kernel connects but can't execute code

**Solution**:
```bash
# Install IPython kernel
pip install ipykernel

# Register kernel
python3 -m ipykernel install --user --name=duckdb-env

# Restart Jupyter
jupyter notebook
```

### Problem: DuckDB Not Available in Jupyter

**Error**: `ModuleNotFoundError` in Jupyter cells

**Solution**:
```python
# Install in the same environment as Jupyter
!pip install duckdb

# Or install from notebook
import sys
!{sys.executable} -m pip install duckdb

# Restart kernel after installation
```

## 🐳 Docker Issues

### Problem: Docker Containers Won't Start

**Error**: Docker compose fails to start containers

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

# Check Docker daemon
sudo systemctl status docker  # Linux
# or restart Docker Desktop (macOS/Windows)
```

### Problem: Volume Mount Issues

**Error**: Permission denied or volume mount errors

**Solution**:
```bash
# Check file permissions
ls -la data/

# Fix permissions
chmod 755 data
chmod 644 data/*

# Use absolute paths in docker-compose.yaml
# volumes:
#   - /absolute/path/to/data:/data

# On Windows, check drive sharing settings
# in Docker Desktop settings
```

### Problem: Network Issues

**Error**: Containers can't communicate or access services

**Solution**:
```bash
# Check network
docker network ls
docker network inspect duckdb-practice-network

# Recreate network
docker-compose down
docker network prune
docker-compose up -d

# Check firewall settings
# Ensure Docker can create networks
```

## 💻 Query Issues

### Problem: Slow Query Performance

**Issue**: Queries take longer than expected

**Solution**:
```python
# Use EXPLAIN to analyze query plan
con.execute("EXPLAIN SELECT * FROM large_table WHERE column = 'value'").fetchall()

# Create indexes on frequently queried columns
con.execute("CREATE INDEX idx_column ON table(column)")

# Use LIMIT when exploring data
con.execute("SELECT * FROM table LIMIT 100").fetchall()

# Optimize configuration
con.execute("SET threads=8")
con.execute("SET memory_limit='8GB'")
```

### Problem: Incorrect Query Results

**Issue**: Queries return unexpected or incorrect results

**Solution**:
```python
# Verify data types
con.execute("DESCRIBE table").fetchall()

# Check for NULL values
con.execute("SELECT COUNT(*) FROM table WHERE column IS NULL").fetchone()

# Test with small sample first
con.execute("SELECT * FROM table LIMIT 10").fetchall()

# Use explicit column names instead of *
con.execute("SELECT column1, column2 FROM table").fetchall()
```

### Problem: Syntax Errors

**Error**: SQL syntax errors or parser errors

**Solution**:
```python
# Check DuckDB SQL reference
# https://duckdb.org/docs/sql/

# Use proper quoting
con.execute("SELECT * FROM table WHERE name = 'value'")  # Single quotes for strings
con.execute("SELECT * FROM \"table\"")  # Double quotes for identifiers

# Check for reserved words
# Avoid using reserved words as column names

# Use parameterized queries
con.execute("SELECT * FROM table WHERE id = ?", [1])
```

## 🔧 Configuration Issues

### Problem: Environment Variables Not Loading

**Issue**: Settings from .env file not being applied

**Solution**:
```bash
# Ensure .env file exists
ls -la .env

# Check file format
cat .env

# Load environment variables manually
export $(cat .env | xargs)

# Use python-dotenv in Python
pip install python-dotenv
```

### Problem: DuckDB Settings Not Applied

**Issue**: Configuration settings don't seem to take effect

**Solution**:
```python
# Check current settings
con.execute("SELECT * FROM duckdb_settings()").fetchall()

# Set settings before creating tables
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=4")

# Verify settings
con.execute("SELECT current_setting('memory_limit')").fetchone()
```

## 📦 Extension Issues

### Problem: Extension Installation Fails

**Error**: Extension installation or loading fails

**Solution**:
```python
# Install extension
con.execute("INSTALL httpfs")

# Load extension
con.execute("LOAD httpfs")

# Verify installation
con.execute("SELECT * FROM duckdb_extensions()").fetchall()

# Try specific version
con.execute("INSTALL httpfs FROM 'https://nightly-extensions.duckdb.org'")
```

### Problem: Extension Functions Not Available

**Error**: Extension functions not found after loading

**Solution**:
```python
# Ensure extension is loaded
con.execute("LOAD httpfs")

# Check available functions
con.execute("SELECT * FROM duckdb_functions() WHERE function_name LIKE 'read_%'").fetchall()

# Restart connection after loading extension
con.close()
con = duckdb.connect('database.db')
con.execute("LOAD httpfs")
```

## 🆘 General Debugging

### Enable Debug Logging

```python
import duckdb
import logging

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Connect with debug enabled
con = duckdb.connect('database.db', config={'log_level': 'debug'})
```

### Check DuckDB Version

```python
import duckdb
print(f"DuckDB version: {duckdb.__version__}")

# Check for known issues with your version
# https://github.com/duckdb/duckdb/releases
```

### Verify Sample Data Integrity

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Check all tables
tables = con.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

# Check row counts
for table in tables:
    count = con.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
    print(f"{table[0]}: {count} rows")

# Check for data corruption
con.execute("CHECKPOINT").fetchall()
```

## 📚 Getting Additional Help

### Community Resources

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share insights
- **DuckDB Discord**: Real-time community support
- **Stack Overflow**: Search for similar issues

### Documentation

- [DuckDB Documentation](https://duckdb.org/docs/)
- [Python API Reference](https://duckdb.org/docs/api/python/)
- [SQL Reference](https://duckdb.org/docs/sql/)

### Project-Specific Help

- **Lab Guides**: Check specific lab documentation
- **Solution Notebooks**: Reference solutions in `solutions/` directory
- **Setup Guide**: [Setup Guide](../docs/SETUP_GUIDE.md)
- **README**: [Project README](../README.md)

---

**Still stuck? Open a GitHub issue with details about your problem and environment.**