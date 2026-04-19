<!--
SEO Metadata
Title: DuckDB Code Practice - Free Hands-on Labs for Modern Analytics Learning
Description: Master DuckDB with free, vendor-independent hands-on labs. Practice SQL analytics, extensions, parquet, and modern data patterns with real-world exercises.
Keywords: duckdb, sql analytics, data analytics, parquet, arrow, python, pandas, data engineering, olap, columnar database, open source data
Author: DuckDB Code Practice Community
-->

# DuckDB Code Practice

## 🎯 Educational Mission

A comprehensive, vendor-independent DuckDB learning environment designed for developers, data engineers, and analysts who want to master modern in-memory SQL analytics through hands-on practice.

**10 progressive labs with 80+ exercises. Completely free and open source. Built for learners, by learners.**

## 🎓 Why This Repository?

This educational resource fills the gap between theoretical knowledge and practical skills in DuckDB and modern analytics technologies:

- **Learn by Doing**: Progressive hands-on labs build real skills
- **Vendor Independent**: Master concepts that apply across all platforms
- **Production Patterns**: Learn best practices used in real analytics workflows
- **Multi-Language Experience**: Work with Python, SQL, and command-line interfaces
- **Community Driven**: Built and improved by the analytics community

## 🎓 Learning Approach

### Progressive Complexity

Our labs are designed to build knowledge progressively:

- **Beginner (Labs 0-2)**: Foundation and basic operations
- **Intermediate (Labs 3-6)**: Advanced features and optimization
- **Advanced (Labs 7-9)**: Production patterns and integration

### Hands-On Learning

Each lab includes:
- **Clear Learning Objectives**: Know what you'll achieve
- **Step-by-Step Instructions**: Guided exercises
- **Real-World Scenarios**: Practical use cases
- **Solution Notebooks**: Reference implementations
- **Conceptual Guides**: Deep-dive explanations

### Multi-Language Experience

Gain experience with different interfaces:
- **Python API**: Programmatic access with duckdb package
- **SQL Shell**: Interactive SQL command-line interface
- **Jupyter Notebooks**: Interactive analysis environment
- **CLI Tools**: Command-line utilities for data processing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DuckDB Code Practice                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         DuckDB Core Engine                           │  │
│  │         - In-memory OLAP database                   │  │
│  │         - Columnar storage format                   │  │
│  │         - SQL query engine                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Client Interfaces                           │  │
│  │         - Python API (duckdb package)              │  │
│  │         - SQL Shell (duckdb command)               │  │
│  │         - Jupyter Integration                      │  │
│  │         - CLI Tools                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Formats & Extensions                    │  │
│  │         - Parquet files                             │  │
│  │         - Apache Arrow                              │  │
│  │         - CSV/JSON                                  │  │
│  │         - Extension ecosystem                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Integration Layer                            │  │
│  │         - Pandas integration                        │  │
│  │         - Polars integration                        │  │
│  │         - Data frame conversion                      │  │
│  │         - External database connectors              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Core Stack

### Database Engine
- **DuckDB**: In-memory SQL OLAP database
- Columnar storage for analytical queries
- Zero-copy integration with Arrow

### Data Formats
- **Parquet**: Columnar storage format
- **Apache Arrow**: In-memory columnar format
- **CSV/JSON**: Common data interchange formats

### Client Interfaces
- **Python**: duckdb package for programmatic access
- **SQL Shell**: Interactive command-line interface
- **Jupyter**: Notebook integration for interactive analysis
- **CLI Tools**: Command-line utilities for data processing

### Extensions
- **httpfs**: HTTP filesystem support for remote data
- **parquet**: Advanced Parquet functionality
- **json**: Enhanced JSON support
- **spatial**: Geospatial data processing

## 🎓 Lab Structure

### Lab Difficulty & Time Estimates

