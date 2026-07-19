# User Payout Management System

A FastAPI-based backend service that manages affiliate payouts, advances, sale reconciliation, and user withdrawals while maintaining a consistent withdrawable balance.

---

# Functional Requirements

## Core Features

- Manage affiliate sales
- Advance payout (10% of pending earnings)
- Sale reconciliation
- Final payout calculation
- User withdrawals
- Failed payout recovery

## Business Rules

- Advance payout is credited only once per sale.
- Advance amount is fixed at **10%** of the sale earning.
- Remaining payout is credited when the sale is approved.
- Rejected sales reverse any previously credited advance.
- Users may initiate only one withdrawal every **24 hours**.
- Failed, cancelled, or rejected withdrawals refund the deducted amount back to the user's withdrawable balance.
- Approval, rejection, and withdrawal status transitions are implemented as **idempotent** operations.

---

# Core Entities

## User

Represents an affiliate who earns commissions through sales.

Responsibilities:

- Owns sales
- Initiates withdrawals
- Maintains withdrawable balance

---

## Sale

Represents an affiliate sale.

Responsibilities:

- Stores commission earned
- Tracks reconciliation status
- Tracks advance payout eligibility

---

## Brand

Represents the merchant or affiliate partner associated with a sale.

Responsibilities:

- Owns affiliate sales
- Groups sales by merchant

---

## Withdrawal

Represents a withdrawal request initiated by a user.

Responsibilities:

- Tracks withdrawal lifecycle
- Supports payout recovery on failure

---

# Database Schema

## User

Tracks the user's current withdrawable balance.

```text
User
----
id                      INTEGER (PK)
name                    VARCHAR
withdrawable_balance    DECIMAL(10,2)

created_at              TIMESTAMP
updated_at              TIMESTAMP
```

---

## Brand

```text
Brand
-----
id                      INTEGER (PK)
name                    VARCHAR
```

---

## Sale

```text
Sale
----
id                      INTEGER (PK)

user_id                 INTEGER (FK -> User.id)
brand_id                INTEGER (FK -> Brand.id)

earning                 DECIMAL(10,2)
advance_amount          DECIMAL(10,2)

status                  ENUM(
                            PENDING,
                            APPROVED,
                            REJECTED
                        )

advance_added           BOOLEAN

created_at              TIMESTAMP
updated_at              TIMESTAMP
```

### Notes

- **earning** stores the total commission for the sale.
- **advance_amount** is stored explicitly so historical data remains correct even if the advance percentage changes in the future.
- **advance_added** indicates whether the advance has already been credited.

---

## Withdrawal

```text
Withdrawal
----------
id                      INTEGER (PK)

user_id                 INTEGER (FK -> User.id)

amount                  DECIMAL(10,2)

status                  ENUM(
                            INITIATED,
                            SUCCESS,
                            FAILED,
                            CANCELLED,
                            REJECTED
                        )

failure_reason          TEXT NULL

created_at              TIMESTAMP
updated_at              TIMESTAMP
```

---

# Entity Relationships

```
User 1 ------ * Sale

User 1 ------ * Withdrawal

Brand 1 ----- * Sale
```

---

# Balance Update Rules

The user's `withdrawable_balance` is maintained incrementally.

| Event | Balance Update |
|-------|----------------|
| Pending sale becomes eligible for advance | `+ advance_amount` |
| Pending → Approved | `+ (earning - advance_amount)` |
| Pending → Rejected | `- advance_amount` |
| Withdrawal initiated | `- withdrawal_amount` |
| Withdrawal failed / cancelled / rejected | `+ withdrawal_amount` |

The balance is maintained as a wallet. Credits and debits are applied incrementally, allowing balance lookups in constant time without replaying historical transactions.

---

# Project Structure

```
app/
│
├── api/
│   ├── sales.py
│   ├── withdrawals.py
│   ├── users.py
│   └── jobs.py
│
├── services/
│   ├── sale_service.py
│   ├── withdrawal_service.py
│   └── balance_service.py
│
├── repositories/
│   ├── sale_repository.py
│   ├── withdrawal_repository.py
│   ├── user_repository.py
│   └── brand_repository.py
│
├── models/
│
├── schemas/
│
├── db/
│
├── exceptions/
│
├── main.py
│
└── tests/
```

---

# Low-Level Design

```
                 FastAPI
                    │
             API Routers
                    │
       ┌────────────┴────────────┐
       │                         │
 SaleService          WithdrawalService
       │                         │
       └────────────┬────────────┘
                    │
             BalanceService
                    │
            Repository Layer
                    │
             SQLAlchemy ORM
                    │
                 SQLite
```

### Responsibilities

- **Routers** handle HTTP requests and responses.
- **Services** implement business rules.
- **Repositories** encapsulate database operations.
- **Models** represent persisted entities.
- **Schemas** define request/response contracts.
- **BalanceService** centralizes wallet updates.

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/sales` | Create a pending sale |
| GET | `/sales/{id}` | Retrieve sale details |
| POST | `/jobs/process-advances` | Credit pending advances |
| POST | `/sales/{id}/approve` | Approve sale |
| POST | `/sales/{id}/reject` | Reject sale |
| POST | `/withdrawals` | Create withdrawal |
| GET | `/withdrawals/{id}` | Retrieve withdrawal |
| POST | `/withdrawals/{id}/success` | Mark withdrawal successful |
| POST | `/withdrawals/{id}/failure` | Mark withdrawal failed |
| GET | `/users/{id}/balance` | Retrieve withdrawable balance |

---

# Error Handling

The API handles the following scenarios:

- User not found
- Brand not found
- Sale not found
- Withdrawal not found
- Insufficient withdrawable balance
- Withdrawal cooldown violation

Business operations such as sale approval, rejection, and withdrawal completion are implemented as **idempotent** endpoints to safely support retries.

---

# Design Decisions & Trade-offs

### Repository-Service Architecture

Business logic is isolated from persistence logic by introducing a service layer above repositories. This separation improves maintainability and testability.

### Incremental Wallet

Instead of recomputing balances from historical transactions, the current withdrawable balance is stored on the `User` entity and updated incrementally after every business event.

**Advantages**

- O(1) balance lookup
- Simple withdrawal validation
- Easy API implementation

**Trade-off**

Every state transition must correctly update the balance to maintain consistency.

### Stored Advance Amount

Although the advance is currently always 10%, the computed advance is persisted with each sale. This preserves historical correctness if payout rules change in the future.

### Idempotent Operations

Approval, rejection, and withdrawal status updates are idempotent. Repeating the same request does not alter the system state, making retries safe.

### Background Processing

Advance payouts are exposed through a `/jobs/process-advances` endpoint to simulate a scheduled background worker. In production this would typically be implemented using a scheduler such as Celery, APScheduler, or a cron job.

### SQLite

SQLite was chosen for simplicity and rapid setup. The repository layer keeps the persistence implementation isolated, allowing migration to PostgreSQL or another relational database with minimal changes.

---

# Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

Interactive API documentation

```
http://localhost:8000/docs
```
