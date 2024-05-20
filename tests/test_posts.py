import pytest
from app import schema


def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")
    post_data = res.json()
    # print(post_data)

    def validate(post):
        # Extract the relevant dictionary if the data is nested under 'Post'
        if 'Post' in post:
            post = post['Post']
        return schema.PostResponse(**post)

    # Apply validate to each item in post_data and print the results
    posts_map = map(validate, post_data)

    posts_list = list(posts_map)

    # print(posts_list)

    assert len(post_data) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[2].id == test_posts[0].id


def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorised_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}/")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorised_client, test_posts):
    res = authorised_client.get("/posts/7787878")
    assert res.status_code == 404


def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}/")
    # print(res.json())
    post = schema.PostResponse(**res.json()['Post'])
    # print(post.id)
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("new title1", "new content1", True),
    ("new title2", "new content2", False),
    ("new title3", "new content3", True),
])
def test_create_post(authorised_client, test_user, test_posts, title, content, published):
    res = authorised_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schema.PostResponse(**res.json())
    print(created_post)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
