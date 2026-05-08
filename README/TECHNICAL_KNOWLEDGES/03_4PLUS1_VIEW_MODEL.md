# 4+1 View Model Implementation Guide

**Reference**: Philippe Kruchten (1995) | **Adapted for**: Clean Architecture & DDD  
**Owner**: Mr. Đức | **Last Updated**: May 9, 2026

---

## 📖 What is 4+1 View Model?

4+1 View Model solves **stakeholder misalignment** by describing a system through 5 distinct viewpoints:

Each view focuses on different concerns and serves different stakeholders.  
The "+1" (Scenarios) validates consistency across all 4 views.

---

## 🎯 Why Use It?

### The Problem It Solves

Modern systems have many moving parts viewed by different people:
- **Product Owner** cares about: features, user journeys, business value
- **Developer** cares about: code structure, maintainability, testability
- **DevOps/Ops** cares about: deployment, scaling, reliability, cost
- **Architect** cares about: consistency, boundaries, evolution

If you try to fit all this in **one diagram**, you get **spaghetti** that nobody understands.

### The Solution

Separate concerns into clear views. Each view answers specific questions:

1. **Scenario (Use Case) View** → "What do users need to do?"
2. **Logical View** → "What is the business logic?"
3. **Development View** → "How should code be organized?"
4. **Process View** → "How does it run at runtime?"
5. **Physical View** → "Where is it deployed?"

---

## 📊 The Five Views

### 1️⃣ SCENARIO VIEW (Use Case / Business)

**Purpose**: Describe major user journeys and business flows.

**Answers**: 
- What can users do with the system?
- What are critical business processes?
- How do actors interact with the system?

**Components**:
- **Use Cases**: "Place Order", "Process Payment", "Generate Report"
- **Actors**: User, Admin, System, External Service
- **Preconditions**: What must be true before starting
- **Postconditions**: What's true after completion
- **Flows**: Normal flow, alternative flows, exception flows

**Example**:
```
Use Case: Place Order

Actors: Customer, Payment Gateway

Preconditions:
- Customer logged in
- Cart has items

Normal Flow:
1. Customer clicks Checkout
2. System shows order summary
3. Customer confirms
4. System requests Payment Gateway
5. Payment succeeds
6. System confirms order
7. Notification sent

Exception Flow:
- Payment failed → Order marked Pending Payment
- Customer timeout → Order cancelled

Postconditions:
- Order saved
- Inventory reserved
- Customer notified
```

**Audience**: Product Manager, Business Analyst, Customer, Tech Lead

---

### 2️⃣ LOGICAL VIEW (Domain Model)

**Purpose**: Describe the business domain in code terms (without implementation details).

**Answers**:
- What are the key concepts (Entities, Value Objects)?
- What are the business rules?
- How do concepts relate?

**Components**:
- **Bounded Context**: A clear business domain boundary
- **Aggregate**: Cluster of entities treated as unit
- **Entity**: Object with identity and lifecycle
- **Value Object**: Immutable concept defined by its value
- **Domain Service**: Business logic that doesn't fit in Entity/VO
- **Domain Event**: Significant business event

**Example - E-Commerce**:
```
Bounded Context: Order Management

Aggregates:
├── Order (Root)
│   ├── orderId (unique)
│   ├── customer: Customer (reference)
│   ├── items: OrderItem[] (part of aggregate)
│   └── status: OrderStatus (enum)
│
├── Payment (separate Aggregate)
│   ├── paymentId
│   ├── amount
│   └── status
│
└── Inventory (separate Aggregate)
    ├── product
    └── quantity

Entities:
- Order (has identity across time)
- OrderItem (identity only within Order)
- Payment (has independent identity)

Value Objects:
- Money (amount + currency, immutable)
- OrderStatus (enum: PENDING, CONFIRMED, SHIPPED)
- Address (street, city, country - immutable)

Business Rules:
- Order must have at least 1 item
- Total amount = sum of item amounts
- Payment must match Order total ± tax
- Can only cancel PENDING orders
- Inventory reserved after payment confirmed

Domain Events:
- OrderCreated
- PaymentProcessed
- OrderShipped
- OrderCancelled
```

**Sơ đồ**: UML Class Diagram (without implementation details)

**Audience**: Product Manager, Business Analyst, Architect, Senior Developer

---

### 3️⃣ DEVELOPMENT VIEW (Code Structure)

**Purpose**: Describe how code is organized and structured.

**Answers**:
- What modules exist and their responsibilities?
- What are the layers?
- How do modules depend on each other?
- What's the package structure?

