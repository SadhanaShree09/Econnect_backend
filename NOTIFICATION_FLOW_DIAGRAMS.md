# E-connect Notification Flow Diagrams

## 1. Direct Chat Message Flow

```
┌─────────────┐
│  User A     │
│  (Sender)   │
└──────┬──────┘
       │ 1. Sends message "Hello!"
       ▼
┌─────────────────────────────────┐
│  WebSocket: /ws/{userA_id}      │
│  - Message saved to MongoDB     │
│  - Timestamp added              │
└──────┬──────────────────────────┘
       │ 2. Broadcast message
       ▼
┌─────────────────────────────────┐
│  Server.py - websocket_endpoint │
│  - Send to User B via WS        │
│  - Create notification          │
└──────┬──────────────────────────┘
       │ 3. Create notification
       ▼
┌─────────────────────────────────┐
│  Mongo.py                       │
│  create_chat_message_notif()    │
│  - Check for duplicates         │
│  - Save to Notifications DB     │
│  - Send via WebSocket           │
└──────┬──────────────────────────┘
       │ 4. Real-time notification
       ▼
┌─────────────┐
│  User B     │
│  (Receiver) │
│  🔔 (1)     │ ← Notification appears
└─────────────┘
       │ 5. User clicks notification
       ▼
┌─────────────┐
│  Chat Page  │
│  Opens with │
│  User A     │
└─────────────┘
```

---

## 2. Group Chat Message Flow

```
┌─────────────┐
│  User A     │
│  (Sender)   │
└──────┬──────┘
       │ 1. Posts "Meeting at 3pm"
       ▼
┌─────────────────────────────────┐
│  WebSocket: /ws/group/{group_id}│
│  - Save to messages collection  │
│  - Get group members            │
└──────┬──────────────────────────┘
       │ 2. Broadcast to group
       ▼
┌─────────────────────────────────┐
│  Server.py - websocket_group    │
│  - Broadcast to all members     │
│  - Create notifications         │
└──────┬──────────────────────────┘
       │ 3. Create notifications
       ▼
┌─────────────────────────────────┐
│  Mongo.py                       │
│  create_group_chat_notif()      │
│  - Loop through members         │
│  - Exclude sender               │
│  - Send to each member          │
└──────┬──────────────────────────┘
       │ 4. Multiple notifications
       ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  User B     │   │  User C     │   │  User D     │
│  🔔 (1)     │   │  🔔 (1)     │   │  🔔 (1)     │
└─────────────┘   └─────────────┘   └─────────────┘
```

---

## 3. Document Assignment Flow

```
┌─────────────┐
│  HR Admin   │
│  (Assigner) │
└──────┬──────┘
       │ 1. Assigns "Aadhar Card"
       ▼
┌─────────────────────────────────┐
│  POST /assign_docs              │
│  - userIds: ["emp123"]          │
│  - docName: "Aadhar Card"       │
└──────┬──────────────────────────┘
       │ 2. Update user record
       ▼
┌─────────────────────────────────┐
│  MongoDB Users Collection       │
│  - Add to assigned_docs array   │
│  - Status: "Pending"            │
└──────┬──────────────────────────┘
       │ 3. Create notification
       ▼
┌─────────────────────────────────┐
│  Mongo.py                       │
│  create_doc_assignment_notif()  │
│  - Save notification            │
│  - Send via WebSocket           │
└──────┬──────────────────────────┘
       │ 4. Notify employee
       ▼
┌─────────────┐
│  Employee   │
│  John       │
│  🔔 (1)     │ ← "Aadhar Card assigned"
└─────────────┘
       │ 5. Clicks notification
       ▼
┌─────────────┐
│ OnboardDocs │
│ Page        │
│ - Aadhar    │ ← Status: Pending
│ - PAN Card  │
└─────────────┘
```

---

## 4. Document Upload & Review Flow

