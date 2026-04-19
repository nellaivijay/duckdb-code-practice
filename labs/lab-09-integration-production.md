# Lab 9: Integration and Production Readiness

## 🎯 Learning Objectives

- Integrate DuckDB with external databases and systems
- Implement production deployment strategies
- Set up monitoring and alerting
- Design backup and recovery procedures
- Implement security and access control
- Build disaster recovery capabilities

## 📋 Prerequisites

- Completed Lab 8: Real-World Use Cases and Patterns
- Working DuckDB environment
- Understanding of production systems
- Basic knowledge of security concepts

## ⏱️ Estimated Time

60-90 minutes

## 🎓 Conceptual Background

Production readiness requires integration, monitoring, and operational excellence. This lab covers:

**External Integration**: Connecting with databases, APIs, and data lakes
**Production Deployment**: Containerization, orchestration, and scaling
**Monitoring & Alerting**: Health checks, metrics, and alerting systems
**Backup & Recovery**: Data protection and disaster recovery
**Security**: Authentication, encryption, and access control
**Operations**: Automation, documentation, and runbooks

## 🚀 Step-by-Step Instructions

### Step 1: External Database Integration

Connect DuckDB with external databases and data sources.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Attach external databases (SQLite example)
print("External database integration...")

# Create a SQLite database for demonstration
con.execute("ATTACH ':memory:' AS external_db (TYPE sqlite)")

# Create tables in external database
con.execute("""
    CREATE TABLE external_db.external_customers (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        email VARCHAR,
        external_source VARCHAR
    )
""")

# Insert data into external database
con.execute("""
    INSERT INTO external_db.external_customers VALUES 
    (1, 'External User 1', 'external1@example.com', 'API'),
    (2, 'External User 2', 'external2@example.com', 'CSV'),
    (3, 'External User 3', 'external3@example.com', 'Database')
""")

# Query across databases
result = con.execute("""
    SELECT 
        sc.customer_id,
        sc.first_name,
        ec.name as external_name,
        ec.email as external_email,
        ec.external_source
    FROM sample_customers sc
    LEFT JOIN external_db.external_customers ec ON sc.customer_id = ec.id
    LIMIT 5
""").fetchdf()
print("Cross-database query results:")
print(result)

# PostgreSQL integration (requires postgres extension)
print("\nPostgreSQL integration...")

try:
    # Install and load postgres extension
    con.execute("INSTALL postgres")
    con.execute("LOAD postgres")
    
    # Example connection (would need actual PostgreSQL instance)
    # con.execute("ATTACH 'host=localhost user=postgres password=password dbname=testdb' AS pg_db (TYPE postgres)")
    
    print("PostgreSQL extension loaded (connection requires actual PostgreSQL instance)")
    
except Exception as e:
    print(f"PostgreSQL extension not available: {e}")
    print("Using SQLite for demonstration")

# MySQL integration (requires mysql extension)
print("\nMySQL integration...")

try:
    # Install and load mysql extension
    con.execute("INSTALL mysql")
    con.execute("LOAD mysql")
    
    print("MySQL extension loaded (connection requires actual MySQL instance)")
    
except Exception as e:
    print(f"MySQL extension not available: {e}")
    print("Using SQLite for demonstration")

# Data federation pattern
print("\nData federation pattern...")

# Create federated view combining multiple sources
con.execute("""
    CREATE OR REPLACE VIEW federated_customer_view AS
    SELECT 
        'internal' as source_system,
        customer_id,
        first_name,
        last_name,
        segment
    FROM sample_customers
    UNION ALL
    SELECT 
        'external' as source_system,
        id as customer_id,
        name as first_name,
        '' as last_name,
        'external' as segment
    FROM external_db.external_customers
""")

federated_result = con.execute("SELECT * FROM federated_customer_view LIMIT 10").fetchdf()
print("Federated view results:")
print(federated_result)
```

### Step 2: Production Deployment

Implement production deployment strategies.

```python
import duckdb
import os
from datetime import datetime

# Production deployment configuration
print("Production deployment configuration...")

