# server.py
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Import database tools and resources
from tools import (
    get_databases,
    query_database,
    execute_sql,
    list_tables,
    describe_table,
    test_connection,
    test_all_connections,
    query_to_csv,
    query_to_csv_string
)
from resources import get_greeting, get_all_databases, get_all_tables, get_database_summary

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("Multi-Database Tools")

# Add resources
@mcp.resource("greeting://{name}")
def greeting_resource(name: str) -> str:
    """Get a personalized greeting"""
    return get_greeting(name)

@mcp.resource("databases://all")
def databases_resource() -> str:
    """Get all available databases with their configurations"""
    return get_all_databases()

@mcp.resource("database://{db_name}/tables")
def tables_resource(db_name: str) -> str:
    """Get all tables from the specified database"""
    return get_all_tables(db_name)

@mcp.resource("database://{db_name}/summary")
def database_summary_resource(db_name: str) -> str:
    """Get summary information about the specified database"""
    return get_database_summary(db_name)

# Add MCP tools
@mcp.tool()
def get_databases_tool() -> str:
    """Get list of all available databases"""
    return get_databases()

@mcp.tool()
def query_database_tool(sql: str, params: str = "", db_name: str = "default") -> str:
    """Execute a SELECT query on the specified MySQL database"""
    return query_database(sql, params, db_name)

@mcp.tool()
def execute_sql_tool(sql: str, params: str = "", db_name: str = "default") -> str:
    """Execute INSERT, UPDATE, or DELETE operations on the specified MySQL database"""
    return execute_sql(sql, params, db_name)

@mcp.tool()
def list_tables_tool(db_name: str = "default") -> str:
    """List all tables in the specified database"""
    return list_tables(db_name)

@mcp.tool()
def describe_table_tool(table_name: str, db_name: str = "default") -> str:
    """Get the structure/schema of a specific table"""
    return describe_table(table_name, db_name)

@mcp.tool()
def test_connection_tool(db_name: str = "default") -> str:
    """Test the connection to the specified database"""
    return test_connection(db_name)

@mcp.tool()
def test_all_connections_tool() -> str:
    """Test connections to all configured databases"""
    return test_all_connections()

@mcp.tool()
def query_to_csv_tool(sql: str, filename: str = "", params: str = "", db_name: str = "default") -> str:
    """Execute a SELECT query and save the results to a CSV file"""
    return query_to_csv(sql, filename, params, db_name)

@mcp.tool()
def query_to_csv_string_tool(sql: str, params: str = "", db_name: str = "default") -> str:
    """Execute a SELECT query and return the results as a CSV string"""
    return query_to_csv_string(sql, params, db_name)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()