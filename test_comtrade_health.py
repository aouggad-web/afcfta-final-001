#!/usr/bin/env python3
"""
Test script to verify the Comtrade health endpoint
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_health_check_function():
    """Test the health_check function directly"""
    print("Testing Comtrade service health check function...")
    
    from services.comtrade_service import comtrade_service
    
    # Get service status
    status = comtrade_service.get_service_status()
    print(f"\n✓ Service Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Try health check (will make a test API call if keys are configured)
    print(f"\n✓ Running health check...")
    health = comtrade_service.health_check()
    print(f"\n✓ Health Status:")
    for key, value in health.items():
        print(f"  {key}: {value}")
    
    return health

def test_endpoint_response():
    """Test that the endpoint logic works"""
    print("\n" + "="*60)
    print("Testing endpoint response logic...")
    
    from services.comtrade_service import comtrade_service
    from datetime import datetime
    
    try:
        health_status = comtrade_service.health_check()
        response = {
            "status": "operational" if health_status["connected"] else "error",
            "using_key": "secondary" if health_status["using_secondary"] else "primary",
            "api_calls_today": health_status["calls_today"],
            "rate_limit_remaining": health_status["rate_limit_remaining"],
            "last_error": health_status["last_error"],
            "primary_key_configured": health_status["primary_key_configured"],
            "secondary_key_configured": health_status["secondary_key_configured"],
            "timestamp": health_status["timestamp"]
        }
        print("\n✓ Endpoint Response:")
        import json
        print(json.dumps(response, indent=2))
        return response
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("COMTRADE API HEALTH CHECK TEST")
    print("="*60)
    
    try:
        health = test_health_check_function()
        response = test_endpoint_response()
        
        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        
        if health and response:
            print("✅ All tests passed!")
            print(f"\nAPI Status: {response['status']}")
            print(f"Active Key: {response['using_key']}")
            print(f"Primary Configured: {response['primary_key_configured']}")
            print(f"Secondary Configured: {response['secondary_key_configured']}")
            
            if not response['primary_key_configured'] and not response['secondary_key_configured']:
                print("\n⚠️  WARNING: No API keys configured")
                print("   Set COMTRADE_API_KEY or COMTRADE_API_KEY_SECONDARY environment variables")
            
            sys.exit(0)
        else:
            print("❌ Tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
