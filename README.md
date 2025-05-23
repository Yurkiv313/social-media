# 🌐 Social Media API

A RESTful API for a social media platform built with Django and Django REST Framework.  
It allows user registration, profile management, following/unfollowing users, creating posts with optional images and hashtags, and searching/filtering posts.

---

## 🚀 Features

### 🔐 Authentication
- JWT-based registration, login, logout (with token blacklisting)
- Secure password validation via Django validators

### 👤 User & Profile
- Register and manage user accounts
- View public profiles
- Update own profile with image, bio, location

### 🔔 Follow System
- Follow and unfollow users
- List your followers and followings

### 📝 Posts
- Create posts with content, hashtags, and optional images
- View your own and followed users’ posts
- Filter posts by hashtags
- Edit or delete only your own posts

### 📄 Documentation
- Swagger/OpenAPI auto-generated docs
- Schema descriptions for all endpoints (`drf-spectacular`)

### ✅ Tests
- Tests for authentication, profile, follow, and post functionality

---

## ⚙️ Installation

```bash
git clone https://github.com/Yurkiv313/social-media-api.git
cd social-media-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

