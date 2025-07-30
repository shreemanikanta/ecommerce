# 🛍️ Product Management System

A Django-based Product Management System with JWT authentication, role-based access control, and a modern responsive dashboard UI. This system supports product listing, order tracking, admin approval, category management, and bulk product operations.

---

## 🚀 Features

- JWT-based Authentication (Login via API, token stored in `localStorage`)
- Role-Based Access: Admin, Staff, and Regular Users
- Responsive Dashboard UI (Bootstrap 5)
- Sidebar with dynamic menu based on user role
- Product CRUD operations
- Category management (Admin only)
- Product approval flow (Admin and Staff)
- Export product data to CSV
- Logout and session management via token
- Loading indicators and Toast notifications
- Secure API calls with `Authorization: Bearer <token>`

---

## 🧠 Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, Bootstrap 5, JS
- **Authentication:** JWT (JSON Web Token)
- **Others:** FontAwesome Icons, Fetch API, Toast UI

---


---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/shreemanikanta/ecommerce.git
cd product-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup

    Create a .env file in the project root according to .env.sample file:

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## ✨ Future Enhancements

    Dockerization

    Pagination and filtering for product lists

    User activity logs

    Unit tests and CI/CD integration

## 👨‍💻 Author

Shree Manikanta M.
Backend Developer | Django | DRF | ERPNext
📧 [shreemanikanta143@gmail.com]
🌐 [https://shreemanikanta.netlify.app/]

