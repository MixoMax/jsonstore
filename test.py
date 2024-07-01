import requests
import random
import string
import time
from tqdm import tqdm



def random_json(n_keys: int, length_key: int, length_value: int) -> dict:
    keys = ["".join(random.choices(string.ascii_letters, k=length_key)) for _ in range(n_keys)]
    values = ["".join(random.choices(string.ascii_letters, k=length_value)) for _ in range(n_keys)]
    return dict(zip(keys, values))

url = "http://127.0.0.1:1960"


n_keys = 100
length_key = 1000
length_value = 1000


n_uploads = 1000
n_gets = 1000
n_parity = 500

ids = []

t_start = time.time()
for _ in tqdm(range(n_uploads)):
    d = random_json(n_keys, length_key, length_value)
    r = requests.post(url + "/upload", json=d)
    assert r.status_code == 200
    assert "id" in r.json()
    ids.append(r.json()["id"])
t_end = time.time()

req_per_sec = n_uploads / (t_end - t_start)
print(f"Uploads: {req_per_sec:.2f} req/sec")


t_start = time.time()
for _ in tqdm(range(n_gets)):
    id = random.choice(ids)
    r = requests.get(url + f"/get?id={id}")
    assert r.status_code == 200
    assert "error" not in r.json()
t_end = time.time()

req_per_sec = n_gets / (t_end - t_start)
print(f"Gets: {req_per_sec:.2f} req/sec")


kv = {}
for _ in range(n_parity):
    d = random_json(n_keys, length_key, length_value)
    r = requests.post(url + "/upload", json=d)
    assert r.status_code == 200
    assert "id" in r.json()
    id = r.json()["id"]
    kv[id] = d

for _ in range(n_parity):
    id = random.choice(list(kv.keys()))
    r = requests.get(url + f"/get?id={id}")
    assert r.status_code == 200
    assert r.json() == kv[id]

print("Parity check passed")
