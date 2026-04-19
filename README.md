<!--
SEO Metadata
Title: DuckDB Code Practice - Free Hands-on Labs for Lakehouse Analytics
Description: Master DuckDB and lakehouse architecture with free, vendor-independent hands-on labs. Practice SQL analytics, ETL patterns, data engineering, and modern data lakehouse concepts with real-world exercises.
Keywords: duckdb, lakehouse, data lakehouse, sql analytics, data analytics, parquet, arrow, python, pandas, data engineering, olap, columnar database, open source data, ETL, data quality, production readiness
Author: DuckDB Code Practice Community
-->

# DuckDB Code Practice

## 🎯 Educational Mission

A comprehensive, vendor-independent DuckDB learning environment designed for developers, data engineers, and analysts who want to master modern in-memory SQL analytics and lakehouse architecture through hands-on practice.

**15 comprehensive labs with 120+ exercises covering DuckDB fundamentals through production deployment. Aligned with comprehensive DuckDB learning curriculum. Completely free and open source. Built for learners, by learners.**

## 🎓 Why This Repository?

This educational resource fills the gap between theoretical knowledge and practical skills in DuckDB, lakehouse architecture, and modern analytics technologies:

- **Learn by Doing**: Progressive hands-on labs build real skills
- **Vendor Independent**: Master concepts that apply across all platforms
- **Lakehouse Focus**: Learn modern data lakehouse architecture patterns
- **Production Patterns**: Learn ETL, data quality, and production operations
- **Multi-Language Experience**: Work with Python, SQL, and command-line interfaces
- **Community Driven**: Built and improved by the analytics community

## 🎓 Learning Approach

### Progressive Complexity

Our labs are designed to build knowledge progressively:

- **Beginner (Labs 0-2)**: Foundation, introduction, and basic operations
- **Intermediate (Labs 3-6)**: Advanced features, data exploration, and optimization
- **Advanced (Labs 7-10)**: Cloud integration, pipelines, applications, and client APIs

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
│                   Lakehouse Learning Environment            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Lakehouse Architecture Layers               │  │
│  │         - Bronze: Raw data ingestion               │  │
│  │         - Silver: Cleaned & validated              │  │
│  │         - Gold: Business-ready aggregates          │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
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
│  │         - Parquet files (lakehouse standard)        │  │
│  │         - Apache Arrow (zero-copy)                 │  │
│  │         - CSV/JSON (interchange)                   │  │
│  │         - Extension ecosystem                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Production Operations                       │  │
│  │         - ETL pipelines                             │  │
│  │         - Data quality frameworks                   │  │
│  │         - Monitoring & alerting                     │  │
│  │         - Backup & recovery                        │  │
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
| Beginner | Labs 0-2 | 30-60 min | Basic setup, introduction, SQL operations, fundamental concepts |
| Intermediate | Labs 3-6 | 45-75 min | Advanced features, data exploration, optimization patterns |
| Advanced | Labs 7-10 | 60-120 min | Cloud integration, pipelines, applications, client APIs |

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

### Lab 1A: Introduction to DuckDB (Chapter 1)
- Understand what DuckDB is and its characteristics
- Learn when to use DuckDB vs. other databases
- Explore DuckDB's place in the data ecosystem
- Understand the complete data processing flow
- Practice DuckDB-specific SQL extensions

### Lab 2: Basic DuckDB Operations (Chapter 3)
- Create databases and tables using DDL
- Insert, update, and delete data using DML
- Execute SQL queries and understand results
- Work with different data types and functions
- Practice DuckDB-specific SQL extensions

### Lab 3: Advanced Features (Chapter 4)
- Window functions and analytical queries
- Advanced aggregation and grouping sets
- Complex subqueries and CTEs
- PIVOT operations and ASOF joins
- LATERAL joins and table functions
- FILTER, QUALIFY, and HAVING clauses

### Lab 4: DuckDB + Python Integration (Chapter 6)
- Deep dive into Python API for programmatic access
- Seamless pandas and NumPy integration
- User-defined functions (UDFs) in Python
- Apache Arrow and Polars interoperability
- Building data processing pipelines

