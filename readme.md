## Structure
```
└── RolyPoly
    ├── rolypoly
    │   ├── bin
    │   ├── include
    │   └── pyvenv.cfg
    ├── docker_manager.py
    ├── main.py
    └── setup.py
```

## Features

1. Rollback

2. Logging 
```
{"level": "INFO", "message": "Stopped and removed container container_test"}
{"level": "INFO", "message": "Started new container container_test with image image_test"}
{"level": "ERROR", "message": "Failed to start new container container_test with image image_test"}
```

## Use

This will rollback your image to whichever image you have chosen:

```rolypoly my-container my-image  --preserve-volumes```

Params:
my-container: container that you ran in your docker

my-image: target image that you want to rollback to

preserve-volumes: preserve volume during rollback


Example: ```rolypoly test-nginx nginx:1.17 --preserve-volumes```

If you want to force the container to stop immediately, you can use the flags below: 

```rolypoly test-nginx nginx:1.17 --force --preserve-volumes```


# Link

https://pypi.org/project/rolypoly/0.1/