class ProductionConfig:
    def __init__(self):
        self.config = {
            # Database configuration
            'database_path': os.environ.get('DUCKDB_DATABASE_PATH', '/data/production.db'),
            'memory_limit': os.environ.get('DUCKDB_MEMORY_LIMIT', '8GB'),
            'threads': os.environ.get('DUCKDB_THREADS', '8'),
            
            # Performance configuration
            'enable_object_cache': True,
            'enable_profiling': False,
            'optimizer_enable': True,
            
            # Security configuration
            'enable_access_control': True,
            'encryption_enabled': False,
            
            # Logging configuration
            'log_level': 'INFO',
            'log_path': '/var/log/duckdb/'
        }
    
    def apply_configuration(self, connection):
        """Apply configuration to DuckDB connection"""
        con = connection
        
        # Apply memory settings
        con.execute(f"SET memory_limit='{self.config['memory_limit']}'")
        con.execute(f"SET threads={self.config['threads']}")
        
        # Apply performance settings
        con.execute(f"SET enable_object_cache={self.config['enable_object_cache']}")
        con.execute(f"SET enable_profiling={self.config['enable_profiling']}")
        con.execute(f"SET enable_optimizer={self.config['optimizer_enable']}")
        
        print(f"Configuration applied: {self.config}")
        
        return con

# Apply production configuration
prod_config = ProductionConfig()
prod_con = duckdb.connect(':memory:')  # Use in-memory for demo
prod_con = prod_config.apply_configuration(prod_con)

# Container deployment strategy
print("\nContainer deployment strategy...")

# Dockerfile example (as documentation)
dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /data

# Set environment variables
ENV DUCKDB_DATABASE_PATH=/data/production.db
ENV DUCKDB_MEMORY_LIMIT=8GB
ENV DUCKDB_THREADS=8

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import duckdb; con = duckdb.connect('/data/production.db'); con.execute('SELECT 1').fetchone()"

# Run application
CMD ["python", "app.py"]
"""

print("Dockerfile content:")
print(dockerfile_content)

# Kubernetes deployment example
kubernetes_deployment = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: duckdb-production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: duckdb
  template:
    metadata:
      labels:
        app: duckdb
    spec:
      containers:
      - name: duckdb
        image: duckdb-production:latest
        ports:
        - containerPort: 8080
        env:
        - name: DUCKDB_DATABASE_PATH
          value: "/data/production.db"
        - name: DUCKDB_MEMORY_LIMIT
          value: "8GB"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "16Gi"
            cpu: "8"
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: duckdb-storage
"""

print("Kubernetes deployment configuration:")
print(kubernetes_deployment)

# Health check implementation
print("\nHealth check implementation...")

class HealthChecker:
    def __init__(self, connection):
        self.con = connection
    
    def check_database_health(self):
        """Check if database is healthy"""
        try:
            # Basic connectivity check
            result = self.con.execute("SELECT 1").fetchone()
            
            # Check if critical tables exist
            tables = self.con.execute("SHOW TABLES").fetchall()
            
            # Check recent query performance
            import time
            start = time.time()
            self.con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()
            query_time = time.time() - start
            
            health_status = {
                'status': 'healthy',
                'connectivity': 'ok',
                'tables_count': len(tables),
                'query_performance': f'{query_time:.4f}s',
                'timestamp': datetime.now().isoformat()
            }
            
            return health_status
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_disk_space(self, database_path):
        """Check available disk space"""
        import shutil
        total, used, free = shutil.disk_usage(database_path)
        
        return {
            'total_gb': total / (1024**3),
            'used_gb': used / (1024**3),
            'free_gb': free / (1024**3),
            'usage_percent': (used / total) * 100
        }

# Run health check
health_checker = HealthChecker(con)
health_status = health_checker.check_database_health()
print("Database health status:")
print(health_status)
```

### Step 3: Monitoring and Alerting

Implement comprehensive monitoring and alerting.

```python
import duckdb
import time
from datetime import datetime, timedelta

con = duckdb.connect('data/duckdb_practice.db')

# Metrics collection framework
print("Monitoring and alerting framework...")