### Lab 5: Data Format Operations
- Parquet file operations for lakehouse storage
- Apache Arrow integration for zero-copy operations
- CSV/JSON processing and conversion
- Data format optimization strategies

### Lab 5A: Exploring Data Without Persistence (Chapter 5)
- Query data files directly without creating tables
- Automatic file type and schema inference
- Shred nested JSON structures
- Convert between data formats (CSV to Parquet)
- Query Parquet files directly
- Access SQLite and other databases
- Work with Excel files

### Lab 6: Performance & Optimization (Chapter 10)
- Query execution plan analysis with EXPLAIN
- Index strategies and performance tuning
- Memory and thread configuration optimization
- Loading and querying large datasets (Stack Overflow, NYC Taxi)
- Export data to Parquet for performance
- S3 integration and cloud data access

### Lab 7: Extensions & Advanced Features
- HTTP filesystem for remote data lake access
- Spatial data processing and analysis
- Advanced JSON operations for semi-structured data
- Custom functions and UDFs for business logic

### Lab 7: DuckDB in the Cloud with MotherDuck (Chapter 7)
- Introduction to MotherDuck and its architecture
- Set up and configure MotherDuck account
- Connect to MotherDuck using CLI and token authentication
- Upload and manage databases in the cloud
- Share databases with collaborators
- Configure S3 secrets and load data from S3
- Optimize data ingestion and usage
- Query data with AI assistance
- Explore MotherDuck integrations

### Lab 8: Real-World Use Cases and Patterns
- ETL pipeline implementation with error handling
- Data quality frameworks and validation
- Slowly Changing Dimensions (SCD) implementation
- Batch processing workflows

### Lab 8A: Building Data Pipelines (Chapter 8)
- Data ingestion with dlt (Data Loading Tool)
- Set up and configure dlt pipelines
- Explore pipeline metadata and monitoring
- Data transformation with dbt (data build tool)
- Set up dbt projects with DuckDB
- Define sources, models, and transformations
- Test transformations and pipelines
- Orchestrate data pipelines with Dagster
- Define assets and dependencies
- Run and monitor Dagster pipelines
- Upload processed data to MotherDuck

### Lab 9: Integration and Production Readiness
- External database and system integration
- Production deployment strategies (Docker/Kubernetes)
- Monitoring, alerting, and health checks
- Backup, recovery, and disaster procedures
- Security implementation and access control

### Lab 9: Building and Deploying Data Apps (Chapter 9)
- Build custom data apps with Streamlit
- Use Streamlit components for enhanced functionality
- Visualize data using plotly
- Deploy Streamlit apps on Community Cloud
- Build BI dashboards with Apache Superset
- Create datasets from SQL queries
- Export and import Superset dashboards
- Integrate DuckDB with both tools

### Lab 10: Client APIs for DuckDB (Appendix)
- Overview of officially supported languages
- Concurrency considerations and best practices
- Importing large amounts of data efficiently
- Using DuckDB from Java via JDBC Driver
- Multi-threaded access patterns
- Data processing from Java
- Additional connection options and configuration
- Cross-language API comparison

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
- [Lakehouse Architecture](docs/LAKEHOUSE_ARCHITECTURE.md) - Lakehouse concepts and DuckDB integration
- [Operations Guide](docs/OPERATIONS_GUIDE.md) - Production operations and readiness
- [Lab Guide](docs/LAB_GUIDE.md) - Complete lab sequence and learning path
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Pages Setup](docs/GITHUB_PAGES_SETUP.md) - Documentation deployment guide
- [Wiki Setup](docs/WIKI_SETUP.md) - Wiki contribution and maintenance guide

### 🎓 Conceptual Guides (Tutorials)
Deep-dive tutorials explaining the "Why" behind the "How":

- [Lakehouse Architecture](docs/LAKEHOUSE_ARCHITECTURE.md) - Understanding lakehouse patterns and DuckDB's role
- [DuckDB Architecture](docs/ARCHITECTURE.md) - Understanding DuckDB's architecture and design
- [Operations & Production Readiness](docs/OPERATIONS_GUIDE.md) - Production operations and best practices

