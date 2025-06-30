# tools.py
import json
import csv
import io
import os
from database import (
    execute_query, 
    execute_non_query, 
    get_db_connection, 
    get_available_databases,
    get_database_info,
    DB_CONFIGS
)


def get_databases() -> str:
    """
    Get list of all available databases.
    
    Returns:
        JSON string containing list of database names and their info
    """
    try:
        databases = get_available_databases()
        db_info = {}
        
        for db_name in databases:
            db_info[db_name] = get_database_info(db_name)
        
        return json.dumps({
            "databases": databases,
            "database_info": db_info,
            "total_databases": len(databases)
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


def query_database(sql: str, params: str = "", db_name: str = "default") -> str:
    """
    Execute a SELECT query on the specified MySQL database.
    
    Args:
        sql: The SQL SELECT query to execute
        params: Optional comma-separated parameters for parameterized queries (e.g., "value1,value2")
        db_name: The database name to query (default: "default")
    
    Returns:
        JSON string containing the query results
    """
    try:
        # Parse parameters if provided
        query_params = None
        if params.strip():
            query_params = tuple(param.strip() for param in params.split(','))
        
        results = execute_query(sql, query_params, db_name)
        return json.dumps({
            "database": db_name,
            "results": results,
            "row_count": len(results)
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)


def execute_sql(sql: str, params: str = "", db_name: str = "default") -> str:
    """
    Execute INSERT, UPDATE, or DELETE operations on the specified MySQL database.
    
    Args:
        sql: The SQL query to execute (INSERT, UPDATE, DELETE)
        params: Optional comma-separated parameters for parameterized queries (e.g., "value1,value2")
        db_name: The database name to execute on (default: "default")
    
    Returns:
        JSON string containing the execution results (affected rows, last insert ID)
    """
    try:
        # Parse parameters if provided
        query_params = None
        if params.strip():
            query_params = tuple(param.strip() for param in params.split(','))
        
        result = execute_non_query(sql, query_params, db_name)
        result["database"] = db_name
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)


def list_tables(db_name: str = "default") -> str:
    """
    List all tables in the specified database.
    
    Args:
        db_name: The database name to list tables from (default: "default")
    
    Returns:
        JSON string containing list of table names
    """
    try:
        results = execute_query("SHOW TABLES", None, db_name)
        tables = [list(row.values())[0] for row in results]
        return json.dumps({
            "database": db_name,
            "tables": tables,
            "table_count": len(tables)
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)


def describe_table(table_name: str, db_name: str = "default") -> str:
    """
    Get the structure/schema of a specific table.
    
    Args:
        table_name: Name of the table to describe
        db_name: The database name containing the table (default: "default")
    
    Returns:
        JSON string containing table structure information
    """
    try:
        results = execute_query(f"DESCRIBE `{table_name}`", None, db_name)
        return json.dumps({
            "database": db_name,
            "table": table_name,
            "structure": results
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name, "table": table_name}, indent=2)


def test_connection(db_name: str = "default") -> str:
    """
    Test the connection to the specified database.
    
    Args:
        db_name: The database name to test (default: "default")
    
    Returns:
        JSON string with connection status
    """
    try:
        connection = get_db_connection(db_name)
        if connection.is_connected():
            db_info = connection.get_server_info()
            connection.close()
            
            config_info = get_database_info(db_name)
            return json.dumps({
                "status": "connected",
                "database": db_name,
                "server_version": db_info,
                "database_name": config_info['database'],
                "host": config_info['host'],
                "port": config_info['port']
            }, indent=2)
        else:
            return json.dumps({"status": "disconnected", "database": db_name}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e), "database": db_name}, indent=2)


def test_all_connections() -> str:
    """
    Test connections to all configured databases.
    
    Returns:
        JSON string with connection status for all databases
    """
    try:
        databases = get_available_databases()
        results = {}
        
        for db_name in databases:
            try:
                connection = get_db_connection(db_name)
                if connection.is_connected():
                    db_info = connection.get_server_info()
                    connection.close()
                    config_info = get_database_info(db_name)
                    results[db_name] = {
                        "status": "connected",
                        "server_version": db_info,
                        "database_name": config_info['database'],
                        "host": config_info['host'],
                        "port": config_info['port']
                    }
                else:
                    results[db_name] = {"status": "disconnected"}
            except Exception as e:
                results[db_name] = {"status": "error", "message": str(e)}
        
        return json.dumps({
            "database_connections": results,
            "total_databases": len(databases)
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


def query_to_csv(sql: str, filename: str = "", params: str = "", db_name: str = "default") -> str:
    """
    Execute a SELECT query and save the results to a CSV file.
    
    Args:
        sql: The SQL SELECT query to execute
        filename: Optional filename for the CSV file (if not provided, uses 'query_results_<db_name>.csv')
        params: Optional comma-separated parameters for parameterized queries (e.g., "value1,value2")
        db_name: The database name to query (default: "default")
    
    Returns:
        JSON string containing the CSV file path and number of rows exported
    """
    try:
        # Parse parameters if provided
        query_params = None
        if params.strip():
            query_params = tuple(param.strip() for param in params.split(','))
        
        # Execute the query
        results = execute_query(sql, query_params, db_name)
        
        if not results:
            return json.dumps({
                "message": "Query returned no results", 
                "rows_exported": 0,
                "database": db_name
            }, indent=2)
        
        # Set default filename if not provided
        if not filename.strip():
            filename = f"query_results_{db_name}.csv"
        elif not filename.endswith('.csv'):
            filename += '.csv'
        
        # Write results to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data rows
            for row in results:
                # Convert any non-string values to strings for CSV compatibility
                csv_row = {k: str(v) if v is not None else '' for k, v in row.items()}
                writer.writerow(csv_row)
        
        return json.dumps({
            "status": "success",
            "database": db_name,
            "csv_file": os.path.abspath(filename),
            "rows_exported": len(results),
            "columns": list(results[0].keys())
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)


def query_to_csv_string(sql: str, params: str = "", db_name: str = "default") -> str:
    """
    Execute a SELECT query and return the results as a CSV string.
    
    Args:
        sql: The SQL SELECT query to execute
        params: Optional comma-separated parameters for parameterized queries (e.g., "value1,value2")
        db_name: The database name to query (default: "default")
    
    Returns:
        JSON string containing the CSV data as a string and metadata
    """
    try:
        # Parse parameters if provided
        query_params = None
        if params.strip():
            query_params = tuple(param.strip() for param in params.split(','))
        
        # Execute the query
        results = execute_query(sql, query_params, db_name)
        
        if not results:
            return json.dumps({
                "message": "Query returned no results", 
                "csv_data": "", 
                "rows_exported": 0,
                "database": db_name
            }, indent=2)
        
        # Create CSV string in memory
        output = io.StringIO()
        fieldnames = results[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for row in results:
            # Convert any non-string values to strings for CSV compatibility
            csv_row = {k: str(v) if v is not None else '' for k, v in row.items()}
            writer.writerow(csv_row)
        
        csv_data = output.getvalue()
        output.close()
        
        return json.dumps({
            "status": "success",
            "database": db_name,
            "csv_data": csv_data,
            "rows_exported": len(results),
            "columns": list(results[0].keys())
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)