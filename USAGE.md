# MCP Database Tools Usage Examples

This document provides examples of how to use the MCP database tools.

## Available Tools

1. **test_connection()** - Test database connectivity
2. **list_tables()** - List all tables in the database
3. **describe_table(table_name)** - Get table schema/structure
4. **query_database(sql, params)** - Execute SELECT queries
5. **execute_sql(sql, params)** - Execute INSERT/UPDATE/DELETE queries

## Usage Examples

### 1. Test Database Connection

```python
# Test if the database connection is working
result = test_connection()
```

### 2. List All Tables

```python
# Get a list of all tables in the database
tables = list_tables()
```

### 3. Describe Table Structure

```python
# Get the schema of a specific table
schema = describe_table("users")
```

### 4. Execute SELECT Queries

```python
# Simple query without parameters
result = query_database("SELECT * FROM users LIMIT 10")

# Query with parameters (safer for user input)
result = query_database(
    "SELECT * FROM users WHERE age > %s AND city = %s",
    "25,New York"
)
```

### 5. Execute Data Modification Queries

```python
# Insert new record
result = execute_sql(
    "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
    "John Doe,john@example.com,30"
)

# Update existing records
result = execute_sql(
    "UPDATE users SET age = %s WHERE id = %s",
    "31,123"
)

# Delete records
result = execute_sql(
    "DELETE FROM users WHERE id = %s",
    "123"
)
```

## Database Configuration

The MCP server connects to MySQL using these environment variables:

- `DB_HOST`: Database host (default: 0.0.0.0)
- `DB_NAME`: Database name (default: rc)
- `DB_USER`: Database user (default: root)
- `DB_PASS`: Database password (default: root@1345)
- `DB_PORT`: Database port (default: 3306)

## Security Notes

1. Always use parameterized queries to prevent SQL injection
2. Store sensitive database credentials in environment variables
3. Use appropriate database user permissions
4. Consider connection pooling for high-traffic applications

## Error Handling

All tools return JSON responses with error information when something goes wrong:

```json
{
  "error": "Database connection failed: Access denied for user 'root'@'localhost'"
}
```

## Running the MCP Server

To start the MCP server:

```bash
python server.py
```

The server will be available for MCP clients to connect and use the database tools.
