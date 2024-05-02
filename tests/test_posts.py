
from typing import List
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

    print(list(posts_map))

    assert len(post_data) == len(test_posts)
    assert res.status_code == 200
