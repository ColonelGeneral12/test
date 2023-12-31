from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/all")

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200



def test_unauthorised_user_get_all_posts(client, test_posts):  # client is unauthorised hence we expect a 401 forbidden
    res = client.get("/posts/all")
    assert res.status_code == 401



def test_unauthorised_user_get_one_posts(client, test_posts):  # an unauthorised client wants to access one apost
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401



def test_get_one_unexisting_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/876")
    assert res.status_code == 404



def test_get_one_post(authorized_client, test_posts):
        res = authorized_client.get(f"/posts/{test_posts[0].id}")
        post = schemas.PostOut(**res.json())
        assert post.Post.id == test_posts[0].id
        assert post.Post.content == test_posts[0].content   # Checks whether the data we input matches the output
        assert post.Post.title == test_posts[0].title



@pytest.mark.parametrize("title, content, published", [
     ("awesome new title", "awesome new content", True),
     ("physcist", "paul dirac", True),
     ("russian missiles", "Bulava and sarmat", False)
])



def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(f"/posts/create", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']



def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(f"/posts/create", json={"title": "shit", "content": "shit"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "shit"
    assert created_post.content == "shit"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']



def test_unauthorised_user_create_post(client, test_user, test_posts):  # client is unauthorised hence we expect a 401 forbidden
    res = client.post("/posts/create", json={"title": "shit", "content": "shit"})
    assert res.status_code == 401



def test_unauthorised_user_delete_post(client, test_user, test_posts):  # client is unauthorised hence we expect a 401 forbidden
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401



def test_successful_deletion(authorized_client, test_user, test_posts):  
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204



def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_delete_an_unexisting_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/876")
    assert res.status_code == 404


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2,test_posts):
    data = {
        "title": "new title",
        "content": "updated post",
        "owner_id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorised_user_update_post(client, test_user, test_posts):  # client is unauthorised hence we expect a 401 forbidden
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_updating_an_unexisting_post(authorized_client, test_posts):
    data = {
        "title": "new title",
        "content": "updated post",
        "owner_id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/876", json=data)
    assert res.status_code == 404