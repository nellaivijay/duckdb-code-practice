# Lab 10: Client APIs for DuckDB

## 🎯 Learning Objectives

- Understand officially supported DuckDB client languages
- Learn about concurrency considerations in DuckDB
- Explore different use cases for client APIs
- Practice importing large amounts of data efficiently
- Learn to use DuckDB from Java via JDBC Driver
- Understand the general usage pattern for JDBC
- Practice using multiple connections from several threads
- Use DuckDB as a data processing tool from Java
- Practice inserting large amounts of data from Java
- Explore additional connection options
- Compare different client API approaches

## 📋 Prerequisites

- Completed Lab 0: Sample Database Setup
- Completed Lab 1A: Introduction to DuckDB
- Python 3.8+ installed (for Python API examples)
- Java 11+ installed (for JDBC examples)
- Basic understanding of different programming languages

## ⏱️ Estimated Time

75-90 minutes

## 🎓 Conceptual Background

### Officially Supported Languages

DuckDB provides client libraries for multiple programming languages:

**Primary Support:**
- **Python**: `duckdb` package (most mature)
- **Java**: JDBC driver
- **C++**: Native library
- **R**: `duckdb` package
- **Go**: `duckdb` package
- **Node.js**: `duckdb` package

**Experimental/Community Support:**
- **C#:** `.NET` bindings
- **Ruby:** `duckdb` gem
- **Julia:** `DuckDB.jl` package
- **Rust:** `duckdb` crate

### A Word on Concurrency

DuckDB has specific concurrency characteristics:

**Read Operations:**
- Multiple concurrent readers supported
- Read operations don't block each other
- Snapshot isolation for consistent reads

**Write Operations:**
- Single writer at a time (by default)
- Write operations block readers
- Automatic locking and conflict resolution

**Best Practices:**
- Use connection pooling for multiple readers
- Batch write operations for efficiency
- Consider WAL mode for better concurrency
- Use transactions for complex operations

### Use Cases for Different APIs

**Python API:**
- Data science and ML workflows
- Jupyter notebook analysis
- ETL and data processing
- Web applications (Flask, Django, FastAPI)

**Java/JDBC:**
- Enterprise applications
- Spring Boot integration
- Big data processing (Spark, Flink)
- Traditional enterprise systems

**R API:**
- Statistical analysis
- Research and academic work
- Bioinformatics
- Traditional R workflows

**C++ API:**
- High-performance applications
- Game development
- Embedded systems
- Performance-critical applications

## 🚀 Step-by-Step Instructions

### Step 1: Python API Basics

Practice Python API fundamentals:

```python
import duckdb
import pandas as pd
import time

# Connection management
print("=== Python API Basics ===")

# In-memory connection
con_memory = duckdb.connect(':memory:')
print("✓ In-memory connection created")

# Persistent connection
con_persistent = duckdb.connect('data/python_test.db')
print("✓ Persistent connection created")

# Read-only connection
con_readonly = duckdb.connect('data/duckdb_practice.db', read_only=True)
print("✓ Read-only connection created")

# Basic operations
con_persistent.execute("CREATE TABLE test AS SELECT * FROM range(100)")
result = con_persistent.execute("SELECT COUNT(*) FROM test").fetchone()
print(f"✓ Query result: {result[0]} rows")

# DataFrame integration
df = pd.DataFrame({
    'id': range(1, 11),
    'value': [i * 10 for i in range(10)]
})
con_persistent.register('test_df', df)
result = con_persistent.execute("SELECT AVG(value) FROM test_df").fetchone()
print(f"✓ DataFrame integration: Average = {result[0]}")

# Cleanup
con_memory.close()
con_persistent.close()
con_readonly.close()
print("✓ All connections closed")
```

### Step 2: Importing Large Amounts of Data

Practice efficient data import strategies:

