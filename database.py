# database.py
import mysql.connector
from mysql.connector import Error
import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Multiple database configurations
DB_CONFIGS = {
    'default': {
        'host': os.getenv('DB_HOST', '0.0.0.0'),
        'database': os.getenv('DB_NAME', 'rc'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASS', 'root@1345'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'autocommit': True
    }
}

# Load additional database configurations from environment variables
# Format: DB_CONFIG_<name>_HOST, DB_CONFIG_<name>_PORT, etc.
def load_additional_db_configs():
    """Load additional database configurations from environment variables"""
    configs = {}
    env_vars = os.environ
    
    # Find all database configuration prefixes
    db_prefixes = set()
    for key in env_vars.keys():
        if key.startswith('DB_CONFIG_') and '_' in key[10:]:
            prefix = key.split('_')[2]  # Extract database name
            db_prefixes.add(prefix)
    
    # Build configurations for each database
    for db_name in db_prefixes:
        config = {
            'host': env_vars.get(f'DB_CONFIG_{db_name}_HOST', '0.0.0.0'),
            'database': env_vars.get(f'DB_CONFIG_{db_name}_NAME', db_name.lower()),
            'user': env_vars.get(f'DB_CONFIG_{db_name}_USER', 'root'),
            'password': env_vars.get(f'DB_CONFIG_{db_name}_PASS', 'root@1345'),
            'port': int(env_vars.get(f'DB_CONFIG_{db_name}_PORT', '3306')),
            'autocommit': True
        }
        configs[db_name.lower()] = config
    
    return configs

# Load all database configurations
additional_configs = load_additional_db_configs()
DB_CONFIGS.update(additional_configs)

# Backward compatibility
DB_CONFIG = DB_CONFIGS['default']


def get_db_connection(db_name: str = 'default'):
    """Create and return a database connection for the specified database"""
    if db_name not in DB_CONFIGS:
        raise Exception(f"Database configuration '{db_name}' not found. Available: {list(DB_CONFIGS.keys())}")
    
    try:
        connection = mysql.connector.connect(**DB_CONFIGS[db_name])
        return connection
    except Error as e:
        raise Exception(f"Database connection failed for '{db_name}': {str(e)}")


def get_available_databases() -> List[str]:
    """Get list of available database configurations"""
    return list(DB_CONFIGS.keys())


def get_database_info(db_name: str = 'default') -> Dict[str, Any]:
    """Get database configuration information (without password)"""
    if db_name not in DB_CONFIGS:
        raise Exception(f"Database configuration '{db_name}' not found")
    
    config = DB_CONFIGS[db_name].copy()
    config['password'] = '***'  # Hide password
    return config


def execute_query(query: str, params: Optional[tuple] = None, db_name: str = 'default') -> List[Dict[str, Any]]:
    """Execute a SELECT query and return results as a list of dictionaries"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection(db_name)
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        return results
    except Error as e:
        raise Exception(f"Query execution failed on '{db_name}': {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def execute_non_query(query: str, params: Optional[tuple] = None, db_name: str = 'default') -> Dict[str, Any]:
    """Execute INSERT, UPDATE, DELETE queries and return affected rows count"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection(db_name)
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        affected_rows = cursor.rowcount
        return {
            "affected_rows": affected_rows,
            "last_insert_id": cursor.lastrowid if cursor.lastrowid else None
        }
    except Error as e:
        raise Exception(f"Query execution failed on '{db_name}': {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
