#!/usr/bin/env python3
"""
Test script to verify MCP database tools functionality
"""
import json
from tools import (
    test_connection, 
    list_tables, 
    describe_table, 
    query_database, 
    execute_sql
)

def test_mcp_tools():
    """Test all MCP database tools"""
    print("=" * 50)
    print("Testing MCP Database Tools")
    print("=" * 50)
    
    # Test 1: Connection test
    print("\n1. Testing database connection...")
    try:
        result = test_connection()
        print("Connection test result:")
        print(result)
    except Exception as e:
        print(f"Connection test failed: {e}")
    
    # Test 2: List tables
    print("\n2. Listing all tables...")
    try:
        result = list_tables()
        print("Tables in database:")
        print(result)
    except Exception as e:
        print(f"List tables failed: {e}")
    
    # Test 3: Simple query
    print("\n3. Testing simple query...")
    try:
        result = query_database("SELECT 1 as test_value, NOW() as `current_time`")
        print("Simple query result:")
        print(result)
    except Exception as e:
        print(f"Simple query failed: {e}")
    
    print("\n" + "=" * 50)
    print("MCP Database Tools Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_mcp_tools()
