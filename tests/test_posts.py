
from typing import List
from app import schema


def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")

    for post in res.json():
        print(post['Post']['title'])
        # posts = schema.Post(res.json())
    assert res.status_code == 200
