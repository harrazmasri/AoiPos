# AOI POS System

This POS system is a web-based point-of-sale and management system built using Python with the Django framework and an SQLite database. Traditional manual cataloguing or cash registers are usually slow and vulnerable to calculation errors. 

Unlike an e-commerce platform designed for external customer shopping and delivery, this internal company management system allows cashiers to process transactions and track inventory. The AOI POS cashier system automates daily store operations, keeps inventory updated in real-time, and provides clear sales tracking through an easy-to-use interface for both admins and cashiers.

---

## User Roles

* **Admin Role:** Full system access (includes all cashier capabilities) plus adding/updating product details, viewing performance analytics, and inspecting transaction logs.
* **Cashier Role:** Restricted operational access focused on adding items to the cart, processing payments, calculating change, issuing sales receipts, and viewing their profile.

---

## Tech Stack & Implementation

* **Backend:** Django (Python)
* **Frontend:** jQuery, Tailwind CSS
* **Database:** SQLite

### Key Features
* Custom Middleware integration
* Automatic seed data generation for the default Admin account upon database migration

---

## Getting Started

### Prerequisites
* Python
* Django

### Setup & Local Installation

1. Generate database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   open 127.0.0.1:8000
   ```
   

<u>Log In</u>
<img width="1377" height="709" alt="image" src="https://github.com/user-attachments/assets/c5b2c958-1448-47bc-8e90-d95880266c3a" />

<u>Cashier Dashboard</u>
<img width="1500" height="793" alt="image" src="https://github.com/user-attachments/assets/682f4379-7edf-40d6-b6ec-3b582481dea0" />

<u>Checkout</u>
<img width="1199" height="635" alt="image" src="https://github.com/user-attachments/assets/14a773bf-47fa-433b-a6f8-2ed1c841fb65" />

<u>Product Catalogue</u>
<img width="1380" height="849" alt="image" src="https://github.com/user-attachments/assets/c8674f8d-fdbc-4824-a915-bd5b3604b5fb" />

<u>Performance Summary</u>
<img width="1600" height="1035" alt="image" src="https://github.com/user-attachments/assets/13cad399-9943-4e0b-89f7-e5be954609ff" />