**Components**:
- **Layer**: Horizontal slice (Presentation, Application, Domain, Infrastructure)
- **Module**: Vertical slice or business domain (Order, Payment, User)
- **Package**: Logical grouping of classes
- **Library**: Reusable code shared across modules

**Example - Layered Architecture**:
```
src/
├── presentation/
│   ├── controllers/
│   │   ├── OrderController.java
│   │   └── PaymentController.java
│   └── dtos/
│       ├── OrderDTO.java
│       └── PaymentDTO.java
│
├── application/
│   ├── services/
│   │   ├── PlaceOrderUseCase.java
│   │   └── ProcessPaymentUseCase.java
│   └── ports/
│       ├── OrderRepository.java (interface)
│       └── PaymentGateway.java (interface)
│
├── domain/
│   ├── entities/
│   │   ├── Order.java
│   │   └── OrderItem.java
│   ├── valueobjects/
│   │   ├── OrderStatus.java
│   │   └── Money.java
│   └── services/
│       └── OrderValidator.java
│
└── infrastructure/
    ├── persistence/
    │   ├── OrderRepositoryImpl.java
    │   └── OrderJpaEntity.java
    └── external/
        ├── StripePaymentGateway.java
        └── MailgunEmailService.java
```

**Dependency Rule**: 
- Presentation → Application → Domain ← Infrastructure
- Domain knows nothing of outer layers
- Infrastructure is pluggable/replaceable

**Sơ đồ**: Package/Module Dependency Diagram

**Audience**: Developer, Architect, Tech Lead

---

### 4️⃣ PROCESS VIEW (Runtime Behavior)

**Purpose**: Describe how the system behaves when running (concurrency, async, failures).

**Answers**:
- How do components communicate?
- How is concurrency handled?
- What happens when something fails?
- How does scaling work?

**Components**:
- **Process**: Running service/component (OrderService, PaymentService, Worker)
- **Message**: Communication between processes
- **Queue**: Buffered async communication
- **Failover**: Backup when primary fails

**Example - E-Commerce Order Processing**:
```
Scenario: Customer places order during peak load

Timeline:
┌─────────────────────────────────────────────────────────────┐
│ t=0: Customer clicks "Place Order"                          │
│ API Gateway receives request                                │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ t=10ms: Authentication checked (Auth Service)               │
│ Authorization verified                                       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ t=50ms: Order Service processes (transactional)             │
│ Order created in database                                   │
│ Publishes: OrderCreated event to Message Bus                │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ t=60ms: Response sent to client (order confirmed)           │
│ Async processing continues in background                    │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────┬──────────────────────┬───────────────┐
│                      │                      │               │
▼                      ▼                      ▼               ▼
Inventory          Payment Service      Email Service      Analytics
Worker             (Process Payment)     (Send Confirm)     (Track Event)
- Reserve stock    - Request Gateway     - Generate email   - Log metrics
- Queue update     - Retry on failure    - Queue email      - Update dashboard
- Publish event    - Publish result      - Send async

If Payment Fails:
├── Circuit breaker trips (after 5 failures)
├── Fallback: User gets PENDING_PAYMENT status
├── Retry scheduled (exponential backoff)
└── Alert sent to Ops team
```

**Sơ đồ**: Sequence Diagram, State Machine Diagram, Deployment Diagram

**Audience**: Developer, QA/Tester, DevOps, Tech Lead

---

### 5️⃣ PHYSICAL VIEW (Infrastructure & Deployment)

**Purpose**: Describe where and how the system is physically deployed.

**Answers**:
- Where do components run?
- How is load balanced?
- How is data replicated?
- What's the disaster recovery strategy?

**Components**:
- **Node**: Server, VM, container, or machine
- **Connection**: Network link between nodes
- **Storage**: Database, cache, file storage

**Example - E-Commerce Deployment**:
```
┌─────────────────────────────────────────────────────────────┐
│                     Internet / CDN                          │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│              Load Balancer (AWS ELB)                         │
│              SSL/TLS termination                             │
└──────────┬──────────────────────────────────────────┬────────┘
           ↓                                          ↓
    ┌─────────────────┐              ┌─────────────────────┐
    │ Web Server 1    │              │  Web Server 2       │
    │ (Kubernetes Pod)│              │ (Kubernetes Pod)    │
    │ - Express app   │              │ - Express app       │
    └────────┬────────┘              └─────────────┬───────┘
             └──────────────┬──────────────────────┘
                            ↓
              ┌──────────────────────────────┐
              │  Shared Services (VPC)       │
              ├──────────────────────────────┤
              │ - PostgreSQL Cluster         │
              │ - Redis Cluster (cache)      │
              │ - RabbitMQ (message broker)  │
              │ - Elasticsearch (logging)    │
              └──────────────────────────────┘
                            ↓
              ┌──────────────────────────────┐
              │  External Services           │
              ├──────────────────────────────┤
              │ - Stripe (Payment gateway)   │
              │ - AWS S3 (File storage)      │
              │ - SendGrid (Email)           │
              │ - Datadog (Monitoring)       │
              └──────────────────────────────┘

High Availability:
├── Multi-zone deployment (us-east-1a, 1b, 1c)
├── Database replication: Primary → Replica
├── Backup: Daily snapshots to separate region
├── Failover: Automatic if primary zone fails (5 min RTO)
└── Monitoring: 24/7 alerts for SLA violations
```

