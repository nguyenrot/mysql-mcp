# MySQL MCP Tools

This is a Model Context Protocol (MCP) server that provides tools for querying and managing a MySQL database.

## Features

The server provides the following tools:

1. **query_database** - Execute SELECT queries on the MySQL database
2. **execute_sql** - Execute INSERT, UPDATE, or DELETE operations
3. **list_tables** - List all tables in the database
4. **describe_table** - Get the structure/schema of a specific table
5. **test_connection** - Test the database connection
6. **query_to_csv** - Execute a SELECT query and save results to a CSV file
7. **query_to_csv_string** - Execute a SELECT query and return results as a CSV string

### Resources

The server also provides these resources:

- **greeting://{name}** - Get a personalized greeting
- **database://tables** - Get all tables from the database with metadata

## Database Configuration

The database connection is configured using environment variables in the `.env` file:

```
DB_USER=root
DB_PASS=root@1345
DB_NAME=rc
DB_HOST=0.0.0.0
DB_PORT=3306

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Configure your database credentials in the `.env` file

3. Run the MCP server:

```bash
python database_mcp.py
```

## Usage Examples

### Query Database

Execute a SELECT query:

```
Tool: query_database
Parameters:
- sql: "SELECT * FROM users LIMIT 5"
- params: "" (optional)
```

### Execute SQL Operations

Execute INSERT, UPDATE, or DELETE:

```
Tool: execute_sql
Parameters:
- sql: "INSERT INTO users (name, email) VALUES (%s, %s)"
- params: "John Doe,john@example.com"
```

### List Tables

Get all tables in the database:

```
Tool: list_tables
```

### Describe Table

Get table structure:

```
Tool: describe_table
Parameters:
- table_name: "users"
```

### Test Connection

Check database connectivity:

```
Tool: test_connection
```

### Export Query Results to CSV

Save query results to a CSV file:

```
Tool: query_to_csv
Parameters:
- sql: "SELECT * FROM users"
- filename: "users_export.csv" (optional, defaults to "query_results.csv")
- params: "" (optional)
```

### Get Query Results as CSV String

Get query results as CSV string in memory:

```
Tool: query_to_csv_string
Parameters:
- sql: "SELECT * FROM products WHERE price > %s"
- params: "100"
```

## MCP Client Configuration

To use this MCP server with MCP clients, you need to configure the client to connect to this server.

### Configuration File (mcp.json)

Create or update your MCP client configuration file (usually `mcp.json` or similar):

#### Using System Python:

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "python",
      "args": ["/path/to/your/mcptools/database_mcp.py"],
      "cwd": "/path/to/your/mcptools",
      "env": {
        "PYTHONPATH": "/path/to/your/mcptools"
      }
    }
  }
}
```

#### Using Virtual Environment Python:

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["/path/to/your/mcptools/database_mcp.py"],
      "cwd": "/path/to/your/mcptools",
      "env": {
        "PYTHONPATH": "/path/to/your/mcptools"
      }
    }
  }
}
```

#### Using Conda Environment:

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "/path/to/conda/envs/your-env/bin/python",
      "args": ["/path/to/your/mcptools/database_mcp.py"],
      "cwd": "/path/to/your/mcptools",
      "env": {
        "PYTHONPATH": "/path/to/your/mcptools"
      }
    }
  }
}
```

### Claude Desktop Configuration

For Claude Desktop, add this configuration to your `claude_desktop_config.json`:

#### Using System Python:

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "python",
      "args": ["/home/nguyen/Public/mcptools/database_mcp.py"],
      "cwd": "/home/nguyen/Public/mcptools",
      "env": {
        "PYTHONPATH": "/home/nguyen/Public/mcptools"
      }
    }
  }
}
```

#### Using Virtual Environment Python:

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "/home/nguyen/Public/mcptools/venv/bin/python",
      "args": ["/home/nguyen/Public/mcptools/database_mcp.py"],
      "cwd": "/home/nguyen/Public/mcptools",
      "env": {
        "PYTHONPATH": "/home/nguyen/Public/mcptools"
      }
    }
  }
}
```

### VS Code MCP Extension

If using VS Code with an MCP extension:

1. Open VS Code settings
2. Search for "MCP" settings
3. Add the server configuration:
   - **Name**: `database-tools`
   - **Command**: `python` (or full path to your Python executable)
   - **Args**: `["/path/to/your/mcptools/database_mcp.py"]`
   - **Working Directory**: `/path/to/your/mcptools`

### Finding Your Python Environment Path

To find the correct Python path for your environment:

#### For Virtual Environment:

```bash
# Activate your virtual environment first
source /path/to/your/venv/bin/activate
# Then find the Python path
which python
```

#### For Conda Environment:

```bash
# Activate your conda environment first
conda activate your-env-name
# Then find the Python path
which python
```

#### For System Python:

```bash
# Find system Python path
which python
# or
which python3
```

#### Example Output:

- Virtual Environment: `/home/user/myproject/venv/bin/python`
- Conda Environment: `/home/user/miniconda3/envs/myenv/bin/python`
- System Python: `/usr/bin/python3`

### Available Resources

The server also provides resources that can be accessed by MCP clients:

- **`greeting://{name}`** - Get a personalized greeting
- **`database://tables`** - Get all tables from the database with metadata

### Troubleshooting Client Configuration

1. **Path Issues**: Ensure all paths in the configuration are absolute paths
2. **Python Environment**: Make sure the Python environment has all required dependencies installed
3. **Permissions**: Ensure the MCP client has permission to execute the server script
4. **Database Connection**: Verify the `.env` file is properly configured with database credentials
5. **Server Status**: Check if the server starts without errors by running `python database_mcp.py` manually

## Security Notes

- The database credentials are stored in environment variables for better security
- Use parameterized queries to prevent SQL injection
- Ensure your MySQL server is properly secured

## Dependencies

- mcp - Model Context Protocol framework
- mysql-connector-python - MySQL database connector
- python-dotenv - Environment variable management
