# AI-Chat-Bot-IFSGuide

## Description

This is a simple app to perform as an AI chatbot for IFS Guide. It is built using FastAPI and Python 3. It is designed using the Clean Architecture design pattern.

The AI side is provided by a free library called [GPT4Free](https://github.com/xtekky/gpt4free).


## Features

- Clean Architecture design pattern
- Web framework layer using FastAPI
- Modular and flexible architecture
- Examples of common features such as authentication, authorization, and CRUD operations

## Requirements

### PostgreSQL docker image

1. Please install Docker and Docker Compose and then run the following command:

```bash
docker pull postgres:latest
```

### config files

In the `src/config_files` folder, there are 2 files that are required to run the app.
Change the names from `database.env.example` and `service.env.example` to `database.env` and `service.env` respectively.
Fill or change the required information in the files.


## How to run

### Using Docker

1. Install Docker and Docker Compose
2. Run the following command in the root directory of the project:

```bash
docker network create ai_chat_bot_service_network
bash cmd/build-docker.sh
bash cmd/start.sh
```

3. The app should be running on http://0.0.0.0:6601/

4. if any problem occurs, run the following command to see the logs and find the problem:

```bash
docker compose logs -f
```

### Using Python - Only for pytest

1. Install Python 3.8+ or using Anaconda
2. Install the dependencies using the following command:

```bash
pip install -r requirements.txt
```
or 
```bash
conda create --name <env> python=3.10
conda activate <env>
pip install -r requirements.txt
```

3. Run the following command in the root directory of the project:

```bash
pytest
```

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
    │   │   │       ├── repositories
    │   │   │       ├── manage.py
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