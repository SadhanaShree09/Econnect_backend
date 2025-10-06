#!/usr/bin/env python3
"""
Test Script for Chat and Document Review Notifications
Tests the new notification functions to ensure they work correctly
"""

import asyncio
import sys
from datetime import datetime
from Mongo import (
    create_chat_message_notification,
    create_group_chat_notification,
    create_document_assignment_notification,
    create_document_upload_notification,
    create_document_review_notification,
    Users,
    get_notifications
)

async def test_chat_notifications():
    """Test chat notification functions"""
    print("\n" + "="*60)
    print("TESTING CHAT NOTIFICATIONS")
    print("="*60)
    
    # Test 1: Direct Message Notification
    print("\n1️⃣ Testing Direct Chat Message Notification...")
    try:
        notification_id = await create_chat_message_notification(
            sender_id="test_sender_001",
            receiver_id="test_receiver_001",
            sender_name="Test Sender",
            message_preview="Hello! This is a test message for notification system.",
            chat_type="direct"
        )
        if notification_id:
            print(f"✅ Direct chat notification created: {notification_id}")
        else:
            print("❌ Failed to create direct chat notification")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Group Message Notification
    print("\n2️⃣ Testing Group Chat Message Notification...")
    try:
        notification_ids = await create_group_chat_notification(
            sender_id="test_sender_001",
            group_id="test_group_001",
            sender_name="Test Sender",
            group_name="Test Group",
            message_preview="Team meeting at 3pm today!",
            member_ids=["test_member_001", "test_member_002", "test_member_003"]
        )
        if notification_ids:
            print(f"✅ Group chat notifications created: {len(notification_ids)} members notified")
        else:
            print("❌ Failed to create group chat notifications")
    except Exception as e:
        print(f"❌ Error: {e}")

async def test_document_notifications():
    """Test document notification functions"""
    print("\n" + "="*60)
    print("TESTING DOCUMENT NOTIFICATIONS")
    print("="*60)
    
    # Test 1: Document Assignment Notification
    print("\n1️⃣ Testing Document Assignment Notification...")
    try:
        notification_id = await create_document_assignment_notification(
            userid="test_employee_001",
            doc_name="Test Aadhar Card",
            assigned_by_name="HR Admin",
            assigned_by_id="test_hr_001"
        )
        if notification_id:
            print(f"✅ Document assignment notification created: {notification_id}")
        else:
            print("❌ Failed to create document assignment notification")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Document Upload Notification
    print("\n2️⃣ Testing Document Upload Notification...")
    try:
        notification_ids = await create_document_upload_notification(
            userid="test_employee_001",
            doc_name="Test Aadhar Card",
            uploaded_by_name="Test Employee",
            uploaded_by_id="test_employee_001",
            reviewer_ids=["test_hr_001", "test_manager_001"]
        )
        if notification_ids:
            print(f"✅ Document upload notifications created: {len(notification_ids)} reviewers notified")
        else:
            print("❌ Failed to create document upload notifications")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Document Review - Approved
    print("\n3️⃣ Testing Document Review Notification (Approved)...")
    try:
        notification_id = await create_document_review_notification(
            userid="test_employee_001",
            doc_name="Test Aadhar Card",
            reviewer_name="HR Admin",
            reviewer_id="test_hr_001",
            status="Verified",
            remarks="Document is clear and verified"
        )
        if notification_id:
            print(f"✅ Document review (approved) notification created: {notification_id}")
        else:
            print("❌ Failed to create document review notification")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Document Review - Rejected
    print("\n4️⃣ Testing Document Review Notification (Rejected)...")
    try:
        notification_id = await create_document_review_notification(
            userid="test_employee_001",
            doc_name="Test PAN Card",
            reviewer_name="HR Admin",
            reviewer_id="test_hr_001",
            status="Rejected",
            remarks="Image is blurry, please upload a clear copy"
        )
        if notification_id:
            print(f"✅ Document review (rejected) notification created: {notification_id}")
        else:
            print("❌ Failed to create document review notification")
    except Exception as e:
        print(f"❌ Error: {e}")

async def test_duplicate_prevention():
    """Test duplicate notification prevention"""
    print("\n" + "="*60)
    print("TESTING DUPLICATE PREVENTION")
    print("="*60)
    
    print("\n🔄 Sending same notification twice within 30 seconds...")
    
    # First notification
    notification_id_1 = await create_chat_message_notification(
        sender_id="test_sender_002",
        receiver_id="test_receiver_002",
        sender_name="Duplicate Test Sender",
        message_preview="Testing duplicate prevention",
        chat_type="direct"
    )
    
    # Immediate duplicate
    notification_id_2 = await create_chat_message_notification(
        sender_id="test_sender_002",
        receiver_id="test_receiver_002",
        sender_name="Duplicate Test Sender",
        message_preview="Testing duplicate prevention",
        chat_type="direct"
    )
    
    if notification_id_1 == notification_id_2:
        print("✅ Duplicate prevention working - same notification ID returned")
    else:
        print("⚠️ Different notification IDs - duplicate may have been created")

async def verify_notifications_in_db():
    """Verify notifications were created in database"""
    print("\n" + "="*60)
    print("VERIFYING NOTIFICATIONS IN DATABASE")
    print("="*60)
    
    # Check chat notifications
    print("\n📊 Chat Notifications:")
    chat_notifs = get_notifications("test_receiver_001", notification_type="chat", limit=10)
    print(f"   Found {len(chat_notifs)} chat notifications")
    
    # Check document notifications
    print("\n📊 Document Notifications:")
    doc_notifs = get_notifications("test_employee_001", notification_type="document", limit=10)
    print(f"   Found {len(doc_notifs)} document notifications")
    
    # Display sample notification
    if doc_notifs:
        print("\n📋 Sample Document Notification:")
        sample = doc_notifs[0]
        print(f"   Title: {sample.get('title')}")
        print(f"   Message: {sample.get('message')}")
        print(f"   Priority: {sample.get('priority')}")
        print(f"   Type: {sample.get('type')}")
        print(f"   Read: {sample.get('is_read')}")

async def main():
    """Main test runner"""
    print("\n" + "🧪 "*20)
    print("CHAT & DOCUMENT NOTIFICATION TEST SUITE")
    print("🧪 "*20)
    print(f"\nTest started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all tests
        await test_chat_notifications()
        await test_document_notifications()
        await test_duplicate_prevention()
        await verify_notifications_in_db()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        print("\n⚠️ Note: These are test notifications. You can delete them from")
        print("   the database if needed using MongoDB commands.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
