import requests
from db.mongo import users_collection

def fetch_and_store_users():
    # the api endpoint for fetching users
    api_url = 'https://dummyapi.io/data/v1/user'
    headers = {'app-id': '65f3b76590f59a2f67cf8d9d'}

# fetching users from the api
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        users_data = response.json()['data']
        # inserting to the mongodb users_collection
        users_collection.insert_many(users_data)
        print(f"Stored {len(users_data)} users in the database.")
    else:
        print("Failed to fetch users from API.")

if __name__ == "__main__":
    fetch_and_store_users()
