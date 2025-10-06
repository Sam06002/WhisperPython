
Hello Windsurf,

We are building an anonymous social media platform using Python. Your task is to generate the complete project structure and all the necessary files for Phase 1.

**Project Specifications:**
- **Framework**: FastAPI
- **Database**: PostgreSQL (with async SQLAlchemy)
- **Authentication**: JWT with PassLib
- **Environment**: Linux (Ubuntu)
- **Python Version**: 3.11

Please execute the following steps precisely. Create each file with the exact path and content provided.

---

### **Step 1: Create the Project Directory and Initial Files**

First, generate the following directory structure.

```

mkdir anon_platform
cd anon_platform
python3 -m venv venv
source venv/bin/activate
pip install "fastapi[all]" uvicorn sqlalchemy[asyncpg] alembic passlib[bcrypt] python-jose[cryptography] python-multipart jinja2 pillow names pydantic-settings
mkdir -p app/api/routes app/core app/db app/schemas app/services app/static/images app/templates
touch app/__init__.py
touch app/api/__init__.py
touch app/api/routes/__init__.py
touch app/core/__init__.py
touch app/db/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/main.py

```

---

### **Step 2: Create Configuration Files**

**File: `pyproject.toml`**
Create this file in the project root (`anon_platform/`).

```

[tool.poetry]
name = "anon-platform"
version = "0.1.0"
description = "Anonymous Social Media Platform"
authors = ["Your Name [you@example.com](mailto:you@example.com)"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = {extras = ["all"], version = "^0.110.0"}
uvicorn = {extras = ["standard"], version = "^0.27.1"}
sqlalchemy = {extras = ["asyncpg"], version = "^2.0.27"}
alembic = "^1.13.1"
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
python-multipart = "^0.0.9"
jinja2 = "^3.1.3"
pillow = "^10.2.0"
names = "^0.3.0"
pydantic-settings = "^2.2.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

```

**File: `.gitignore`**
Create this file in the project root (`anon_platform/`).

```


# Byte-compiled / optimized / DLL files

__pycache__/
*.py[cod]
*\$py.class

# C extensions

*.so

# Distribution / packaging

.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller

# Usually these files are written by a python script from a template

# before PyInstaller builds the exe, so as to inject date/other infos into it.

*.manifest
*.spec

# Installer logs

pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports

htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations

*.mo
*.pot

# Django stuff:

*.log
local_settings.py
db.sqlite3

# Flask stuff:

instance/
.webassets-cache

# Scrapy stuff:

.scrapy

# Sphinx documentation

docs/_build/

# PyBuilder

target/

# Jupyter Notebook

.ipynb_checkpoints

# IPython

profile_default/
ipython_config.py

# pyenv

.python-version

# poetry

poetry.lock

# PEP 582;

__pypackages__/

# Celery stuff

celerybeat-schedule
celerybeat.pid

# SageMath parsed files

*.sage.py

# Environments

.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE specific files

.idea/
.vscode/

```

**File: `app/core/config.py`**
This file will manage all our environment variables and settings.

```

import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
PROJECT_NAME: str = "Anonymous Social Platform"
API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/anon_db")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_long_and_random")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Image Upload Settings
    IMAGE_UPLOAD_DIR: str = "app/static/images"
    MAX_IMAGE_SIZE_MB: int = 2
    ALLOWED_IMAGE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    IMAGE_MAX_WIDTH: int = 1200
    
    class Config:
        case_sensitive = True
        env_file = ".env"
    settings = Settings()

```

---

### **Step 3: Set Up Database Connection**

**File: `app/db/session.py`**

```

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)
AsyncSessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine,
class_=AsyncSession,
expire_on_commit=False,
)

```

**File: `app/db/base.py`**
This file will contain the base model for SQLAlchemy.

```

from sqlalchemy.orm import declarative_base

Base = declarative_base()

```

---

### **Step 4: Define Database Models**

**File: `app/db/models.py`**
This file defines all database tables.

