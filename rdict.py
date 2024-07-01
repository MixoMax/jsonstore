import requests

class rdict:
    url: str
    prefix: str

    def __init__(self, url: str, prefix: str):
        self.url = url
        self.prefix = prefix
    
    def __getitem__(self, key):
        key = self.prefix + key

        url = f"{self.url}/kv_get"
        params = {"k": key}
        r = requests.get(url, params=params)
        assert r.status_code == 200
        assert "value" in r.json(), "Key not found"

        return r.json()["value"]
    
    def __setitem__(self, key, value):
        key = self.prefix + key

        url = f"{self.url}/kv_upload"
        params = {"k": key, "v": value}
        r = requests.get(url, params=params)

        assert r.status_code == 200, f"unexpected status code: {r.status_code}"
        assert "status" in r.json(), "Key exists"