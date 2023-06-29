import requests


def get(url):
    try:
        response = requests.get(url)
        if not response.ok:
            print(f'GET: Error {response.status_code}')
            return
        return response.json()
    except requests.ConnectionError:
        print('GET: ConnectionError')