**Sơ đồ**: Deployment Diagram, Network Topology

**Audience**: DevOps, SRE, Infrastructure Architect, Tech Lead, Operations

---

## ✅ How to Apply 4+1 for Your Project

### Step 1: Start with Scenario View
Understand what users need to do. Don't code yet.
- Document 3-5 critical use cases
- Create simple flow diagrams
- Validate with Product/Business

### Step 2: Design Logical View
Map business concepts to your domain.
- Identify Bounded Contexts
- Define Aggregates and Entities
- Document business rules

### Step 3: Design Development View
Organize code to support the domain.
- Define layers
- Assign modules
- Plan dependencies
- Ensure Domain Layer is isolated

### Step 4: Design Process View
Plan runtime behavior.
- Identify services/components
- Plan async flows
- Handle failures
- Plan scaling

### Step 5: Design Physical View
Plan infrastructure.
- Deployment topology
- HA/DR strategy
- Monitoring & alerting

### Step 6: Validate with Scenarios (+1)
Pick critical scenarios and trace through all views.
- Scenario → which use case?
- Logical → which aggregates involved?
- Development → which modules?
- Process → which services communicate?
- Physical → which servers touched?

**If trace breaks down → redesign that view.**

---

## 🚀 Example: Building a Microservices E-Commerce System

### Scenario View
```
Use Case: Customer checkout and payment
- Customer selects items
- Customer enters shipping address
- Customer pays
- Order confirmed and inventory reserved
```

### Logical View
```
Bounded Contexts:
├── Order Context
├── Payment Context
├── Inventory Context
└── Shipping Context

Order Aggregate:
- Order (root)
- OrderItem (entity)
- OrderStatus (value object)
```

### Development View
```
Module Structure:
├── order-service/
│   ├── api/ (controllers)
│   ├── application/ (use cases)
│   ├── domain/ (business logic)
│   └── infrastructure/ (database)
├── payment-service/
├── inventory-service/
└── shared-libs/
    ├── exceptions/
    └── utils/
```

### Process View
```
Runtime Flow:
1. API Gateway receives request
2. Order Service creates order
3. Publishes OrderCreated event
4. Payment Service consumes event (async)
5. Payment Service calls external gateway
6. Payment result published
7. Inventory Service consumes, reserves stock
```

### Physical View
```
Infrastructure:
├── Kubernetes cluster (3 zones)
├── Load balancer
├── 3+ pods per service (auto-scaling)
├── PostgreSQL cluster (replicated)
├── Redis (cache)
├── Kafka (event bus)
└── Monitoring stack (Prometheus, Grafana)
```

### Scenarios Validation
Pick scenario: "Place order with payment"
- ✅ Scenario: Order checkout flow defined
- ✅ Logical: Order, Payment aggregates aligned
- ✅ Development: Services separate, clean boundaries
- ✅ Process: Async communication, failover handled
- ✅ Physical: Multi-zone, load balanced

---

## 🎓 Common Mistakes to Avoid

❌ **Mistake 1**: Treating 4+1 as sequential
- **Fix**: Views are parallel perspectives, not phases. Design them together.

❌ **Mistake 2**: Over-detailed diagrams
- **Fix**: Simplify. One diagram per view, focus on key relationships.

❌ **Mistake 3**: Ignoring Scenario (+1) view
- **Fix**: Scenarios validate all other views. Never skip them.

❌ **Mistake 4**: Mismatching views
- **Fix**: If Logical has 5 bounded contexts but Development has 2 modules, redesign.

---

## 📚 When to Document

**Quick decision** → Sketch on whiteboard
**Team discussion** → Create minimal diagrams (draw.io)
**Long-term decision** → Create ADR with all 5 views
**Major change** → Create RFC including 4+1 analysis

---

**Contact**: Mr. Đức | duch9707@gmail.com | 0389 086 502
