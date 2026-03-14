# Agent Orchestrator REST API

This project implements a REST API for an agent orchestrator using FastAPI. The orchestrator is designed to dynamically select and manage sub-agents based on a given prompt.

## Overview

The core of this project is the `Orchestator` which leverages the `google.adk` library to manage a sequence of agents. It dynamically constructs instructions for a main `SequentialAgent` based on the registered sub-agents.

The API exposes endpoints for health checks and for interacting with the chat functionality.

## Features

- **Dynamic Agent Orchestration**: The main agent's behavior is configured based on the available sub-agents.
- **FastAPI Integration**: A robust and fast web framework for building APIs.
- **Pydantic Models**: Used for data validation and settings management.
- **Docker Support**: Comes with a `Dockerfile` for easy containerization and deployment.

## Class Diagram

Here is a diagram of the main classes in the project:

```mermaid
classDiagram
    class ChatRequest {
        +message: str
        +source: Optional[str]
        +gen_model_to_use: Optional[str]
    }

    class Settings {
        +log_level: str
    }

    class Orchestator {
        -model_name: str
        -key: str
        -model_url: str
        -llm: OpenAICompatibleModel
        -agents: list[Agent]
        -main_agent: SequentialAgent
        +__init__(model_name, key, model_url, agents)
        - __init_llm()
        - __init_main_agent()
        +run(input: str)
    }

    class AgentMetadata {
        +agent: str
        +location: str
        +key_path: str
        +description: str
        +author: str
    }

    class AgentRepository {
        <<interface>>
        +find_by_friendly_name(friendly_name: str) Optional[AgentMetadata]
        +search(author: str, location: str) List[AgentMetadata]
    }

    class "FastAPI Endpoints" as Endpoints {
        +/chat (POST)
        +/health (GET)
    }

    Orchestator --|> Agent
    Orchestator o-- "OpenAICompatibleModel"
    Orchestator o-- "SequentialAgent"
    Endpoints ..> ChatRequest : uses
    AgentRepository ..> AgentMetadata : returns
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker

### Installation and Running

1.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    uvicorn src.agent.main:app --reload
    ```

3.  The API will be available at `http://localhost:8000`.

### Running with Docker

1.  Build the Docker image:
    ```bash
    docker build -t agent-orchestrator .
    ```

2.  Run the Docker container:
    ```bash
    docker run -p 8000:8000 agent-orchestrator
    ```