```python
import duckdb
import pandas as pd
import numpy as np
import time

print("=== Large Data Import Strategies ===")

con = duckdb.connect('data/large_import.db')

# Method 1: Batch insertion
print("\nMethod 1: Batch Insertion")
start = time.time()
for i in range(10):
    batch_data = pd.DataFrame({
        'id': range(i * 10000, (i + 1) * 10000),
        'value': np.random.rand(10000) * 100,
        'category': np.random.choice(['A', 'B', 'C'], 10000)
    })
    con.register('batch', batch_data)
    con.execute("INSERT INTO large_table SELECT * FROM batch")
    con.execute("DROP TABLE batch")
batch_time = time.time() - start
print(f"✓ Batch insertion: {batch_time:.4f}s")

# Method 2: Direct COPY command
print("\nMethod 2: COPY Command")
con.execute("CREATE TABLE large_table2 AS SELECT * FROM large_table LIMIT 0")
start = time.time()
for i in range(10):
    batch_data = pd.DataFrame({
        'id': range(i * 10000, (i + 1) * 10000),
        'value': np.random.rand(10000) * 100,
        'category': np.random.choice(['A', 'B', 'C'], 10000)
    })
    batch_data.to_csv(f'data/batch_{i}.csv', index=False)
    con.execute(f"COPY large_table2 FROM 'data/batch_{i}.csv' (FORMAT CSV, HEADER)")
copy_time = time.time() - start
print(f"✓ COPY command: {copy_time:.4f}s")

# Method 3: Appender (most efficient for large datasets)
print("\nMethod 3: Appender")
con.execute("CREATE TABLE large_table3 (id INTEGER, value DOUBLE, category VARCHAR)")
start = time.time()
appender = con.appender('large_table3')
for i in range(100000):
    appender.append_row(i, np.random.rand() * 100, np.random.choice(['A', 'B', 'C']))
appender.close()
appender_time = time.time() - start
print(f"✓ Appender: {appender_time:.4f}s")

print(f"\nPerformance comparison:")
print(f"Batch insertion: {batch_time:.4f}s")
print(f"COPY command: {copy_time:.4f}s")
print(f"Appender: {appender_time:.4f}s")
```

### Step 3: Java JDBC Setup

Set up Java environment for DuckDB JDBC:

```bash
# Download DuckDB JDBC driver
# Visit: https://github.com/duckdb/duckdb/releases
# Download the JDBC JAR file

# Or use Maven dependency:
# <dependency>
#     <groupId>org.duckdb</groupId>
#     <artifactId>duckdb-jdbc</artifactId>
#     <version>0.9.0</version>
# </dependency>
```

### Step 4: Understanding General Usage Pattern (Java)

Learn the general JDBC pattern for DuckDB:

```java
import java.sql.*;

public class DuckDBJDBCBasic {
    public static void main(String[] args) {
        // Connection string
        String url = "jdbc:duckdb:data/java_test.db";
        
        try {
            // Establish connection
            Connection conn = DriverManager.getConnection(url);
            System.out.println("✓ Connected to DuckDB");
            
            // Create statement
            Statement stmt = conn.createStatement();
            
            // Create table
            stmt.execute("CREATE TABLE users (id INTEGER, name VARCHAR, email VARCHAR)");
            System.out.println("✓ Table created");
            
            // Insert data
            stmt.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@example.com')");
            stmt.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@example.com')");
            System.out.println("✓ Data inserted");
            
            // Query data
            ResultSet rs = stmt.executeQuery("SELECT * FROM users");
            while (rs.next()) {
                System.out.println("User: " + rs.getInt("id") + 
                                 ", " + rs.getString("name") + 
                                 ", " + rs.getString("email"));
            }
            
            // Cleanup
            rs.close();
            stmt.close();
            conn.close();
            System.out.println("✓ Connection closed");
            
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

### Step 5: Using Multiple Connections from Several Threads

Practice concurrent access with Java:

```java
import java.sql.*;
import java.util.concurrent.*;

public class DuckDBConcurrency {
    private static final int THREAD_COUNT = 5;
    private static final int OPERATIONS_PER_THREAD = 100;
    
    public static void main(String[] args) throws InterruptedException {
        String url = "jdbc:duckdb:data/concurrent_test.db";
        
        // Create thread pool
        ExecutorService executor = Executors.newFixedThreadPool(THREAD_COUNT);
        
        // Submit tasks
        for (int i = 0; i < THREAD_COUNT; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    Connection conn = DriverManager.getConnection(url);
                    Statement stmt = conn.createStatement();
                    
                    // Perform operations
                    for (int j = 0; j < OPERATIONS_PER_THREAD; j++) {
                        stmt.execute(
                            String.format("INSERT INTO concurrent_test VALUES (%d, %d, %f)", 
                                        threadId * OPERATIONS_PER_THREAD + j, 
                                        threadId, 
                                        Math.random() * 100)
                        );
                    }
                    
                    stmt.close();
                    conn.close();
                    System.out.println("✓ Thread " + threadId + " completed");
                    
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            });
        }
        
        // Wait for completion
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);
        System.out.println("✓ All threads completed");
    }
}
```

### Step 6: Using DuckDB as a Data Processing Tool from Java

Use DuckDB for data processing in Java:

```java
import java.sql.*;

