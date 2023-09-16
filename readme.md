## Structure
```
└── RolyPoly
    ├── rolypoly
    │   ├── bin
    │   ├── include
    │   └── pyvenv.cfg
    ├── tests
    │   └── test_docker_manager.py
    ├── docker_manager.py
    ├── main.py
    └── setup.py
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

```source rolypoly/bin/activate```
```pip install . --use-pep517```

## Use

```python main.py test-nginx nginx:1.17 --preserve-volumes```