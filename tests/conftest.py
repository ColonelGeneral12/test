from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base
import pytest
from app.oath2 import create_access_token
from app.config import settings
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:kali@localhost/fastapi_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)     # Drops all tables before running
    Base.metadata.create_all(bind=engine)   # Runs before test (creates all tables before runnig the tests)
    db = TestingSessionLocal()
    try:
        yield db                                    # Create the database object
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def overide_get_db():   
        try:                                # sets up a testclient
           yield session
        finally:
           session.close()
    app.dependency_overrides[get_db] = overide_get_db    # Swaps get_db with overide_get_db inorder to pass in a diffrent session creaing a new database for testing purposes
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@gmail.com", "password": "hello123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello123@gmail.com", "password": "hello123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,           # Unpack the client.headers dictionary and add the authorisation token
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "missile",
        "content": "content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)   # goes through the post_data and returns a map
    posts = list(post_map)                        # converts the map into a lis

    session.add_all(posts)                   # adds all changes
    session.commit()                # makes all the changes to the database
    posts = session.query(models.Post).all()   # Queries for the existing posts

    return posts