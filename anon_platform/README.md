# WhisperFeed - Anonymous Social Platform

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

WhisperFeed is a secure, anonymous social media platform built with Python and FastAPI. It allows users to share thoughts, posts, and messages while maintaining complete anonymity.

## 🌟 Features

- **Anonymous Posting**: Share your thoughts without revealing your identity
- **Secure Authentication**: JWT-based authentication with password hashing
- **Real-time Messaging**: Private conversations between users
- **Voting System**: Upvote/downvote posts and comments
- **Modern API**: Built with FastAPI for high performance and automatic documentation
- **Async Database**: Uses PostgreSQL with SQLAlchemy for efficient data handling

## 🚀 Tech Stack

- **Backend**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with PassLib
- **Async Support**: Built with async/await for better performance
- **Data Validation**: Pydantic models for request/response validation

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sam06002/WhisperPython.git
   cd WhisperPython
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/anon_db
   SECRET_KEY=your-secret-key-here
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📚 API Documentation

Once the server is running, you can access:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🌐 Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/posts` - Get all posts
- `POST /api/v1/posts` - Create a new post
- `POST /api/v1/comments` - Add a comment to a post
- `POST /api/v1/vote` - Vote on a post or comment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using FastAPI and Python
- Special thanks to all contributors