```

from sqlalchemy import (
Column,
Integer,
String,
Text,
DateTime,
ForeignKey,
Float,
func,
Boolean,
)
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
__tablename__ = "users"
id = Column(Integer, primary_key=True, index=True)
username = Column(String(50), unique=True, index=True, nullable=False)
hashed_password = Column(String, nullable=False)
bio = Column(Text, nullable=True)
avatar_url = Column(String, nullable=True)
created_at = Column(DateTime, server_default=func.now())
upvote_count = Column(Integer, default=0)
downvote_count = Column(Integer, default=0)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    votes = relationship("Vote", back_populates="user")
    class Post(Base):
__tablename__ = "posts"
id = Column(Integer, primary_key=True, index=True)
content = Column(Text, nullable=False)
image_url = Column(String, nullable=True)
created_at = Column(DateTime, server_default=func.now(), index=True)
owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")
    class Comment(Base):
__tablename__ = "comments"
id = Column(Integer, primary_key=True, index=True)
content = Column(Text, nullable=False)
created_at = Column(DateTime, server_default=func.now())
owner_id = Column(Integer, ForeignKey("users.id"))
post_id = Column(Integer, ForeignKey("posts.id"))
parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="comment", cascade="all, delete-orphan")
    class Vote(Base):
__tablename__ = "votes"
id = Column(Integer, primary_key=True)
user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
value = Column(Integer, nullable=False) \# 1 for upvote, -1 for downvote

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")
    comment = relationship("Comment", back_populates="votes")
    class Conversation(Base):
__tablename__ = "conversations"
id = Column(Integer, primary_key=True, index=True)
participant1_id = Column(Integer, ForeignKey("users.id"))
participant2_id = Column(Integer, ForeignKey("users.id"))
accepted = Column(Boolean, default=False)
created_at = Column(DateTime, server_default=func.now())

class Message(Base):
__tablename__ = "messages"
id = Column(Integer, primary_key=True, index=True)
conversation_id = Column(Integer, ForeignKey("conversations.id"))
sender_id = Column(Integer, ForeignKey("users.id"))
content = Column(Text, nullable=False)
created_at = Column(DateTime, server_default=func.now())

```

---

### **Step 5: Set Up Database Migrations with Alembic**

Run these commands in the terminal from the project root (`anon_platform/`) to set up Alembic.

```

alembic init alembic

```

Now, **edit the `alembic/env.py` file**.
Find the line `target_metadata = None` and replace it with:
```

from app.db.base import Base
target_metadata = Base.metadata

```

Next, **edit `alembic.ini`**.
Find the line `sqlalchemy.url = ...` and replace it with the database URL from our settings.
```

sqlalchemy.url = postgresql+asyncpg://user:password@localhost/anon_db

```
*Note to user: You will need to update this with your actual database URL.*

Finally, run these commands to create the first migration.
```

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

```

---

### **Step 6: Create Pydantic Schemas**

**File: `app/schemas/user.py`**

```

from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
username: constr(min_length=3, max_length=50)
password: str

class UserBase(BaseModel):
id: int
username: str

    class Config:
        from_attributes = True
    class UserProfile(UserBase):
bio: Optional[str]
avatar_url: Optional[str]
created_at: datetime
upvote_count: int
downvote_count: int
vote_ratio: float

class Token(BaseModel):
access_token: str
token_type: str

class TokenData(BaseModel):
username: Optional[str] = None

```

---

### **Step 7: Implement Authentication and User Services**

**File: `app/services/security.py`**

```

from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
to_encode = data.copy()
if expires_delta:
expire = datetime.now(timezone.utc) + expires_delta
else:
expire = datetime.now(timezone.utc) + timedelta(minutes=15)
to_encode.update({"exp": expire})
encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
return encoded_jwt

```

**File: `app/services/user_service.py`**
This service will handle user creation logic, including generating random usernames.

```

import names
import random
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.user import UserCreate
from app.services.security import get_password_hash

async def get_user_by_username(db: AsyncSession, username: str):
result = await db.execute(select(User).filter(User.username == username))
return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
hashed_password = get_password_hash(user.password)
db_user = User(username=user.username, hashed_password=hashed_password)
db.add(db_user)
await db.commit()
await db.refresh(db_user)
return db_user

async def is_username_taken(db: AsyncSession, username: str) -> bool:
user = await get_user_by_username(db, username)
return user is not None

def generate_random_username() -> str:
adjective = names.get_first_name(gender='male').capitalize() \# Using names for adjectives
noun = names.get_last_name().capitalize()
number = random.randint(10, 999)
return f"{adjective}{noun}{number}"

async def get_unique_random_username(db: AsyncSession) -> str:
while True:
username = generate_random_username()
if not await is_username_taken(db, username):
return username

```