```
┌─────────────┐
│  Employee   │
│  John       │
└──────┬──────┘
       │ 1. Uploads Aadhar Card file
       ▼
┌─────────────────────────────────┐
│  POST /upload_document          │
│  - userid: "emp123"             │
│  - docName: "Aadhar Card"       │
│  - file: Binary(...)            │
└──────┬──────────────────────────┘
       │ 2. Save to GridFS
       ▼
┌─────────────────────────────────┐
│  MongoDB assignments_collection │
│  - Store file binary            │
│  - Get file_id                  │
└──────┬──────────────────────────┘
       │ 3. Update user record
       ▼
┌─────────────────────────────────┐
│  MongoDB Users Collection       │
│  - Status: "Uploaded"           │
│  - fileId: "file123"            │
└──────┬──────────────────────────┘
       │ 4. Notify reviewers
       ▼
┌─────────────────────────────────┐
│  Mongo.py                       │
│  create_doc_upload_notif()      │
│  - Find HR users                │
│  - Find employee's manager      │
│  - Send to all reviewers        │
└──────┬──────────────────────────┘
       │ 5. Multiple notifications
       ▼
┌─────────────┐           ┌─────────────┐
│  HR Admin   │           │  Manager    │
│  🔔 (1)     │ ← "John   │  🔔 (1)     │ ← "John
└─────────────┘    uploaded"└─────────────┘    uploaded"
       │                          │
       │ 6. HR reviews            │
       ▼                          │
┌─────────────────────────────────┐
│  PUT /review_document           │
│  - userId: "emp123"             │
│  - docName: "Aadhar Card"       │
│  - status: "Verified"           │
│  - remarks: "Approved"          │
└──────┬──────────────────────────┘
       │ 7. Update status
       ▼
┌─────────────────────────────────┐
│  MongoDB Users Collection       │
│  - Status: "Verified"           │
│  - remarks: "Approved"          │
│  - reviewedAt: timestamp        │
└──────┬──────────────────────────┘
       │ 8. Notify employee
       ▼
┌─────────────────────────────────┐
│  Mongo.py                       │
│  create_doc_review_notif()      │
│  - Status-based message         │
│  - Include remarks              │
└──────┬──────────────────────────┘
       │ 9. Employee notified
       ▼
┌─────────────┐
│  Employee   │
│  John       │
│  🔔 (1)     │ ← "Aadhar approved ✅"
└─────────────┘
```

---

## 5. Notification System Architecture

```
┌────────────────────────────────────────────────────────┐
│                  E-CONNECT PLATFORM                     │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌──────────────┐            │
│  │  Frontend    │         │   Backend    │            │
│  │  Components  │◄────────┤   Server.py  │            │
│  │              │ WebSocket│              │            │
│  │ - NotifBell  │         │ - Chat WS    │            │
│  │ - NotifDash  │         │ - Group WS   │            │
│  └──────────────┘         │ - APIs       │            │
│         ▲                 └───────┬──────┘            │
│         │                         │                    │
│         │ WebSocket               │ Function calls    │
│         │ Updates                 ▼                    │
│         │                 ┌──────────────┐            │
│         │                 │   Mongo.py   │            │
│         │                 │              │            │
│         │                 │ - Chat       │            │
│         │                 │   Notifs     │            │
│         │                 │ - Doc        │            │
│         │                 │   Notifs     │            │
│         │                 └───────┬──────┘            │
│         │                         │                    │
│         │                         │ Save & Broadcast  │
│         │                         ▼                    │
│         │                 ┌──────────────┐            │
│         │                 │   MongoDB    │            │
│         │                 │              │            │
│         │                 │ Notifications│            │
│         │                 │  Collection  │            │
│         │                 └───────┬──────┘            │
│         │                         │                    │
│         └─────────────────────────┘                    │
│              Real-time delivery via                    │
│              notification_manager                      │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## 6. Notification Lifecycle

```
START
  │
  ├─► [Action Occurs]
  │   - Chat message sent
  │   - Document assigned
  │   - Document uploaded
  │   - Document reviewed
  │
  ├─► [Validation]
  │   - Check user exists
  │   - Validate data
  │   - Get user names
  │
  ├─► [Duplicate Check]
  │   - Search recent notifications
  │   - Match criteria (sender, type, time)
  │   - Return existing if found
  │
  ├─► [Create Notification]
  │   - Build notification object
  │   - Add metadata
  │   - Determine priority
  │   - Set action_url
  │
  ├─► [Save to Database]
  │   - Insert into Notifications
  │   - Get notification_id
  │   - Timestamp with IST
  │
  ├─► [WebSocket Broadcast]
  │   - Send to user's WS connection
  │   - Update unread count
  │   - Real-time delivery
  │
  ├─► [Frontend Display]
  │   - Bell icon updates
  │   - Toast notification
  │   - Add to dashboard
  │
  └─► [User Interaction]
      ├─► Click notification
      │   - Navigate to action_url
      │   - Mark as read
      │   - Clear from unread
      │
      └─► Dismiss
          - Mark as read
          - Keep in history
