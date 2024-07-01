# jsonstore

A simple key-value store that uses JSON files to store data.

Written in Python 3.x using FastAPI.

Featuring two modes:
- json mode:
    - GET /get?id={id} -> returns a JSON
    - POST /upload + JSON body -> stores a JSON and returns {id: id}
- simple kv mode:
    - GET /kv_get?k={key} -> returns a simple string -> {value: VALUE}
    - POST /kv_upload?k={key}&v={value} -> stores a simple string and returns {status: OK}

# JSON Mode

upload any json body to /upload and get a unique id for it. Then you can retrieve it using /get?id={id}

# Simple KV Mode

upload a simple key-value pair to /kv_upload and retrieve it using /kv_get?k={key}
because the sender can choose the key, it is possible that the server returns an error if the key is already in use.

# Running

```bash
python3 main.py
```

# load testing

while the server is running:

```bash
python3 test.py
```

# Dependencies

```bash
pip install fastapi uvicorn tqdm
```

tqdm is only used for the load testing script.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Author

Linus Horn <linus@linush.org>