---

### **Step 8: Create API Endpoints (Routers)**

**File: `app/api/dependencies.py`**
This file will contain common dependencies for our API.

```

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.db.session import AsyncSessionLocal
from app.core.config import settings
from app.schemas.user import TokenData
from app.services.user_service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")

async def get_db():
async with AsyncSessionLocal() as session:
yield session

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
credentials_exception = HTTPException(
status_code=status.HTTP_401_UNAUTHORIZED,
detail="Could not validate credentials",
headers={"WWW-Authenticate": "Bearer"},
)
try:
payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
username: str = payload.get("sub")
if username is None:
raise credentials_exception
token_data = TokenData(username=username)
except JWTError:
raise credentials_exception
user = await get_user_by_username(db, username=token_data.username)
if user is None:
raise credentials_exception
return user

```

**File: `app/api/routes/users.py`**

```

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.api.dependencies import get_db, get_current_user
from app.schemas.user import UserCreate, UserProfile, Token
from app.services import user_service, security
from app.core.config import settings
from app.db.models import User

router = APIRouter()

@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
if await user_service.is_username_taken(db, user.username):
raise HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
detail="Username already registered",
)
db_user = await user_service.create_user(db=db, user=user)
ratio = (db_user.upvote_count / (db_user.upvote_count + db_user.downvote_count)) if (db_user.upvote_count + db_user.downvote_count) > 0 else 0.0
return UserProfile(
id=db_user.id,
username=db_user.username,
bio=db_user.bio,
avatar_url=db_user.avatar_url,
created_at=db_user.created_at,
upvote_count=db_user.upvote_count,
downvote_count=db_user.downvote_count,
vote_ratio=ratio
)

@router.get("/register/generate-username", response_model=dict)
async def generate_username(db: AsyncSession = Depends(get_db)):
username = await user_service.get_unique_random_username(db)
return {"username": username}

@router.post("/login", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
user = await user_service.get_user_by_username(db, username=form_data.username)
if not user or not security.verify_password(form_data.password, user.hashed_password):
raise HTTPException(
status_code=status.HTTP_401_UNAUTHORIZED,
detail="Incorrect username or password",
headers={"WWW-Authenticate": "Bearer"},
)
access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
access_token = security.create_access_token(
data={"sub": user.username}, expires_delta=access_token_expires
)
return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserProfile)
async def read_users_me(current_user: User = Depends(get_current_user)):
ratio = (current_user.upvote_count / (current_user.upvote_count + current_user.downvote_count)) if (current_user.upvote_count + current_user.downvote_count) > 0 else 0.0
return UserProfile(
id=current_user.id,
username=current_user.username,
bio=current_user.bio,
avatar_url=current_user.avatar_url,
created_at=current_user.created_at,
upvote_count=current_user.upvote_count,
downvote_count=current_user.downvote_count,
vote_ratio=ratio
)

```

---

### **Step 9: Assemble the Main Application**

**File: `app/main.py`**

```

from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import users

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

@app.get("/")
def read_root():
return {"message": f"Welcome to {settings.PROJECT_NAME}"}

```

---

### **Step 10: Final Sanity Check**

Make sure all files are in their correct locations. The project structure should look like this:

```

anon_platform/
├── alembic/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── users.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── user_service.py
│   ├── static/
│   │   └── images/
│   ├── templates/
│   ├── __init__.py
│   └── main.py
├── .gitignore
├── alembic.ini
├── pyproject.toml
└── venv/

```

Once all files are generated, you can start the application from the project root directory (`anon_platform/`) with the following command:

`uvicorn app.main:app --reload`

You can then access the API documentation at `http://127.0.0.1:8000/docs`.

This completes Phase 1.
```
