# resources.py
import json
from database import execute_query, get_available_databases, get_database_info


def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


def get_all_databases() -> str:
    """Get all available databases with their configurations"""
    try:
        databases = get_available_databases()
        db_info = {}
        
        for db_name in databases:
            try:
                config = get_database_info(db_name)
                db_info[db_name] = {
                    "host": config['host'],
                    "port": config['port'],
                    "database_name": config['database'],
                    "user": config['user']
                }
            except Exception as e:
                db_info[db_name] = {"error": str(e)}
        
        return json.dumps({
            "available_databases": databases,
            "database_configurations": db_info,
            "total_databases": len(databases)
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


def get_all_tables(db_name: str = "default") -> str:
    """Get all tables from the specified database"""
    try:
        results = execute_query("SHOW TABLES", None, db_name)
        tables = [list(row.values())[0] for row in results]
        
        config = get_database_info(db_name)
        return json.dumps({
            "database": db_name,
            "database_name": config['database'],
            "host": config['host'],
            "port": config['port'],
            "tables": tables,
            "table_count": len(tables)
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)


def get_database_summary(db_name: str = "default") -> str:
    """Get summary information about a specific database"""
    try:
        # Get database configuration
        config = get_database_info(db_name)
        
        # Get table count
        table_results = execute_query("SHOW TABLES", None, db_name)
        table_count = len(table_results)
        
        # Get database size (if possible)
        size_query = """
        SELECT 
            ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'size_mb'
        FROM information_schema.tables 
        WHERE table_schema = %s
        """
        try:
            size_results = execute_query(size_query, (config['database'],), db_name)
            size_mb = size_results[0]['size_mb'] if size_results and size_results[0]['size_mb'] else 0
        except:
            size_mb = "N/A"
        
        return json.dumps({
            "database": db_name,
            "configuration": {
                "host": config['host'],
                "port": config['port'],
                "database_name": config['database'],
                "user": config['user']
            },
            "statistics": {
                "table_count": table_count,
                "size_mb": size_mb
            }
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "database": db_name}, indent=2)
