# Learning Path

This guide provides a structured learning path to master DuckDB through the DuckDB Code Practice repository.

## 🎯 Overview

The learning path consists of 15 comprehensive labs that cover DuckDB from fundamentals through production deployment, aligned with comprehensive DuckDB learning curriculum. Each lab includes:

- Clear learning objectives
- Step-by-step instructions
- Hands-on exercises
- Expected outcomes
- Troubleshooting guidance

## 📊 Lab Structure

### Beginner Level (Labs 0-2)
**Focus**: Foundation, introduction, and basic operations
**Time**: 30-60 minutes per lab
**Prerequisites**: Basic Python knowledge

### Intermediate Level (Labs 3-6)
**Focus**: Advanced features, data exploration, and optimization
**Time**: 45-75 minutes per lab
**Prerequisites**: Complete beginner labs

### Advanced Level (Labs 7-10)
**Focus**: Cloud integration, pipelines, applications, and client APIs
**Time**: 60-120 minutes per lab
**Prerequisites**: Complete intermediate labs

## 🎓 Detailed Learning Path

### Phase 1: Foundation (Beginner)

#### Lab 0: Sample Database Setup
**🎯 Learning Objectives**
- Generate realistic sample data
- Load data into DuckDB
- Understand sample database schema
- Practice basic queries

**⏱️ Time**: 20-30 minutes
**📋 Prerequisites**: Python 3.8+, DuckDB installed
**🚀 Start**: [Lab 0 Guide](../labs/lab-00-sample-database.md)

**Key Concepts**:
- Sample data generation
- Database schema design
- Data loading strategies
- Basic SQL queries

**Success Criteria**:
- ✅ Sample data generated and loaded
- ✅ Can query all sample tables
- ✅ Understand database schema

---

#### Lab 1: Environment Setup
**🎯 Learning Objectives**
- Verify DuckDB installation
- Test database connectivity
- Explore different interfaces
- Validate Jupyter setup

**⏱️ Time**: 30-45 minutes
**📋 Prerequisites**: Lab 0 completed
**🚀 Start**: [Lab 1 Guide](../labs/lab-01-setup.md)

**Key Concepts**:
- Python API usage
- SQL shell interface
- Jupyter integration
- Configuration options

**Success Criteria**:
- ✅ All interfaces working
- ✅ Can connect to databases
- ✅ Understand connection modes

---

#### Lab 2: Basic Operations (Chapter 3)
**🎯 Learning Objectives**
- Create and manage databases using DDL
- Perform CRUD operations using DML
- Understand data types and functions
- Practice DuckDB-specific SQL extensions
- Execute SQL queries and understand results

**⏱️ Time**: 45-60 minutes
**📋 Prerequisites**: Lab 1 completed
**🚀 Start**: [Lab 2 Guide](../labs/lab-02-basic-operations.md)

**Key Concepts**:
- Table creation and modification
- Data insertion and querying
- DuckDB SQL extensions
- Basic SQL operations

**Success Criteria**:
- ✅ Can create tables
- ✅ Can perform CRUD operations
- ✅ Understand DuckDB data types

---

#### Lab 1A: Introduction to DuckDB (Chapter 1)
**🎯 Learning Objectives**
- Understand what DuckDB is and its characteristics
- Learn when to use DuckDB vs. other databases
- Explore DuckDB's place in the data ecosystem
- Understand the complete data processing flow
- Practice DuckDB-specific SQL extensions

**⏱️ Time**: 45-60 minutes
**📋 Prerequisites**: Lab 0 completed
**🚀 Start**: [Lab 1A Guide](../labs/lab-01a-introduction.md)

**Key Concepts**:
- DuckDB fundamentals and architecture
- Data processing flow
- Use case analysis
- SQL extensions
- Performance characteristics

**Success Criteria**:
- ✅ Understand DuckDB's role in analytics
- ✅ Know when to use DuckDB
- ✅ Understand data processing pipeline
- ✅ Can use DuckDB-specific SQL features