| Level | Labs | Time per Lab | What It Tests |
|-------|------|--------------|---------------|
| Beginner | Labs 0-2 | 30-45 min | Basic setup, SQL operations, fundamental concepts |
| Intermediate | Labs 3-6 | 45-60 min | Advanced features, optimization patterns, real-world scenarios |
| Advanced | Labs 7-9 | 60-90 min | Performance analysis, extensions, integration patterns |

### Lab 0: Sample Database Setup
- Generate and load realistic business data
- Explore sample database schema and relationships
- Practice queries on sample data
- **Prerequisite for all subsequent labs**

### Lab 1: Environment Setup
- Install DuckDB and dependencies
- Test database connectivity
- Validate Python API setup
- Explore different interfaces

### Lab 2: Basic DuckDB Operations
- Create databases and tables
- Insert and query data
- Understand SQL basics in DuckDB
- Work with different data types

### Lab 3: Advanced DuckDB Features
- Window functions and analytics
- Complex joins and aggregations
- Subqueries and CTEs
- Data type conversions

### Lab 4: DuckDB + Python Integration
- Python API usage
- Pandas integration
- Data frame operations
- Transaction handling

### Lab 5: Data Format Operations
- Parquet file operations
- CSV/JSON processing
- Apache Arrow integration
- Data format conversions

### Lab 6: Performance & Optimization
- Query optimization techniques
- Index usage and performance
- Memory management
- Query execution analysis

### Lab 7: Extensions & Advanced Features
- HTTP filesystem extension
- Spatial data processing
- JSON extensions
- Custom functions

### Lab 8: Real-world Data Patterns
- ETL patterns with DuckDB
- Data cleaning and validation
- Slowly Changing Dimensions
- Batch processing patterns

### Lab 9: Integration & Production
- Integration with external databases
- Production deployment patterns
- Monitoring and logging
- Error handling and recovery

## 💾 Sample Database

The environment includes a comprehensive sample database with realistic business data for hands-on learning:

### Sample Tables
- **sample_customers** (1,000 records): Customer dimension with segmentation
- **sample_products** (200 records): Product catalog with categories
- **sample_orders** (5,000 records): Order fact table with status tracking
- **sample_transactions** (10,000 records): Transaction details with payment methods
- **sample_events** (20,000 records): Web events for user engagement analysis

### Loading Sample Data
```bash
# Generate and load sample data
python3 scripts/generate_sample_data.py
python3 scripts/load_sample_data.py
```

### Sample Data Documentation
- [Sample Database Guide](docs/SAMPLE_DATABASE.md) - Complete schema and usage documentation
- [Lab 0: Sample Database Setup](labs/lab-00-sample-database.md) - Step-by-step loading and exploration

## 🚀 Quick Start

### 🎓 New to DuckDB?

Follow our recommended learning path:

