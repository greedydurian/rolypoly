## Structure
```
rolypoly/
├─ docker_manager.py
├─ main.py
├─ tests/
│  ├─ test_docker_manager.py
│  ├─ __init__.py
├─ .gitignore
├─ package.json
├─ README.md

```

## Run unit tests
```python -m unittest tests/test_docker_manager.py```

## Features

1. Rollback

2. Logging 
```
{"level": "INFO", "message": "Stopped and removed container container_test"}
{"level": "INFO", "message": "Started new container container_test with image image_test"}
{"level": "ERROR", "message": "Failed to start new container container_test with image image_test"}
```