---

### Phase 2: Intermediate Skills

#### Lab 3: Advanced Features (Chapter 4)
**🎯 Learning Objectives**
- Window functions and analytical queries
- Advanced aggregation and grouping sets
- Complex subqueries and CTEs
- PIVOT operations and ASOF joins
- LATERAL joins and table functions
- FILTER, QUALIFY, and HAVING clauses

**⏱️ Time**: 60-75 minutes
**📋 Prerequisites**: Lab 2 completed
**🚀 Start**: [Lab 3 Guide](../labs/lab-03-advanced-features.md)

**Key Concepts**:
- Analytical functions
- Advanced SQL patterns
- Join strategies
- Query optimization

**Success Criteria**:
- ✅ Can write complex queries
- ✅ Understand window functions
- ✅ Can optimize queries

---

#### Lab 4: Python Integration (Chapter 6)
**🎯 Learning Objectives**
- Python API deep dive
- Pandas and NumPy integration
- User-defined functions (UDFs)
- Apache Arrow and Polars interoperability
- Data processing pipelines

**⏱️ Time**: 60-75 minutes
**📋 Prerequisites**: Lab 3 completed
**🚀 Start**: [Lab 4 Guide](../labs/lab-04-python-integration.md)

**Key Concepts**:
- Python-DuckDB integration
- Pandas interoperability
- Data processing pipelines
- Error handling

**Success Criteria**:
- ✅ Proficient with Python API
- ✅ Can integrate with pandas
- ✅ Understand transactions

---

#### Lab 5: Data Format Operations
**🎯 Learning Objectives**
- Parquet file operations
- CSV/JSON processing
- Arrow integration
- Format conversions

**⏱️ Time**: 45-60 minutes
**📋 Prerequisites**: Lab 4 completed
**🚀 Start**: [Lab 5 Guide](../labs/lab-05-data-format-operations.md)

**Key Concepts**:
- Parquet operations
- Arrow format
- Data format conversion
- File system operations

**Success Criteria**:
- ✅ Can work with Parquet
- ✅ Understand Arrow format
- ✅ Can convert between formats

---

#### Lab 5A: Exploring Data Without Persistence (Chapter 5)
**🎯 Learning Objectives**
- Query data files directly without creating tables
- Automatic file type and schema inference
- Shred nested JSON structures
- Convert between data formats
- Query Parquet files directly
- Access SQLite and other databases
- Work with Excel files

**⏱️ Time**: 60-75 minutes
**📋 Prerequisites**: Lab 4 completed
**🚀 Start**: [Lab 5A Guide](../labs/lab-05a-exploring-data.md)

**Key Concepts**:
- Direct file queries
- Schema inference
- JSON shredding
- Format conversion
- Cross-database queries

**Success Criteria**:
- ✅ Can query files directly
- ✅ Understand schema inference
- ✅ Can work with nested data
- ✅ Can convert between formats

---

#### Lab 6: Performance & Optimization (Chapter 10)
**🎯 Learning Objectives**
- Query execution plan analysis with EXPLAIN
- Index strategies and performance tuning
- Memory and thread configuration optimization
- Loading and querying large datasets
- Export data to Parquet for performance
- S3 integration and cloud data access

**⏱️ Time**: 60-75 minutes
**📋 Prerequisites**: Lab 5A completed
**🚀 Start**: [Lab 6 Guide](../labs/lab-06-performance-optimization.md)

**Key Concepts**:
- Query execution plans
- Index strategies
- Memory configuration
- Performance tuning
- Large dataset handling

**Success Criteria**:
- ✅ Can optimize queries
- ✅ Understand execution plans
- ✅ Can configure for performance

---

### Phase 3: Advanced Production

#### Lab 7: Extensions & Advanced Features
**🎯 Learning Objectives**
- HTTP filesystem extension
- Spatial data processing
- JSON extensions
- Custom functions

