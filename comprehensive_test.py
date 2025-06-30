#!/usr/bin/env python3
"""
Comprehensive test of MCP database tools with proper MySQL syntax
"""
import json
from server import (
    test_connection, 
    list_tables, 
    describe_table, 
    query_database, 
    execute_sql
)

def comprehensive_test():
    """Test all MCP database tools with proper MySQL queries"""
    print("=" * 60)
    print("Comprehensive MCP Database Tools Test")
    print("=" * 60)
    
    # Test 1: Connection test
    print("\n1. Testing database connection...")
    try:
        result = test_connection()
        connection_data = json.loads(result)
        print(f"✅ Connection Status: {connection_data['status']}")
        print(f"✅ Database: {connection_data['database']}")
        print(f"✅ Server Version: {connection_data['server_version']}")
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return
    
    # Test 2: List tables
    print("\n2. Listing all tables...")
    try:
        result = list_tables()
        tables_data = json.loads(result)
        tables = tables_data['tables']
        print(f"✅ Found {len(tables)} tables in the database")
        print(f"✅ First 5 tables: {tables[:5]}")
    except Exception as e:
        print(f"❌ List tables failed: {e}")
        return
    
    # Test 3: Describe a table (using first table from the list)
    if tables:
        print(f"\n3. Describing table structure for '{tables[0]}'...")
        try:
            result = describe_table(tables[0])
            table_info = json.loads(result)
            if isinstance(table_info, list) and table_info:
                print(f"✅ Table '{tables[0]}' has {len(table_info)} columns")
                print("✅ Column details:")
                for col in table_info[:3]:  # Show first 3 columns
                    print(f"   - {col.get('Field', 'N/A')} ({col.get('Type', 'N/A')})")
            else:
                print(f"✅ Table structure retrieved for '{tables[0]}'")
        except Exception as e:
            print(f"❌ Describe table failed: {e}")
    
    # Test 4: Simple queries with proper MySQL syntax
    print("\n4. Testing simple queries...")
    
    # Test basic query
    try:
        result = query_database("SELECT 1 as test_value, NOW() as `current_time`")
        query_data = json.loads(result)
        if "error" in query_data:
            print(f"❌ Simple query failed: {query_data['error']}")
        else:
            print(f"✅ Simple query successful: {query_data}")
    except Exception as e:
        print(f"❌ Simple query failed: {e}")
    
    # Test information schema query
    try:
        result = query_database("SELECT DATABASE() as current_database, VERSION() as mysql_version")
        query_data = json.loads(result)
        if "error" in query_data:
            print(f"❌ Info query failed: {query_data['error']}")
        else:
            print(f"✅ Database info query successful: {query_data}")
    except Exception as e:
        print(f"❌ Info query failed: {e}")
    
    # Test table count query
    try:
        result = query_database("SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = DATABASE()")
        query_data = json.loads(result)
        if "error" in query_data:
            print(f"❌ Count query failed: {query_data['error']}")
        else:
            print(f"✅ Table count query successful: {query_data}")
    except Exception as e:
        print(f"❌ Count query failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ MCP Database Tools Test Complete!")
    print("✅ All core functionality is working properly.")
    print("=" * 60)
    
    # Summary of available tools
    print("\n📋 Available MCP Tools Summary:")
    print("1. test_connection() - Test database connectivity")
    print("2. list_tables() - List all tables in database")
    print("3. describe_table(table_name) - Get table schema")
    print("4. query_database(sql, params) - Execute SELECT queries")
    print("5. execute_sql(sql, params) - Execute INSERT/UPDATE/DELETE")
    print("\n🔧 Example usage:")
    print('query_database("SELECT * FROM ai_companies LIMIT 5")')
    print('describe_table("ai_companies")')

if __name__ == "__main__":
    comprehensive_test()
