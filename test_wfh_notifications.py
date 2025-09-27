#!/usr/bin/env python3
"""
Test script to verify WFH notification system is working correctly
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notification_automation import (
    notify_wfh_submitted_to_manager,
    notify_wfh_recommended_to_hr,
    notify_wfh_approved_to_employee,
    notify_wfh_rejected_to_employee
)

async def test_wfh_notifications():
    """Test the WFH notification functions"""
    print("🧪 Testing WFH notification system...")
    
    # Test data
    employee_name = "Test Employee"
    employee_id = "66f02b7d6f5a4b2c8d123456"  # Sample ObjectId
    manager_id = "66f02b7d6f5a4b2c8d123457"   # Sample ObjectId
    request_date_from = "01-10-2025"
    request_date_to = "03-10-2025"
    wfh_id = "66f02b7d6f5a4b2c8d123458"      # Sample ObjectId
    
    try:
        # Test 1: Employee submits WFH request to manager
        print("\n1. Testing: Employee WFH submission notification to manager...")
        result1 = await notify_wfh_submitted_to_manager(
            employee_name=employee_name,
            employee_id=employee_id,
            request_date_from=request_date_from,
            request_date_to=request_date_to,
            manager_id=manager_id,
            wfh_id=wfh_id
        )
        print(f"   Result: {'✅ SUCCESS' if result1 else '❌ FAILED'}")
        
        # Test 2: Manager recommends WFH to HR
        print("\n2. Testing: Manager WFH recommendation notification to HR...")
        result2 = await notify_wfh_recommended_to_hr(
            employee_name=employee_name,
            employee_id=employee_id,
            request_date_from=request_date_from,
            request_date_to=request_date_to,
            recommended_by="Test Manager",
            wfh_id=wfh_id
        )
        print(f"   Result: {'✅ SUCCESS' if result2 else '❌ FAILED'}")
        
        # Test 3: HR approves WFH request
        print("\n3. Testing: HR WFH approval notification to employee...")
        result3 = await notify_wfh_approved_to_employee(
            userid=employee_id,
            employee_name=employee_name,
            request_date_from=request_date_from,
            request_date_to=request_date_to,
            approved_by="HR",
            wfh_id=wfh_id
        )
        print(f"   Result: {'✅ SUCCESS' if result3 else '❌ FAILED'}")
        
        # Test 4: HR rejects WFH request
        print("\n4. Testing: HR WFH rejection notification to employee...")
        result4 = await notify_wfh_rejected_to_employee(
            userid=employee_id,
            employee_name=employee_name,
            request_date_from=request_date_from,
            request_date_to=request_date_to,
            rejected_by="HR",
            reason="Business requirements",
            wfh_id=wfh_id
        )
        print(f"   Result: {'✅ SUCCESS' if result4 else '❌ FAILED'}")
        
        # Summary
        total_tests = 4
        passed_tests = sum([result1, result2, result3, result4])
        print(f"\n📊 Test Summary: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All WFH notification tests passed! The system is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the error messages above.")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_wfh_notifications())