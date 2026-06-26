⚔️ Paragon API

A Flask-based RESTful API featuring relational database design, JWT authentication, and full CRUD functionality for a fantasy world management system.

📌 Overview

Paragon API is a backend service that models a fantasy world consisting of Kingdoms, Cities, and Characters.
It demonstrates modern backend development concepts including authentication, database relationships, and secure API design.

Built with:

Flask
Flask-SQLAlchemy
Flask-JWT-Extended
SQLite


🏰 World Structure
Kingdoms contain multiple Cities
Cities contain multiple Characters
Fully relational database design (One-to-Many relationships)


👤 Authentication System
User registration with password hashing
Secure login system
JWT-based authentication
Protected routes for data modification

⚔️ Character System (CRUD)
Create characters (protected)
Read all characters
Read individual characters
Update characters (protected)
Delete characters (protected)

🌍 World Queries
Get all cities with kingdom data
Get all kingdoms with nested cities
Get all characters in a specific city

🔐 Authentication

Most write operations require a JWT token.

Register
POST /register
{
  "username": "user1",
  "password": "password123"
}
Login
POST /login
{
  "username": "user1",
  "password": "password123"
}

Response:

{
  "access_token": "your-jwt-token"
}
Using Token in Requests

Include the token in Postman or headers:

Authorization: Bearer <your_token>
📡 API Endpoints
🏰 Kingdoms
GET /kingdoms
GET /kingdoms/<id>

🏙️ Cities
GET /cities
GET /cities/<city_id>/characters

⚔️ Characters
GET /characters
GET /characters/<id>

POST /characters        (JWT required)
PUT /characters/<id>    (JWT required)
DELETE /characters/<id> (JWT required)

👤 Auth
POST /register
POST /login

🧠 Example Character Object
{
  "id": 1,
  "name": "Aldric",
  "race": "Human",
  "class": "Paladin",
  "city": "Fortitudo"
}

🗄️ Database Schema
Kingdom
id (PK)
name
City
id (PK)
name
kingdom_id (FK → Kingdom)
Character
id (PK)
name
race
character_class
city_id (FK → City)
User
id (PK)
username
password (hashed)

🛠️ Tech Stack
Python 3
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Werkzeug Security
SQLite

📦 Installation & Setup
1. Clone repo
git clone https://github.com/yourusername/paragon-api.git
cd paragon-api
2. Create virtual environment
python -m venv venv
3. Activate environment
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Run server
python app.py
📮 Testing (Postman)
Register user → /register
Login → /login
Copy JWT token

Add to headers:

Authorization: Bearer <token>
Test protected routes:
POST /characters
PUT /characters/<id>
DELETE /characters/<id>

📈 What This Project Demonstrates
REST API design principles
JWT authentication & authorization
Relational database modeling
CRUD operations
Secure password handling
Backend architecture fundamentals

🚀 Future Improvements
Role-based access control (Admin/User)
Pagination for large datasets
Swagger/OpenAPI documentation
Deployment to Render / Railway
Docker containerization

👨‍💻 Author

Kevin Gonzalez