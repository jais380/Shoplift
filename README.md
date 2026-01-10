# 🛒 SHOPLIFT – Django REST E-Commerce API

SHOPLIFT is a backend e-commerce REST API built with Django and Django Rest Framework (DRF).
It provides product management, user authentication with JWT, and a robust shopping cart system with transactional safety and business rules enforced at the database level.

This project is designed as a backend-only service, ready to be consumed by a frontend (React, HTMX, mobile app, etc.).

LIVE API DOCS - https://shoplift-2o3r.onrender.com

# 🚀 Features
🔐 Authentication

- User registration

- JWT authentication (access & refresh tokens)

- Protected endpoints using IsAuthenticated

📦 Products

- Create, read, update, delete products (admin-only)

- Public product listing

- Product search by name

- Product filtering by category

- Pagination support

🛍️ Cart System

- One pending cart per user (enforced via database constraint)

- Add items to cart

- Increment quantity when the same product is added

- Prevent adding items to non-pending carts

- Remove or update cart items (only if cart is pending)

- Automatic total price calculation

- Item count per cart

- Transaction-safe cart operations

🔒 Permissions & Safety

- Implemented TDD best practices for endpoints

- Read-only access for non-admins on products

- Users can only access their own carts

- Atomic transactions to avoid race conditions

- Database-level uniqueness constraints

# 🧱 Tech Stack

- Python

- Django

- Django REST Framework

- PostgreSQL

- Simple JWT

- django-filters

# ⚙️ Installation & Setup
1️⃣ Clone the repository

- git clone https://github.com/jais380/Shoplift.git

- cd Shoplift

2️⃣ Create a virtual environment


- python -m venv venv

- source venv/bin/activate  or  On Windows: venv\Scripts\activate

3️⃣ Install dependencies


- pip install -r requirements.txt

4️⃣ Configure PostgreSQL

Update your DATABASES settings in settings.py:


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<YOUR_DATABASE_NAME>',
        'USER': '<YOUR_USERNAME>',
        'PASSWORD': '<YOUR_PASSWORD>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5️⃣ Run migrations

- python manage.py makemigrations

- python manage.py migrate

6️⃣ Create superuser


- python manage.py createsuperuser

7️⃣ Run the server


- python manage.py runserver

# 🔑 Authentication Endpoints

Register


`POST /account/register/`

Obtain JWT Token


`POST /account/api/token/`

Refresh Token


`POST /account/api/token/refresh/`

Logout


`POST /account/logout/`

# 📦 Product Endpoints

| Method    | Endpoint                             | Description            |
| --------- | ------------------------------------ | ---------------------- |
| GET       | `/api/products/`                     | List products          |
| POST      | `/api/products/`                     | Create product (admin) |
| GET       | `/api/product/<id>/`                 | Retrieve product       |
| PUT/PATCH | `/api/product/<id>/`                 | Update product (admin) |
| DELETE    | `/api/product/<id>/`                 | Delete product (admin) |
| GET       | `/api/category/<category>/products/` | Products by category   |

# 🛒 Cart Endpoints

| Method | Endpoint                | Description                |
| ------ | ----------------------- | -------------------------- |
| GET    | `/api/carts/`           | List user carts            |
| POST   | `/api/carts/`           | Create new cart            |
| GET    | `/api/cart/pending/`    | Get or create pending cart |
| GET    | `/api/cart/<id>/`       | Retrieve cart              |
| DELETE | `/api/cart/<id>/`       | Delete cart                |
| GET    | `/api/cart/<id>/items/` | List cart items            |
| POST   | `/api/cart/<id>/items/` | Add item to cart           |
| GET    | `/api/cart/item/<id>/`  | Retrieve cart item         |
| PATCH  | `/api/cart/item/<id>/`  | Update quantity            |
| DELETE | `/api/cart/item/<id>/`  | Remove item                |


# 🧠 Business Rules

- Only one pending cart per user

- Items can only be added to pending carts

- Cart items are unique per product

- Quantity must be ≥ 1

- Users can only access their own carts

- Cart operations are transaction-safe

# 📌 Future Improvements

- Checkout & payment integration

- Order history

- Stock management

- Product images

- Coupon & discount system

- Frontend integration (React / HTMX)

# 👤 Author

Jude

Backend Developer (Django / DRF)

# 📜 License

This project is open-source and available under the MIT License.