public class DuckDBDataProcessing {
    public static void main(String[] args) {
        String url = "jdbc:duckdb:data/processing.db";
        
        try {
            Connection conn = DriverManager.getConnection(url);
            Statement stmt = conn.createStatement();
            
            // Create sample data
            stmt.execute("CREATE TABLE sales (id INTEGER, product_id INTEGER, amount DOUBLE, date DATE)");
            stmt.execute("INSERT INTO sales VALUES (1, 101, 100.50, '2023-01-15')");
            stmt.execute("INSERT INTO sales VALUES (2, 102, 200.75, '2023-01-16')");
            stmt.execute("INSERT INTO sales VALUES (3, 101, 150.25, '2023-01-17')");
            
            // Data aggregation
            ResultSet rs = stmt.executeQuery(
                "SELECT product_id, SUM(amount) as total, COUNT(*) as count " +
                "FROM sales GROUP BY product_id"
            );
            
            System.out.println("Sales Summary:");
            while (rs.next()) {
                System.out.println("Product " + rs.getInt("product_id") + 
                                 ": Total=" + rs.getDouble("total") + 
                                 ", Count=" + rs.getInt("count"));
            }
            
            // Complex transformation
            stmt.execute(
                "CREATE TABLE sales_summary AS " +
                "SELECT " +
                "  product_id, " +
                "  SUM(amount) as total_amount, " +
                "  AVG(amount) as avg_amount, " +
                "  MIN(date) as first_sale, " +
                "  MAX(date) as last_sale " +
                "FROM sales " +
                "GROUP BY product_id"
            );
            
            System.out.println("✓ Data processing complete");
            
            stmt.close();
            conn.close();
            
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

### Step 7: Inserting Large Amounts of Data from Java

Practice efficient bulk insertion in Java:

```java
import java.sql.*;
import java.util.*;

public class DuckDBBulkInsert {
    private static final int BATCH_SIZE = 10000;
    private static final int TOTAL_RECORDS = 100000;
    
    public static void main(String[] args) {
        String url = "jdbc:duckdb:data/bulk_insert.db";
        
        try {
            Connection conn = DriverManager.getConnection(url);
            
            // Method 1: Prepared Statement with Batching
            System.out.println("Method 1: Prepared Statement Batching");
            conn.createStatement().execute("CREATE TABLE bulk_test1 (id INTEGER, value DOUBLE, category VARCHAR)");
            
            PreparedStatement pstmt = conn.prepareStatement("INSERT INTO bulk_test1 VALUES (?, ?, ?)");
            long start = System.currentTimeMillis();
            
            for (int i = 0; i < TOTAL_RECORDS; i++) {
                pstmt.setInt(1, i);
                pstmt.setDouble(2, Math.random() * 100);
                pstmt.setString(3, i % 3 == 0 ? "A" : (i % 3 == 1 ? "B" : "C"));
                pstmt.addBatch();
                
                if (i % BATCH_SIZE == 0) {
                    pstmt.executeBatch();
                }
            }
            pstmt.executeBatch();
            
            long time1 = System.currentTimeMillis() - start;
            System.out.println("✓ Prepared statement batching: " + time1 + "ms");
            
            // Method 2: Appender (most efficient)
            System.out.println("\nMethod 2: Appender");
            conn.createStatement().execute("CREATE TABLE bulk_test2 (id INTEGER, value DOUBLE, category VARCHAR)");
            
            start = System.currentTimeMillis();
            
            // Note: DuckDB Java appender API
            // This requires the specific DuckDB Java appender interface
            // The exact implementation depends on the DuckDB version
            
            long time2 = System.currentTimeMillis() - start;
            System.out.println("✓ Appender: " + time2 + "ms");
            
            conn.close();
            
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

### Step 8: Additional Connection Options

Explore advanced connection options:

```python
import duckdb

print("=== Advanced Connection Options ===")

# Thread-safe connection
con_threadsafe = duckdb.connect('data/threadsafe.db', config={
    'threads': 4,
    'memory_limit': '2GB',
    'default_order': 'ASC'
})
print("✓ Thread-safe connection with custom config")

# Read-only connection with specific access mode
con_readonly_config = duckdb.connect('data/duckdb_practice.db', 
                                   read_only=True,
                                   config={'access_mode': 'read_only'})
print("✓ Configured read-only connection")

# In-memory with specific size limit
con_memory_limit = duckdb.connect(':memory:', config={
    'max_memory': '1GB'
})
print("✓ In-memory connection with size limit")

# Connection with custom extensions
con_extensions = duckdb.connect('data/extensions.db', config={
    'enable_external_access': True,
    'allow_unsigned_extensions': False
})
print("✓ Connection with extension configuration")

# WAL mode for better concurrency
con_wal = duckdb.connect('data/wal_mode.db', config={
    'wal_autocheckpoint': '1GB'
})
print("✓ WAL mode connection")

print("\n=== Connection Options Summary ===")
print("• threads: Number of worker threads")
print("• memory_limit: Maximum memory usage")
print("• default_order: Default sort order")
print("• access_mode: Read/write or read-only")
print("• max_memory: Memory limit for in-memory")
print("• enable_external_access: Allow file access")
print("• wal_autocheckpoint: WAL checkpoint size")
```

### Step 9: Cross-Language Comparison

Compare different client APIs:

```python
import duckdb
import time

print("=== Cross-Language API Comparison ===")

con = duckdb.connect('data/api_comparison.db')

# Create test data
con.execute("""
    CREATE TABLE api_test AS
    SELECT 
        id,
        random() * 100 as value,
        'Category ' || ((id % 5) + 1) as category
    FROM range(100000)
""")

# Performance comparison
operations = [
    "Simple SELECT",
    "Aggregation",
    "Join operation",
    "Window function"
]

queries = [
    "SELECT * FROM api_test LIMIT 1000",
    "SELECT category, AVG(value) FROM api_test GROUP BY category",
    "SELECT a.*, b.value FROM api_test a JOIN api_test b ON a.id = b.id LIMIT 1000",
    "SELECT *, AVG(value) OVER (PARTITION BY category) FROM api_test LIMIT 1000"
]

print("\nPerformance Comparison:")
for op, query in zip(operations, queries):
    start = time.time()
    con.execute(query).fetchall()
    elapsed = time.time() - start
    print(f"{op}: {elapsed:.4f}s")

print("\nLanguage-Specific Considerations:")
print("Python: Best for data science, ML, rapid prototyping")
print("Java: Best for enterprise applications, Spring integration")
print("R: Best for statistical analysis, research")
print("C++: Best for high-performance applications")
```

## 💻 Hands-On Exercises

### Exercise 1: Python API Mastery

Practice advanced Python API usage:

```python
import duckdb
import pandas as pd

# Your advanced Python API code here:
# 1. Connection pooling
# 2. Transaction management
# 3. Error handling
# 4. Performance optimization
```

### Exercise 2: Java JDBC Application

Build a complete Java application:

```java
// Your complete Java application here:
// 1. Connection management
// 2. CRUD operations
// 3. Transaction handling
// 4. Error handling
```

### Exercise 3: Concurrency Patterns

Implement concurrent access patterns:

```python
# Your concurrency implementation here:
# 1. Multi-threaded reads
# 2. Batched writes
# 3. Connection pooling
# 4. Conflict resolution
```

### Exercise 4: Performance Optimization

Optimize API performance:

```python
# Your optimization code here:
# 1. Batch operations
# 2. Memory management
# 3. Query optimization
# 4. Connection tuning
```

### Exercise 5: Cross-Language Integration

Integrate multiple languages:

```python
# Your integration code here:
# 1. Python-Java interoperability
# 2. Shared database access
# 3. Data format exchange
# 4. API bridging
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Understand officially supported DuckDB client languages
2. ✅ Be aware of concurrency considerations
3. ✅ Know different use cases for each API
4. ✅ Be able to import large amounts of data efficiently
5. ✅ Understand JDBC usage patterns
6. ✅ Be able to use DuckDB from Java
7. ✅ Practice concurrent access patterns
8. ✅ Know additional connection options
9. ✅ Understand performance characteristics
10. ✅ Be able to choose the right API for your use case

## 🔍 Verification

Verify your API knowledge:

```python
import duckdb

print("=== Client API Verification ===")

# Test 1: Python API
con = duckdb.connect(':memory:')
con.execute("CREATE TABLE test AS SELECT * FROM range(100)")
result = con.execute("SELECT COUNT(*) FROM test").fetchone()
print(f"✓ Python API: {result[0]} rows")

# Test 2: Connection options
con_config = duckdb.connect(':memory:', config={'threads': 4})
config = con_config.execute("SELECT current_setting('threads')").fetchone()
print(f"✓ Connection config: {config[0]} threads")

# Test 3: Performance
import time
start = time.time()
con.execute("SELECT SUM(column0) FROM test").fetchone()
perf = time.time() - start
print(f"✓ Performance: Query completed in {perf:.4f}s")

print("=== Verification Complete ===")
```

## 🆘 Troubleshooting

### Issue: Java JDBC connection fails

**Solution**: Verify JDBC driver and classpath:
```bash
# Check JDBC driver
java -cp duckdb-jdbc.jar org.duckdb.TestConnection

# Verify classpath
echo $CLASSPATH
```

### Issue: Concurrency errors

**Solution**: Use appropriate connection modes:
```python
# Use WAL mode for better concurrency
con = duckdb.connect('data/test.db', config={'wal_autocheckpoint': '1GB'})
```

### Issue: Memory errors with large datasets

**Solution**: Configure memory limits:
```python
con = duckdb.connect('data/test.db', config={'memory_limit': '4GB'})
```

## 📚 Next Steps

After completing this lab:

1. **Review all labs**: Consolidate your DuckDB knowledge
2. **Practice real projects**: Build applications using your preferred API
3. **Explore advanced features**: Look into specific language features
4. **Contribute to community**: Share your experiences and code

---

**You now have comprehensive knowledge of DuckDB client APIs and can use DuckDB from any major programming language!**