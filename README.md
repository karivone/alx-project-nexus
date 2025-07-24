# Smart Property Management System (SPMS) - Backend

A robust backend application for managing rental properties, tenants, and landlords, built with Django and PostgreSQL. This project simulates a real-world property management tool supporting secure authentication, property listings, tenant applications, maintenance tracking, and payment recording.

## 🚀 Project Nexus: Capstone Overview

This project demonstrates mastery of backend engineering concepts including:

- RESTful and GraphQL APIs
- Role-based authentication
- Optimized database design
- Background task management
- API documentation (Swagger & GraphQL Playground)
- Caching and performance tuning
- Dockerization and CI/CD practices

---

## 📌 Key Features

### 🔐 Authentication
- JWT-based login and registration
- Role-based access: Admin, Landlord, Tenant

### 🏠 Property Listings
- CRUD APIs for properties
- Filtering by location, price, type
- Pagination and search support
- Media URL support for property images/videos

### 📄 Tenant Applications
- Apply to listed properties
- Upload documents (proof of income, ID)
- Landlord approval or rejection workflow

### 🛠️ Maintenance Requests
- Tenants submit repair requests
- Landlords or admins assign and resolve
- Optional: WebSocket/real-time updates (via Django Channels)

### 💰 Rent Payments
- Tenants can log monthly rent payments
- Payment tracking for each property
- Optional: mock integration with a payment gateway (e.g., Stripe)

### 📬 Notifications (Optional)
- In-app/email reminders for upcoming rent
- Task-based notifications for maintenance status
- Powered by Celery + Redis

### 📊 Analytics Dashboard (Optional)
- Number of active tenants
- Total monthly rent
- Pending maintenance requests

---

## ⚙️ Technologies Used

| Purpose                 | Technology            |
|------------------------|-----------------------|
| Backend Framework      | Django, Django REST Framework |
| Database               | PostgreSQL            |
| Caching & Queues       | Redis, Celery         |
| Authentication         | JWT (SimpleJWT)       |
| Documentation          | Swagger (drf-yasg), GraphQL Playground |
| DevOps & Deployment    | Docker, GitHub Actions |
| Version Control        | Git + Conventional Commits |
| Optional Realtime      | Django Channels       |

---

## 🗃️ Database Models (Simplified)

- **User**: Custom user model with roles (`is_admin`, `is_landlord`, `is_tenant`)
- **Property**: Property listing with metadata (location, rent, media, etc.)
- **Application**: Tenant applications to properties
- **MaintenanceRequest**: Requests for property repairs
- **Payment**: Record of rent payments per tenant per property
- **Notification**: Optional table for storing alerts/events

---

## 📑 API Endpoints

### 🔐 Authentication

| Method | Endpoint           | Description                     |
|--------|--------------------|---------------------------------|
| POST   | `/api/auth/register/` | Register a user                |
| POST   | `/api/auth/login/`    | JWT-based login                |
| GET    | `/api/auth/profile/`  | Get current user profile       |

---

### 🏘️ Property Management

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/api/properties/`     | List all properties (with filters) |
| POST   | `/api/properties/`     | Create a property (landlord only) |
| GET    | `/api/properties/:id/` | View single property           |
| PUT    | `/api/properties/:id/` | Update property (owner only)   |
| DELETE | `/api/properties/:id/` | Delete property (owner only)   |

#### Filters Supported

- `?location=city`
- `?min_price=10000&max_price=50000`
- `?type=apartment`
- Pagination: `?page=1&page_size=10`

---

### 📝 Tenant Applications

| Method | Endpoint                          | Description                     |
|--------|-----------------------------------|---------------------------------|
| POST   | `/api/applications/`              | Submit application (tenant)    |
| GET    | `/api/applications/`              | List applications (landlord/admin) |
| PATCH  | `/api/applications/:id/approve/`  | Approve application (landlord) |
| PATCH  | `/api/applications/:id/reject/`   | Reject application (landlord)  |

---

### 🛠️ Maintenance Requests

| Method | Endpoint                           | Description                      |
|--------|------------------------------------|----------------------------------|
| POST   | `/api/maintenance/`                | Submit request (tenant)         |
| GET    | `/api/maintenance/`                | List all requests (landlord/admin) |
| PATCH  | `/api/maintenance/:id/resolve/`    | Mark as resolved (landlord)     |

---

### 💳 Rent Payments

| Method | Endpoint              | Description                  |
|--------|-----------------------|------------------------------|
| POST   | `/api/payments/`      | Record payment (tenant)      |
| GET    | `/api/payments/`      | View payment history         |

---

### 🛎️ Notifications (Optional)

| Method | Endpoint              | Description                  |
|--------|-----------------------|------------------------------|
| GET    | `/api/notifications/` | Get all current notifications |
| POST   | Background via Celery |

---

### 🧪 GraphQL (Optional)

> Endpoint: `/graphql/` with GraphQL Playground enabled

Sample Queries:
```graphql
query {
  properties(location: "Nairobi", minPrice: 20000) {
    title
    rent
    landlord {
      name
    }
  }
}
```

---

## 📝 API Documentation

- **Swagger UI**: Available at `/api/docs/`
- **GraphQL Playground**: Available at `/graphql/` (if enabled)
- **Postman Collection**: [Link to collection](#) (optional)

---

## 🐳 Dockerized Setup

```bash
# Build and run the app
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

---

## ✅ Project Goals Achieved

- ✅ REST + GraphQL API implementations
- ✅ JWT Authentication and RBAC
- ✅ PostgreSQL with indexing and optimization
- ✅ Redis Caching for listing queries
- ✅ Celery tasks for notifications
- ✅ Swagger Documentation
- ✅ Docker & GitHub Actions CI

---

## 📂 Git Commit Workflow

```bash
feat: setup Django project with PostgreSQL
feat: implement JWT authentication and roles
feat: add property listing with filtering
feat: add tenant application logic
feat: implement rent payment APIs
feat: integrate Celery + Redis for notifications
feat: add GraphQL queries for dashboard
feat: document APIs with Swagger
docs: update README with setup and usage
```

---

## 📖 Setup Instructions

```bash
# Clone project
git clone https://github.com/yourusername/spms-backend.git
cd spms-backend

# Setup virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Run locally
python manage.py runserver
```

---

## 📌 License

MIT License

---