**⏱️ Time**: 60-90 minutes
**📋 Prerequisites**: Lab 6 completed
**🚀 Start**: [Lab 7 Guide](../labs/lab-07-extensions-advanced-features.md)

**Key Concepts**:
- Extension ecosystem
- Remote data access
- Geospatial processing
- Advanced JSON operations

**Success Criteria**:
- ✅ Can use extensions
- ✅ Can access remote data
- ✅ Understand extension system

---

#### Lab 7: DuckDB in the Cloud with MotherDuck (Chapter 7)
**🎯 Learning Objectives**
- Introduction to MotherDuck and its architecture
- Set up and configure MotherDuck account
- Connect to MotherDuck using CLI and token authentication
- Upload and manage databases in the cloud
- Share databases with collaborators
- Configure S3 secrets and load data from S3
- Optimize data ingestion and usage
- Query data with AI assistance
- Explore MotherDuck integrations

**⏱️ Time**: 75-90 minutes
**📋 Prerequisites**: Lab 6 completed
**🚀 Start**: [Lab 7 Guide](../labs/lab-07-motherduck.md)

**Key Concepts**:
- Cloud database management
- Token-based authentication
- S3 integration
- Data sharing
- AI-assisted querying

**Success Criteria**:
- ✅ Can use MotherDuck
- ✅ Understand cloud data management
- ✅ Can integrate with S3
- ✅ Can share databases

---

#### Lab 8: Real-World Data Patterns
**🎯 Learning Objectives**
- ETL patterns
- Data cleaning
- Slowly Changing Dimensions
- Batch processing

**⏱️ Time**: 60-90 minutes
**📋 Prerequisites**: Lab 7 completed
**🚀 Start**: [Lab 8 Guide](../labs/lab-08-real-world-patterns.md)

**Key Concepts**:
- ETL workflows
- Data quality
- Dimensional modeling
- Production patterns

**Success Criteria**:
- ✅ Can build ETL pipelines
- ✅ Understand data patterns
- ✅ Can handle real-world scenarios

---

#### Lab 8A: Building Data Pipelines (Chapter 8)
**🎯 Learning Objectives**
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

**⏱️ Time**: 90-120 minutes
**📋 Prerequisites**: Lab 7 completed
**🚀 Start**: [Lab 8A Guide](../labs/lab-08a-data-pipelines.md)

**Key Concepts**:
- Modern data stack (dlt, dbt, Dagster)
- Pipeline orchestration
- Data transformation
- Cloud integration
- Pipeline monitoring

**Success Criteria**:
- ✅ Can build data pipelines
- ✅ Understand modern data stack
- ✅ Can orchestrate workflows
- ✅ Can integrate with cloud

---

#### Lab 9: Integration & Production
**🎯 Learning Objectives**
- External database integration
- Production deployment
- Monitoring and logging
- Error handling

**⏱️ Time**: 60-90 minutes
**📋 Prerequisites**: Lab 8A completed
**🚀 Start**: [Lab 9 Guide](../labs/lab-09-integration-production.md)

**Key Concepts**:
- Database integration
- Deployment strategies
- Monitoring practices
- Production considerations

**Success Criteria**:
- ✅ Can integrate with other systems
- ✅ Understand deployment options
- ✅ Can monitor DuckDB operations

---

#### Lab 9: Building and Deploying Data Apps (Chapter 9)
**🎯 Learning Objectives**
- Build custom data apps with Streamlit
- Use Streamlit components for enhanced functionality
- Visualize data using plotly
- Deploy Streamlit apps on Community Cloud
- Build BI dashboards with Apache Superset
- Create datasets from SQL queries
- Export and import Superset dashboards
- Integrate DuckDB with both tools

**⏱️ Time**: 90-120 minutes
**📋 Prerequisites**: Lab 8A completed
**🚀 Start**: [Lab 9 Guide](../labs/lab-09-data-apps.md)

