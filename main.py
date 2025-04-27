from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

DATABASE_URL = "mysql+mysqlconnector://user@127.0.0.1:3306/blog_cms"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# New SQLAlchemy models
class User(Base):
    __tablename__ = 'user'
    id = Column(String(10), primary_key=True)
    username = Column(String(15), unique=True, nullable=False)
    firstName = Column(String(50), nullable=False)
    secondName = Column(String(50))
    otherName = Column(String(50))

class AuthorModel(Base):
    __tablename__ = 'author'
    id = Column(String(12), primary_key=True)
    username = Column(String(15), unique=True, nullable=False)
    user = Column('user', String(15), ForeignKey("`user`.username", ondelete="CASCADE"), nullable=False)
    firstName = Column(String(50), nullable=False)
    secondName = Column(String(50))
    otherName = Column(String(50))
    nickName = Column(String(50))

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(50), primary_key=True)

class HashtagModel(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    category = Column(String(50), ForeignKey("category.name", ondelete="RESTRICT"), nullable=False)

class PostModel(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(15), ForeignKey("author.username", ondelete="RESTRICT"), nullable=False)
    category = Column(String(50), ForeignKey("category.name", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text)
    status = Column(Boolean, nullable=False, default=False)

# Pydantic schemas
class UserBase(BaseModel):
    username: str
    firstName: str
    secondName: Optional[str] = None
    otherName: Optional[str] = None

class UserCreate(UserBase): pass
class UserOut(UserBase):
    id: str
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase): pass
class CategoryOut(CategoryBase):
    class Config:
        orm_mode = True

class HashtagBase(BaseModel):
    name: str
    category: str

class HashtagCreate(HashtagBase): pass
class HashtagOut(HashtagBase):
    id: int
    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    username: str
    user: str
    firstName: str
    secondName: Optional[str] = None
    otherName: Optional[str] = None
    nickName: Optional[str] = None

class AuthorCreate(AuthorBase): pass
class AuthorOut(AuthorBase):
    id: str
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    author: str
    category: str
    title: str
    body: Optional[str] = None
    status: bool = False

class PostCreate(PostBase): pass
class PostUpdate(BaseModel):
    author: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    status: Optional[bool] = None

class PostOut(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Items API!"}  # Root handler :contentReference[oaicite:8]{index=8}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD endpoints for User, Category, Hashtag, Author, Post
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, firstName=user.firstName, secondName=user.secondName, otherName=user.otherName)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    db.query(AuthorModel).filter(AuthorModel.user == username).delete()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    return {"detail": "User and associated authors deleted"}

@app.post("/categories/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_cat = Category(name=category.name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/categories/", response_model=List[CategoryOut])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Category).offset(skip).limit(limit).all()

@app.delete("/categories/{name}")
def delete_category(name: str, db: Session = Depends(get_db)):
    db.query(Category).filter(Category.name == name).delete()
    db.commit()
    return {"detail": "Category deleted"}

@app.post("/hashtags/", response_model=HashtagOut)
def create_hashtag(hashtag: HashtagCreate, db: Session = Depends(get_db)):
    db_ht = HashtagModel(name=hashtag.name, category=hashtag.category)
    db.add(db_ht)
    db.commit()
    db.refresh(db_ht)
    return db_ht

@app.get("/hashtags/", response_model=List[HashtagOut])
def read_hashtags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(HashtagModel).offset(skip).limit(limit).all()

@app.get("/hashtags/latest", response_model=List[HashtagOut])
def read_latest_hashtags(db: Session = Depends(get_db)):
    return db.query(HashtagModel).order_by(HashtagModel.id.desc()).limit(10).all()

@app.delete("/hashtags/{id}")
def delete_hashtag(id: int, db: Session = Depends(get_db)):
    db.query(HashtagModel).filter(HashtagModel.id == id).delete()
    db.commit()
    return {"detail": "Hashtag deleted"}

@app.post("/authors/", response_model=AuthorOut)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = AuthorModel(username=author.username, user=author.user, firstName=author.firstName,
                            secondName=author.secondName, otherName=author.otherName, nickName=author.nickName)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/authors/", response_model=List[AuthorOut])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(AuthorModel).offset(skip).limit(limit).all()

@app.get("/authors/latest", response_model=List[AuthorOut])
def read_latest_authors(db: Session = Depends(get_db)):
    return db.query(AuthorModel).order_by(AuthorModel.id.desc()).limit(10).all()

@app.delete("/authors/{username}")
def delete_author(username: str, db: Session = Depends(get_db)):
    db.query(AuthorModel).filter(AuthorModel.username == username).delete()
    db.commit()
    return {"detail": "Author deleted"}

@app.post("/posts/", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = PostModel(author=post.author, category=post.category, title=post.title, body=post.body, status=post.status)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[PostOut])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(PostModel).offset(skip).limit(limit).all()

@app.get("/posts/latest", response_model=List[PostOut])
def read_latest_posts(db: Session = Depends(get_db)):
    return db.query(PostModel).order_by(PostModel.created_at.desc()).limit(10).all()

@app.get("/posts/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, update: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for var, value in vars(update).items():
        if value is not None:
            setattr(post, var, value)
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db.query(PostModel).filter(PostModel.id == post_id).delete()
    db.commit()
    return {"detail": "Post deleted"}

# Create tables after models
Base.metadata.create_all(bind=engine)