class MetricsCollector:
    def __init__(self, connection):
        self.con = connection
        self.metrics = []
    
    def collect_query_metrics(self, query, query_name):
        """Collect metrics for a specific query"""
        start_time = time.time()
        
        try:
            result = self.con.execute(query).fetchdf()
            execution_time = time.time() - start_time
            
            metric = {
                'query_name': query_name,
                'execution_time': execution_time,
                'rows_returned': len(result),
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
            self.metrics.append(metric)
            return metric
            
        except Exception as e:
            execution_time = time.time() - start_time
            metric = {
                'query_name': query_name,
                'execution_time': execution_time,
                'rows_returned': 0,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            self.metrics.append(metric)
            return metric
    
    def collect_system_metrics(self):
        """Collect system-level metrics"""
        try:
            # Database size
            db_size = self.con.execute("PRAGMA database_size").fetchone()
            
            # Memory usage
            memory_info = self.con.execute("SELECT * FROM duckdb_memory_info()").fetchdf()
            
            # Active connections
            connections = self.con.execute("SELECT COUNT(*) FROM duckdb_queries()").fetchone()
            
            metric = {
                'metric_type': 'system',
                'database_size': db_size,
                'active_connections': connections[0],
                'memory_info': memory_info.to_dict() if len(memory_info) > 0 else {},
                'timestamp': datetime.now().isoformat()
            }
            
            self.metrics.append(metric)
            return metric
            
        except Exception as e:
            metric = {
                'metric_type': 'system',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            self.metrics.append(metric)
            return metric
    
    def get_metrics_summary(self):
        """Get summary of collected metrics"""
        import pandas as pd
        df = pd.DataFrame(self.metrics)
        return df

# Alerting framework
class AlertManager:
    def __init__(self):
        self.alerts = []
        self.alert_rules = {
            'query_performance': {'threshold': 5.0, 'comparison': 'greater_than'},
            'error_rate': {'threshold': 0.1, 'comparison': 'greater_than'},
            'disk_usage': {'threshold': 90.0, 'comparison': 'greater_than'}
        }
    
    def check_alert(self, metric, rule_name):
        """Check if metric triggers alert"""
        if rule_name not in self.alert_rules:
            return None
        
        rule = self.alert_rules[rule_name]
        threshold = rule['threshold']
        comparison = rule['comparison']
        
        # Extract value from metric (simplified)
        value = metric.get('execution_time', 0)
        
        triggered = False
        if comparison == 'greater_than' and value > threshold:
            triggered = True
        elif comparison == 'less_than' and value < threshold:
            triggered = True
        
        if triggered:
            alert = {
                'rule_name': rule_name,
                'metric_value': value,
                'threshold': threshold,
                'timestamp': datetime.now().isoformat(),
                'severity': 'high' if value > threshold * 2 else 'medium'
            }
            self.alerts.append(alert)
            return alert
        
        return None
    
    def get_alerts(self):
        """Get all alerts"""
        return self.alerts

# Run monitoring
print("Running monitoring...")

metrics_collector = MetricsCollector(con)
alert_manager = AlertManager()

# Collect query metrics
metrics_collector.collect_query_metrics(
    "SELECT COUNT(*) FROM sample_customers",
    "customer_count"
)

metrics_collector.collect_query_metrics(
    "SELECT * FROM sample_orders WHERE order_date >= '2022-01-01'",
    "recent_orders"
)

metrics_collector.collect_system_metrics()

# Check for alerts
for metric in metrics_collector.metrics:
    if metric.get('metric_type') == 'query':
        alert_manager.check_alert(metric, 'query_performance')

# Get results
metrics_summary = metrics_collector.get_metrics_summary()
alerts = alert_manager.get_alerts()

print("Metrics Summary:")
print(metrics_summary)

print("\nAlerts:")
if alerts:
    for alert in alerts:
        print(f"ALERT: {alert}")
else:
    print("No alerts triggered")
```

### Step 4: Backup and Recovery

Implement backup and recovery procedures.

```python
import duckdb
import os
import shutil
from datetime import datetime

con = duckdb.connect('data/duckdb_practice.db')

# Backup framework
print("Backup and recovery framework...")

class BackupManager:
    def __init__(self, connection, backup_dir):
        self.con = connection
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, backup_name=None):
        """Create a full backup of the database"""
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            # Export all tables to Parquet files
            tables = self.con.execute("SHOW TABLES").fetchall()
            
            for table in tables:
                table_name = table[0]
                file_path = os.path.join(backup_path, f"{table_name}.parquet")
                
                self.con.execute(f"""
                    COPY {table_name} TO '{file_path}' (FORMAT PARQUET)
                """)
                
                print(f"Backed up table: {table_name}")
            
            # Create backup metadata
            metadata = {
                'backup_name': backup_name,
                'backup_time': datetime.now().isoformat(),
                'tables_backed_up': len(tables),
                'backup_path': backup_path
            }
            
            # Save metadata
            metadata_path = os.path.join(backup_path, 'backup_metadata.json')
            with open(metadata_path, 'w') as f:
                import json
                json.dump(metadata, f, indent=2)
            
            print(f"Backup created successfully: {backup_path}")
            return metadata
            
        except Exception as e:
            print(f"Backup failed: {e}")
            raise
    
    def restore_backup(self, backup_name):
        """Restore database from backup"""
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        
        try:
            # Read backup metadata
            metadata_path = os.path.join(backup_path, 'backup_metadata.json')
            with open(metadata_path, 'r') as f:
                import json
                metadata = json.load(f)
            
            print(f"Restoring backup: {metadata['backup_name']}")
            
            # Restore tables
            for file in os.listdir(backup_path):
                if file.endswith('.parquet'):
                    table_name = file.replace('.parquet', '')
                    file_path = os.path.join(backup_path, file)
                    
                    self.con.execute(f"""
                        CREATE OR REPLACE TABLE {table_name} AS 
                        SELECT * FROM '{file_path}'
                    """)
                    
                    print(f"Restored table: {table_name}")
            
            print(f"Backup restored successfully from: {backup_path}")
            return metadata
            
        except Exception as e:
            print(f"Restore failed: {e}")
            raise
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        
        for item in os.listdir(self.backup_dir):
            item_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(item_path):
                metadata_path = os.path.join(item_path, 'backup_metadata.json')
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        import json
                        metadata = json.load(f)
                    backups.append(metadata)
        
        return backups

# Run backup operations
print("Running backup operations...")

backup_manager = BackupManager(con, 'backups')

# Create backup
backup_metadata = backup_manager.create_backup()
print(f"Backup metadata: {backup_metadata}")

# List backups
available_backups = backup_manager.list_backups()
print("Available backups:")
for backup in available_backups:
    print(f"  - {backup['backup_name']} ({backup['backup_time']})")

# Incremental backup strategy
print("\nIncremental backup strategy...")

class IncrementalBackupManager(BackupManager):
    def create_incremental_backup(self, base_backup_name):
        """Create incremental backup based on base backup"""
        # This is a simplified version - real implementation would track changes
        base_backup_path = os.path.join(self.backup_dir, base_backup_name)
        
        if not os.path.exists(base_backup_path):
            raise FileNotFoundError(f"Base backup not found: {base_backup_name}")
        
        # Create incremental backup
        incremental_name = f"incremental_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return self.create_backup(incremental_name)

# Disaster recovery procedures
print("\nDisaster recovery procedures...")

class DisasterRecoveryManager:
    def __init__(self, backup_manager):
        self.backup_manager = backup_manager
        self.recovery_plan = {
            'rpo_hours': 24,  # Recovery Point Objective
            'rto_hours': 4,   # Recovery Time Objective
            'backup_retention_days': 30
        }
    
    def assess_recovery_status(self):
        """Assess current recovery readiness"""
        backups = self.backup_manager.list_backups()
        
        # Find most recent backup
        if backups:
            latest_backup = max(backups, key=lambda x: x['backup_time'])
            backup_age = datetime.now() - datetime.fromisoformat(latest_backup['backup_time'])
            
            return {
                'status': 'ready' if backup_age.total_seconds() < 3600 else 'warning',
                'latest_backup': latest_backup['backup_name'],
                'backup_age_hours': backup_age.total_seconds() / 3600,
                'available_backups': len(backups)
            }
        else:
            return {
                'status': 'critical',
                'message': 'No backups available'
            }
    
    def execute_recovery_plan(self, backup_name):
        """Execute disaster recovery plan"""
        print(f"Executing recovery plan using backup: {backup_name}")
        
        # Step 1: Validate backup
        print("Step 1: Validating backup...")
        # (Validation logic here)
        
        # Step 2: Restore database
        print("Step 2: Restoring database...")
        self.backup_manager.restore_backup(backup_name)
        
        # Step 3: Verify data integrity
        print("Step 3: Verifying data integrity...")
        # (Integrity checks here)
        
        # Step 4: Update recovery status
        print("Step 4: Recovery completed")
        
        return {
            'status': 'success',
            'recovery_time': datetime.now().isoformat(),
            'backup_used': backup_name
        }

# Run disaster recovery assessment
dr_manager = DisasterRecoveryManager(backup_manager)
recovery_status = dr_manager.assess_recovery_status()
print("Disaster recovery status:")
print(recovery_status)
```

### Step 5: Security Implementation

Implement security and access control.

```python
import duckdb
import hashlib
from datetime import datetime

con = duckdb.connect('data/duckdb_practice.db')

# Security framework
print("Security implementation...")

class SecurityManager:
    def __init__(self, connection):
        self.con = connection
        self.setup_security_tables()
    
    def setup_security_tables(self):
        """Setup security-related tables"""
        # Users table
        self.con.execute("""
            CREATE OR REPLACE TABLE security_users (
                user_id INTEGER PRIMARY KEY,
                username VARCHAR UNIQUE,
                password_hash VARCHAR,
                email VARCHAR,
                role VARCHAR,
                created_at TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN
            )
        """)
        
        # Roles table
        self.con.execute("""
            CREATE OR REPLACE TABLE security_roles (
                role_id INTEGER PRIMARY KEY,
                role_name VARCHAR UNIQUE,
                description VARCHAR,
                permissions JSON
            )
        """)
        
        # Audit log table
        self.con.execute("""
            CREATE OR REPLACE TABLE security_audit_log (
                audit_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                action VARCHAR,
                resource VARCHAR,
                timestamp TIMESTAMP,
                ip_address VARCHAR,
                success BOOLEAN,
                details JSON
            )
        """)
        
        print("Security tables created")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, email, role):
        """Create a new user"""
        password_hash = self.hash_password(password)
        
        user_id = self.con.execute(f"""
            SELECT COALESCE(MAX(user_id), 0) + 1 FROM security_users
        """).fetchone()[0]
        
        self.con.execute("""
            INSERT INTO security_users 
            (user_id, username, password_hash, email, role, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, true)
        """, [user_id, username, password_hash, email, role, datetime.now()])
        
        print(f"User created: {username} with role: {role}")
        return user_id
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        password_hash = self.hash_password(password)
        
        result = self.con.execute("""
            SELECT user_id, username, role, is_active 
            FROM security_users 
            WHERE username = ? AND password_hash = ?
        """, [username, password_hash]).fetchone()
        
        if result and result[3]:  # is_active
            # Update last login
            self.con.execute("""
                UPDATE security_users 
                SET last_login = ? 
                WHERE user_id = ?
            """, [datetime.now(), result[0]])
            
            # Log successful login
            self.log_audit(result[0], 'login', 'system', True, {'username': username})
            
            return {
                'user_id': result[0],
                'username': result[1],
                'role': result[2]
            }
        else:
            # Log failed login attempt
            self.log_audit(None, 'login', 'system', False, {'username': username})
            return None
    
    def log_audit(self, user_id, action, resource, success, details):
        """Log security audit event"""
        audit_id = self.con.execute(f"""
            SELECT COALESCE(MAX(audit_id), 0) + 1 FROM security_audit_log
        """).fetchone()[0]
        
        self.con.execute("""
            INSERT INTO security_audit_log 
            (audit_id, user_id, action, resource, timestamp, success, details)
            VALUES (?, ?, ?, ?, ?, ?, ?::JSON)
        """, [audit_id, user_id, action, resource, datetime.now(), success, str(details)])
        
        return audit_id
    
    def check_permission(self, user, resource, action):
        """Check if user has permission for action on resource"""
        # Simplified permission check
        if user['role'] == 'admin':
            return True
        elif user['role'] == 'analyst' and action == 'read':
            return True
        else:
            return False

# Setup security
print("Setting up security...")

security_manager = SecurityManager(con)

# Create users
security_manager.create_user('admin', 'securePassword123', 'admin@example.com', 'admin')
security_manager.create_user('analyst', 'analystPassword123', 'analyst@example.com', 'analyst')
security_manager.create_user('readonly', 'readonlyPassword123', 'readonly@example.com', 'readonly')

# Test authentication
print("\nTesting authentication...")

# Successful login
admin_user = security_manager.authenticate_user('admin', 'securePassword123')
print(f"Admin login: {admin_user}")

# Failed login
failed_login = security_manager.authenticate_user('admin', 'wrongpassword')
print(f"Failed login: {failed_login}")

# Test permissions
print("\nTesting permissions...")

if admin_user:
    can_delete = security_manager.check_permission(admin_user, 'sample_customers', 'delete')
    print(f"Admin can delete: {can_delete}")

    analyst_user = security_manager.authenticate_user('analyst', 'analystPassword123')
    if analyst_user:
        can_delete = security_manager.check_permission(analyst_user, 'sample_customers', 'delete')
        print(f"Analyst can delete: {can_delete}")

# View audit log
audit_log = con.execute("SELECT * FROM security_audit_log ORDER BY timestamp DESC LIMIT 5").fetchdf()
print("\nRecent audit log:")
print(audit_log)
```

### Step 6: Operations Automation

Implement operational automation and documentation.

```python
import duckdb
from datetime import datetime, timedelta

con = duckdb.connect('data/duckdb_practice.db')

# Operations automation
print("Operations automation...")

class OperationsAutomation:
    def __init__(self, connection):
        self.con = connection
        self.setup_operations_tables()
    
    def setup_operations_tables(self):
        """Setup operations-related tables"""
        # Scheduled tasks table
        self.con.execute("""
            CREATE OR REPLACE TABLE ops_scheduled_tasks (
                task_id INTEGER PRIMARY KEY,
                task_name VARCHAR,
                task_type VARCHAR,
                schedule VARCHAR,
                last_run TIMESTAMP,
                next_run TIMESTAMP,
                status VARCHAR,
                config JSON
            )
        """)
        
        # Runbook table
        self.con.execute("""
            CREATE OR REPLACE TABLE ops_runbooks (
                runbook_id INTEGER PRIMARY KEY,
                runbook_name VARCHAR,
                description VARCHAR,
                steps JSON,
                owner VARCHAR,
                last_updated TIMESTAMP
            )
        """)
        
        print("Operations tables created")
    
    def schedule_task(self, task_name, task_type, schedule, config):
        """Schedule a new task"""
        task_id = self.con.execute(f"""
            SELECT COALESCE(MAX(task_id), 0) + 1 FROM ops_scheduled_tasks
        """).fetchone()[0]
        
        # Calculate next run time (simplified)
        next_run = datetime.now() + timedelta(hours=1)
        
        self.con.execute("""
            INSERT INTO ops_scheduled_tasks 
            (task_id, task_name, task_type, schedule, next_run, status, config)
            VALUES (?, ?, ?, ?, ?, 'scheduled', ?::JSON)
        """, [task_id, task_name, task_type, schedule, next_run, str(config)])
        
        print(f"Task scheduled: {task_name} (ID: {task_id})")
        return task_id
    
    def create_runbook(self, runbook_name, description, steps, owner):
        """Create a new runbook"""
        runbook_id = self.con.execute(f"""
            SELECT COALESCE(MAX(runbook_id), 0) + 1 FROM ops_runbooks
        """).fetchone()[0]
        
        self.con.execute("""
            INSERT INTO ops_runbooks 
            (runbook_id, runbook_name, description, steps, owner, last_updated)
            VALUES (?, ?, ?, ?::JSON, ?, ?)
        """, [runbook_id, runbook_name, description, str(steps), owner, datetime.now()])
        
        print(f"Runbook created: {runbook_name} (ID: {runbook_id})")
        return runbook_id
    
    def execute_runbook(self, runbook_id):
        """Execute a runbook"""
        runbook = self.con.execute(f"""
            SELECT runbook_name, steps FROM ops_runbooks 
            WHERE runbook_id = {runbook_id}
        """).fetchone()
        
        if not runbook:
            raise ValueError(f"Runbook not found: {runbook_id}")
        
        print(f"Executing runbook: {runbook[0]}")
        
        # Parse and execute steps (simplified)
        steps = eval(runbook[1])  # In production, use proper JSON parsing
        
        for i, step in enumerate(steps):
            print(f"Step {i+1}: {step['description']}")
            # Execute step logic here
            # (This would be more sophisticated in production)
        
        print(f"Runbook {runbook[0]} completed")
        return True

# Setup operations
print("Setting up operations automation...")

ops_automation = OperationsAutomation(con)

# Schedule common tasks
ops_automation.schedule_task(
    'daily_backup',
    'backup',
    '0 2 * * *',  # Daily at 2 AM
    {'backup_type': 'full', 'retention_days': 30}
)

ops_automation.schedule_task(
    'data_quality_check',
    'validation',
    '0 6 * * *',  # Daily at 6 AM
    {'tables': ['sample_customers', 'sample_orders']}
)

ops_automation.schedule_task(
    'performance_metrics',
    'monitoring',
    '*/30 * * * *',  # Every 30 minutes
    {'metrics': ['query_time', 'memory_usage', 'disk_usage']}
)

# Create runbooks
backup_runbook_steps = [
    {'description': 'Stop applications', 'command': 'systemctl stop app'},
    {'description': 'Create backup', 'command': 'python backup.py'},
    {'description': 'Verify backup', 'command': 'python verify_backup.py'},
    {'description': 'Start applications', 'command': 'systemctl start app'}
]

ops_automation.create_runbook(
    'Database Backup',
    'Complete database backup procedure',
    backup_runbook_steps,
    'dba_team'
)

recovery_runbook_steps = [
    {'description': 'Stop applications', 'command': 'systemctl stop app'},
    {'description': 'Restore from backup', 'command': 'python restore.py'},
    {'description': 'Verify data integrity', 'command': 'python verify_integrity.py'},
    {'description': 'Start applications', 'command': 'systemctl start app'},
    {'description': 'Monitor for issues', 'command': 'python monitor.py'}
]

ops_automation.create_runbook(
    'Disaster Recovery',
    'Complete disaster recovery procedure',
    recovery_runbook_steps,
    'dba_team'
)

# View scheduled tasks
scheduled_tasks = con.execute("SELECT * FROM ops_scheduled_tasks").fetchdf()
print("Scheduled tasks:")
print(scheduled_tasks)

# View runbooks
runbooks = con.execute("SELECT * FROM ops_runbooks").fetchdf()
print("\nAvailable runbooks:")
print(runbooks)
```

## 💻 Hands-On Exercises

### Exercise 1: Build Production Deployment

Create complete production deployment setup:

```python
# Your code here
# Container configuration
# Orchestration setup
# CI/CD integration
# Environment management
# Rolling updates
```

### Exercise 2: Comprehensive Monitoring System

Build production monitoring and alerting:

```python
# Your code here
# Metrics collection
# Alert routing
# Dashboard creation
# Performance baselines
# Anomaly detection
```

### Exercise 3: Backup Strategy Design

Design comprehensive backup strategy:

```python
# Your code here
# Backup scheduling
# Retention policies
# Recovery testing
# Backup validation
# Offsite storage
```

### Exercise 4: Security Hardening

Implement comprehensive security measures:

```python
# Your code here
# Encryption at rest
# Network security
# Access control
# Audit logging
# Compliance reporting
```

### Exercise 5: Operations Runbook Library

Create comprehensive operations runbook library:

```python
# Your code here
# Common procedures
# Emergency procedures
# Maintenance procedures
# Troubleshooting guides
# Documentation templates
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Integrate DuckDB with external systems
2. ✅ Implement production deployment strategies
3. ✅ Set up monitoring and alerting
4. ✅ Design backup and recovery procedures
5. ✅ Implement security measures
6. ✅ Build operational automation

## 🔍 Verification

Test your production readiness skills:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Test external integration
external_test = con.execute("SELECT COUNT(*) FROM federated_customer_view").fetchone()
print(f"External integration test: {external_test[0]} rows")

# Test security
security_test = con.execute("SELECT COUNT(*) FROM security_users").fetchone()
print(f"Security users test: {security_test[0]} users")

# Test operations
ops_test = con.execute("SELECT COUNT(*) FROM ops_scheduled_tasks").fetchone()
print(f"Operations tasks test: {ops_test[0]} tasks")

# Test backup
backup_test = len(backup_manager.list_backups())
print(f"Backup test: {backup_test} backups available")

print("✅ Production readiness test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: External connection failures

**Solution**: Implement connection pooling and retry logic:
```python
# Add connection retry logic
# Implement connection pooling
# Use circuit breakers
# Add connection health checks
```

### Issue: Backup performance degradation

**Solution**: Optimize backup strategies:
```python
# Use incremental backups
# Implement parallel backup
-- Compress backup data
# Schedule during low-traffic periods
```

### Issue: Security performance impact

**Solution**: Balance security and performance:
```python
# Cache authentication results
# Use connection pooling
# Optimize audit logging
-- Implement role-based access efficiently
```

## 📚 Next Steps

After completing this lab:

1. **Study advanced topics**: Deep dive into specific areas
2. **Build production system**: Apply to real deployment
3. **Implement monitoring**: Set up production monitoring
4. **Document procedures**: Create operational documentation

---

**Congratulations! You have completed all 9 labs and are now ready for production DuckDB deployment in lakehouse environments!**