**Key Concepts**:
- Streamlit app development
- Data visualization
- Dashboard creation
- Cloud deployment
- BI tool integration

**Success Criteria**:
- ✅ Can build data apps
- ✅ Can create dashboards
- ✅ Can deploy applications
- ✅ Can integrate with BI tools

---

#### Lab 10: Client APIs for DuckDB (Appendix)
**🎯 Learning Objectives**
- Overview of officially supported languages
- Concurrency considerations and best practices
- Importing large amounts of data efficiently
- Using DuckDB from Java via JDBC Driver
- Multi-threaded access patterns
- Data processing from Java
- Additional connection options and configuration
- Cross-language API comparison

**⏱️ Time**: 75-90 minutes
**📋 Prerequisites**: Lab 9 completed
**🚀 Start**: [Lab 10 Guide](../labs/lab-10-client-apis.md)

**Key Concepts**:
- Multi-language support
- JDBC integration
- Concurrency patterns
- Performance optimization
- Cross-language comparison

**Success Criteria**:
- ✅ Understand different client APIs
- ✅ Can use JDBC driver
- ✅ Understand concurrency
- ✅ Can optimize performance

---

## 📈 Progress Tracking

### Skill Development

Track your progress through these skill areas:

#### Foundation Skills
- [ ] Database setup and configuration
- [ ] Basic SQL operations
- [ ] Data loading and querying
- [ ] Understanding DuckDB architecture

#### Intermediate Skills
- [ ] Complex SQL queries
- [ ] Python integration
- [ ] Data format operations
- [ ] Performance optimization

#### Advanced Skills
- [ ] Extension usage
- [ ] Cloud integration (MotherDuck)
- [ ] Modern data stack (dlt, dbt, Dagster)
- [ ] Data app development (Streamlit, Superset)
- [ ] Multi-language APIs (JDBC, Python, R)
- [ ] Production deployment
- [ ] System integration
- [ ] Monitoring and deployment

### Project Ideas

As you progress, build these projects:

#### After Beginner Labs
- Personal expense tracker
- Book catalog system
- Simple reporting dashboard

#### After Intermediate Labs
- Data warehouse prototype
- Analytics pipeline
- Data conversion tool

#### After Advanced Labs
- Production ETL system with dlt, dbt, and Dagster
- Cloud-based analytics platform with MotherDuck
- Interactive data applications with Streamlit
- Enterprise BI dashboards with Superset
- Multi-language data processing system
- Real-time analytics platform

## 🎯 Certification Readiness

Completing all labs prepares you for:

- **Data Analyst Roles**: SQL and analytics skills
- **Data Engineering Roles**: ETL, pipelines, and cloud skills
- **Data Science Roles**: Python, data processing, and ML preparation
- **BI Developer Roles**: Dashboard and visualization skills
- **Full Stack Data Roles**: End-to-end data application development
- **Cloud Data Roles**: Cloud database and integration skills

## 🆘 Support

### Getting Stuck

1. **Review Lab Documentation**: Each lab has detailed instructions
2. **Check Troubleshooting Guide**: [Troubleshooting](Troubleshooting.md)
3. **Use Solution Notebooks**: Reference solutions in `solutions/` directory
4. **Ask Community**: GitHub Discussions for help

### Best Practices

- **Complete Labs in Order**: Each builds on previous knowledge
- **Practice Regularly**: Consistent practice reinforces learning
- **Build Projects**: Apply skills to real projects
- **Share Knowledge**: Help others learn

## 📚 Additional Resources

### Official Documentation
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Python API Reference](https://duckdb.org/docs/api/python/)
- [SQL Reference](https://duckdb.org/docs/sql/)

### Community
- [DuckDB Discord](https://discord.gg/duckdb)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/duckdb)
- [GitHub Discussions](https://github.com/duckdb/duckdb/discussions)

---

**Ready to start? Begin with [Lab 0: Sample Database Setup](../labs/lab-00-sample-database.md)!**