1. **Start with Fundamentals**: Read [DuckDB Fundamentals](https://github.com/nellaivijay/duckdb-code-practice/wiki/DuckDB-Fundamentals) wiki page
2. **Set Up Environment**: Follow [Getting Started Guide](https://github.com/nellaivijay/duckdb-code-practice/wiki/Getting-Started)
3. **Begin Lab 0**: Load sample data with [Lab 0](https://github.com/nellaivijay/duckdb-code-practice/blob/main/labs/lab-00-sample-database.md)
4. **Progress Through Labs**: Follow the [Learning Path](https://github.com/nellaivijay/duckdb-code-practice/wiki/Learning-Path)

### 📋 Setup Options

### Option 1: Python Environment (Recommended)
```bash
cd duckdb-code-practice
pip install -r requirements.txt
python3 scripts/setup.py
```

### Option 2: Docker Environment
```bash
cd duckdb-code-practice
docker-compose up -d
```

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended)
- 2GB disk space minimum

## 🔧 Configuration

### Python Environment Setup
```bash
# Install dependencies
pip install duckdb pandas jupyter

# Install optional extensions
pip install duckdb-httpfs duckdb-spatial
```

### DuckDB Configuration
```python
# Configure DuckDB settings
import duckdb
con = duckdb.connect()
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=4")
```

## 📚 Documentation

### 🎓 Educational Resources

**Wiki Guides** (Comprehensive learning materials):
- [Wiki Home](https://github.com/nellaivijay/duckdb-code-practice/wiki) - Main wiki page with all guides
- [Getting Started Guide](https://github.com/nellaivijay/duckdb-code-practice/wiki/Getting-Started) - Complete setup and first steps
- [DuckDB Fundamentals](https://github.com/nellaivijay/duckdb-code-practice/wiki/DuckDB-Fundamentals) - Core concepts and architecture
- [Lab Guides](https://github.com/nellaivijay/duckdb-code-practice/wiki/Lab-Guides) - Detailed lab walkthroughs
- [Learning Path](https://github.com/nellaivijay/duckdb-code-practice/wiki/Learning-Path) - Recommended learning sequence
- [Best Practices](https://github.com/nellaivijay/duckdb-code-practice/wiki/Best-Practices) - Production-ready patterns
- [Troubleshooting](https://github.com/nellaivijay/duckdb-code-practice/wiki/Troubleshooting) - Common issues and solutions

### Core Documentation
- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed setup instructions for Python and Docker
- [Architecture Overview](docs/ARCHITECTURE.md) - System architecture and component details
- [Lab Guide](docs/LAB_GUIDE.md) - Complete lab sequence and learning path
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Pages Setup](docs/GITHUB_PAGES_SETUP.md) - Documentation deployment guide
- [Wiki Setup](docs/WIKI_SETUP.md) - Wiki contribution and maintenance guide

### 🎓 Conceptual Guides (Tutorials)
Deep-dive tutorials explaining the "Why" behind the "How":

- [Conceptual Guide 1: DuckDB Architecture](docs/conceptual-guides/01-duckdb-architecture.md) - Understanding DuckDB's architecture and design
- [Conceptual Guide 2: SQL Operations & Data Types](docs/conceptual-guides/02-sql-operations-data-types.md) - SQL operations and DuckDB data types
- [Conceptual Guide 3: Python Integration](docs/conceptual-guides/03-python-integration.md) - Python API and pandas integration
- [Conceptual Guide 4: Data Format Operations](docs/conceptual-guides/04-data-format-operations.md) - Parquet, Arrow, and format conversions
- [Conceptual Guide 5: Performance & Optimization](docs/conceptual-guides/05-performance-optimization.md) - Query optimization and performance tuning
- [Conceptual Guide 6: Extensions & Advanced Features](docs/conceptual-guides/06-extensions-advanced-features.md) - Extension ecosystem and advanced capabilities
- [Conceptual Guide 7: Real-World Data Patterns](docs/conceptual-guides/07-real-world-patterns.md) - ETL patterns and data processing workflows
- [Conceptual Guide 8: Integration & Production](docs/conceptual-guides/08-integration-production.md) - Production deployment and integration patterns

### Lab Materials
- [Lab 0: Sample Database Setup](labs/lab-00-sample-database.md) - Generate and load sample data
- [Lab 1: Environment Setup](labs/lab-01-setup.md) - Component verification and first DuckDB query
- [Lab 2: Basic Operations](labs/lab-02-basic-operations.md) - Tables, queries, data types
- [Lab 3: Advanced Features](labs/lab-03-advanced-features.md) - Window functions, joins, aggregations
- [Lab 4: Python Integration](labs/lab-04-python-integration.md) - Python API and pandas integration
- [Lab 5: Data Format Operations](labs/lab-05-data-format-operations.md) - Parquet, Arrow, format conversions
- [Lab 6: Performance & Optimization](labs/lab-06-performance-optimization.md) - Query optimization and performance analysis
- [Lab 7: Extensions & Advanced Features](labs/lab-07-extensions-advanced-features.md) - Extensions and advanced capabilities
- [Lab 8: Real-World Data Patterns](labs/lab-08-real-world-patterns.md) - ETL patterns and data processing
- [Lab 9: Integration & Production](labs/lab-09-integration-production.md) - Production deployment and integration

### 💡 Jupyter Notebooks
Interactive Jupyter notebooks for hands-on learning:

- [Lab Notebooks](notebooks/) - Student notebooks with exercises
- [Solution Helper](notebooks/SOLUTION_HELPER_INSTRUCTIONS.md) - How to use the solution helper when stuck

### 🔧 Solutions Framework
Complete solution notebooks for reference and validation:

- [Lab 1 Solution](solutions/lab-01-setup-solution.ipynb) - Environment setup solution
- [Lab 2 Solution](solutions/lab-02-basic-operations-solution.ipynb) - Basic operations solution
- [Lab 3 Solution](solutions/lab-03-advanced-features-solution.ipynb) - Advanced features solution
- [Lab 4 Solution](solutions/lab-04-python-integration-solution.ipynb) - Python integration solution
- [Lab 5 Solution](solutions/lab-05-data-format-operations-solution.ipynb) - Data format operations solution
- [Lab 6 Solution](solutions/lab-06-performance-optimization-solution.ipynb) - Performance optimization solution
- [Lab 7 Solution](solutions/lab-07-extensions-advanced-features-solution.ipynb) - Extensions solution
- [Lab 8 Solution](solutions/lab-08-real-world-patterns-solution.ipynb) - Real-world patterns solution
- [Lab 9 Solution](solutions/lab-09-integration-production-solution.ipynb) - Integration solution

### 🤖 Automation Scripts
- [Solution Helper](scripts/solution_helper.py) - Python helper for accessing solutions and hints
- [Validate Solutions](scripts/validate_solutions.sh) - CI/CD validation script for solution notebooks
- [Convert Labs to Notebooks](scripts/convert_labs_to_notebooks.py) - Convert Markdown labs to Jupyter notebooks
- [Generate Sample Data](scripts/generate_sample_data.py) - Generate realistic business data
- [Load Sample Data](scripts/load_sample_data.py) - Load sample data into DuckDB

## 🆘 Vendor Independence

This environment uses only MIT-licensed tools:
- DuckDB (MIT)
- Python packages (various open source licenses)
- Jupyter (BSD)
- Pandas (BSD)
- Apache Arrow (Apache 2.0)

No proprietary cloud services or consoles required.

## 🤝 Contributing

This is a practice environment for learning. Feel free to extend labs, add examples, or improve the setup process.

> **Disclaimer**: This is an independent educational resource for learning DuckDB and modern analytics concepts. It is not affiliated with, endorsed by, or sponsored by DuckDB or any vendor.

## 👥 Community and Learning

This repository is an open educational resource built for the data analytics community. We believe in learning together and sharing knowledge.

### 🤝 Learning Together

- **📖 Comprehensive Wiki**: Detailed guides and tutorials for all skill levels
- **💬 GitHub Discussions**: Ask questions and share insights with fellow learners
- **🐛 Issue Tracking**: Report bugs and suggest improvements
- **🔄 Pull Requests**: Contribute labs, fixes, and enhancements
- **⭐ Star the Repo**: Show your support and help others discover this resource

### 🎓 Contributing to Learning

We welcome contributions that improve the educational value:
- **New Labs**: Suggest new lab topics and exercises
- **Better Explanations**: Improve clarity of existing content
- **Additional Examples**: Add more practical examples
- **Translation**: Help translate content for global learners
- **Bug Fixes**: Report and fix issues in labs or documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### 📚 Additional Learning Resources

- **Official DuckDB Documentation**: [https://duckdb.org/docs/](https://duckdb.org/docs/)
- **DuckDB Blog**: Latest updates and articles
- **Conference Talks**: Learn from industry experts

## 📄 License

MIT License