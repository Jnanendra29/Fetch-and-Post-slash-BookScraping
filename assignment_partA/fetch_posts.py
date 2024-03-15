import requests
from db.mongo import users_collection, posts_collection

def fetch_and_store_posts():
    headers = {'app-id': '65f3b76590f59a2f67cf8d9d'}
    # fetching all users from the users_collection
    users = users_collection.find()

    for user in users:
        user_id = str(user['id'])  # ensuring the user ID is in the string format
        api_url = f'https://dummyapi.io/data/v1/user/{user_id}/post'

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            posts_data = response.json()['data']
            if posts_data:
                # posts for insertion
                for post in posts_data:
                    post['user_id'] = user_id  # adding a reference to the user in each post
                # inserting to the database posts_collection
                posts_collection.insert_many(posts_data)
                print(f"Stored posts for user {user_id}")
            else:
                print(f"No posts found for user {user_id}")
        else:
            print(f"Failed to fetch posts for user {user_id}: {response.status_code}, {response.text}")


if __name__ == "__main__":
    fetch_and_store_posts()