END
```

---

## 7. Data Flow Diagram

```
╔════════════════════════════════════════════════════════╗
║                  USER ACTIONS                          ║
╚════════════════════════════════════════════════════════╝
         │                  │                  │
         │ Chat             │ Upload           │ Review
         │ Message          │ Document         │ Document
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ WebSocket       │ │ POST            │ │ PUT             │
│ /ws/{userid}    │ │ /upload_doc     │ │ /review_doc     │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼
         ╔═══════════════════════════════════════╗
         ║    Notification Creation Functions     ║
         ║                                        ║
         ║ • create_chat_message_notification()  ║
         ║ • create_document_upload_notification ║
         ║ • create_document_review_notification ║
         ╚═══════════════════════════════════════╝
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
         ┌─────────┐ ┌─────────┐ ┌─────────┐
         │ MongoDB │ │WebSocket│ │ Metadata│
         │  Save   │ │Broadcast│ │ Storage │
         └────┬────┘ └────┬────┘ └────┬────┘
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
              ╔═════════════════════╗
              ║   Frontend Render   ║
              ║                     ║
              ║ • Notification Bell ║
              ║ • Toast Message     ║
              ║ • Dashboard List    ║
              ╚═════════════════════╝
```

---

## 8. Priority & Routing Matrix

```
┌─────────────────┬──────────┬─────────────────────────┐
│ Notification    │ Priority │ Action URL              │
├─────────────────┼──────────┼─────────────────────────┤
│ Chat (Direct)   │ Medium   │ /User/Chat              │
│ Chat (Group)    │ Low      │ /User/Chat              │
│ Doc Assigned    │ High     │ /User/OnboardingDocs    │
│ Doc Uploaded    │ High     │ /admin (HR)             │
│                 │          │ /Manager/OnboardingDocs │
│ Doc Approved    │ Medium   │ /User/OnboardingDocs    │
│ Doc Rejected    │ High     │ /User/OnboardingDocs    │
└─────────────────┴──────────┴─────────────────────────┘
```

---

## 9. Error Handling Flow

```
[Action Triggered]
      │
      ▼
[Try Create Notification]
      │
      ├─► Success
      │   └─► Notification created
      │       └─► User notified
      │
      └─► Error
          ├─► Log error
          │   "Error creating notification: ..."
          │
          ├─► Continue normal flow
          │   (Chat still sent, doc still uploaded)
          │
          └─► User experience unaffected
              (Core functionality preserved)
```

---

## 10. Real-time Notification Delivery

```
[Notification Created in DB]
         │
         ▼
[notification_manager.send_personal_notification()]
         │
         ├─► User Online?
         │   │
         │   ├─► YES
         │   │   └─► Send via WebSocket
         │   │       └─► Instant delivery (~10ms)
         │   │           └─► Toast + Bell update
         │   │
         │   └─► NO
         │       └─► Store in DB only
         │           └─► User sees on next login
         │
         └─► Update unread count
             └─► Broadcast count to user
                 └─► Bell icon shows number
```

---

**These diagrams illustrate the complete flow of notifications through the E-connect system, from action trigger to user interaction.**

**Date:** October 6, 2025  
**Version:** 2.0