### Lab Materials
- [Lab 0: Sample Database Setup](labs/lab-00-sample-database.md) - Generate and load sample data
- [Lab 1: Environment Setup](labs/lab-01-setup.md) - Component verification and first DuckDB query
- [Lab 1A: Introduction to DuckDB](labs/lab-01a-introduction.md) - DuckDB fundamentals and ecosystem
- [Lab 2: Basic DuckDB Operations](labs/lab-02-basic-operations.md) - Tables, queries, data types (Chapter 3)
- [Lab 3: Advanced Features](labs/lab-03-advanced-features.md) - Window functions, advanced SQL (Chapter 4)
- [Lab 4: DuckDB + Python Integration](labs/lab-04-python-integration.md) - Python API, pandas, UDFs (Chapter 6)
- [Lab 5: Data Format Operations](labs/lab-05-data-format-operations.md) - Parquet, Arrow, formats
- [Lab 5A: Exploring Data Without Persistence](labs/lab-05a-exploring-data.md) - Direct file queries, JSON shredding (Chapter 5)
- [Lab 6: Performance & Optimization](labs/lab-06-performance-optimization.md) - Query optimization, large datasets (Chapter 10)
- [Lab 7: Extensions & Advanced Features](labs/lab-07-extensions-advanced-features.md) - HTTP filesystem, spatial
- [Lab 7: DuckDB in the Cloud with MotherDuck](labs/lab-07-motherduck.md) - Cloud integration, S3, AI (Chapter 7)
- [Lab 8: Real-World Use Cases and Patterns](labs/lab-08-real-world-patterns.md) - ETL, SCD, production patterns
- [Lab 8A: Building Data Pipelines](labs/lab-08a-data-pipelines.md) - dlt, dbt, Dagster (Chapter 8)
- [Lab 9: Integration and Production Readiness](labs/lab-09-integration-production.md) - Production deployment, monitoring
- [Lab 9: Building and Deploying Data Apps](labs/lab-09-data-apps.md) - Streamlit, Superset (Chapter 9)
- [Lab 10: Client APIs for DuckDB](labs/lab-10-client-apis.md) - Multi-language APIs, JDBC (Appendix)

### 💡 Jupyter Notebooks
Interactive Jupyter notebooks for hands-on learning:

- [Lab Notebooks](notebooks/) - Student notebooks with exercises (coming soon)
- [Solution Helper](notebooks/SOLUTION_HELPER_INSTRUCTIONS.md) - How to use the solution helper when stuck

### 🤖 Automation Scripts
- [Solution Helper](scripts/solution_helper.py) - Python helper for accessing solutions and hints (coming soon)
- [Setup Script](scripts/setup.py) - Environment validation and setup
- [Generate Sample Data](scripts/generate_sample_data.py) - Generate realistic business data
- [Load Sample Data](scripts/load_sample_data.py) - Load sample data into DuckDB

## 🔗 Related Practice Repositories

Continue your learning journey with these related repositories:

### AI/ML Practice
- [🤖 DSPy Code Practice](https://github.com/nellaivijay/dspy-code-practice) - Declarative LLM programming
- [🧠 LLM Fine-Tuning Practice](https://github.com/nellaivijay/llm-fine-tuning-practice) - Model fine-tuning techniques

### Data Engineering Practice
- [⚡ Apache Spark Code Practice](https://github.com/nellaivijay/spark-code-practice) - Big data processing
- [🏔️ Apache Iceberg Code Practice](https://github.com/nellaivijay/iceberg-code-practice) - Lakehouse architecture
- [🔧 Apache Beam Code Practice](https://github.com/nellaivijay/beam-code-practice) - Data pipelines

### Programming Practice
- [⚙️ Scala Data Analysis Practice](https://github.com/nellaivijay/scala-dataanalysis-code-practice) - Functional programming

### Resource Hub
- [📚 Awesome My Notes](https://github.com/nellaivijay/awesome-my-notes) - Comprehensive technical notes and learning resources

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

Apache License 2.0