# AI-Chat-Bot-IFSGuide

## Description

...


## Features

- Clean Architecture design pattern
- Web framework layer using FastAPI
- Modular and flexible architecture
- Examples of common features such as authentication, authorization, and CRUD operations

## folder structure

```
└── app
    ├── cmd
    │   ├── start.sh
    │   ├── stop.sh
    │   ├── restart.sh
    │   └── ...
    ├── data
    │   └── ...
    ├── src
    │   ├── adapters
    │   │   ├── authentication_provider
    │   │   │   ├── tests
    │   │   │   └── ...
    │   │   ├── db
    │   │   │   └── django_orm
    │   │   │       ├── core
    │   │   │       ├── db
    │   │   │       ├── tests
    │   │   │       ├── manage.py
    │   │   │       ├── repository.py
    │   │   │       └── ...
    │   │   └── ...
    │   ├── config_files
    │   │   └── ...
    │   ├── entities
    │   │   └── ...
    │   ├── framework
    │   │   ├── api
    │   │   │   ├── configs
    │   │   │   ├── schemas
    │   │   │   ├── tests
    │   │   │   └── ...
    │   │   └── ...
    │   ├── use_cases
    │   │   ├── interfaces
    │   │   │   └── ...
    │   │   ├── tests
    │   │   └── ...
    │   ├── utils
    │   │   └── ...
    │   ├── config.py
    │   ├── config_dependency_injection.py
    │   ├── config_dependency_injection_test.py
    │   ├── config.py
    │   └── ...
    ├── dependencies.py
    ├── main.py
    ├── manage.py
    ├── requirements.txt
    ├── docker-compose.yml
    ├── dockerfile
    └── ...
```