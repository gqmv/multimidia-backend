# **BrainIAc API**
*For internal use only*


## Installation
To install the BrainIAc API, you need to have a working Python 3.8+ installation.

1. Clone the repository
    ```bash
    git clone [repoUrl]
    ```
2. Setup a virtual environment
    ```bash
    python3 -m venv .venv
    ```
3. Activate the virtual environment
    
    For Windows, run:
    ```bash
    .venv\Scripts\activate.bat
    ```
    For Linux or MacOS run:
    ```bash
    source .venv/bin/activate
    ```
4. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```
5. Run the API
    ```bash
    cd src/
    python manage.py runserver
    ```

## Environment variables
The following environment variables need to be defined in order to run the API:

| Variable         | Description                                                                                    | Default |
| ---------------- | ---------------------------------------------------------------------------------------------- | ------- |
| `ENV`            | The environment the API is running in. This is used to load the correct Django Settings Module | `local` |
| `SECRET_KEY`     | The secret key used by Django                                                                  | `None`  |
| `OPENAI_API_KEY` | The API key for OpenAI                                                                         | `None`  |
| `DEBUG`          | Whether to run the API in debug mode                                                           | `False` |

*In development, a `.env` file can be used to define the environment variables.*

*Note: Due to it's nature, the `ENV` environment variable cannot be defined in the `.env` file. For development, it is recommended to use it's default value.*


## Usage
The API is available at `http://localhost:8000/api/` by default.

An OpenAPI-compliant schema is available at `http://localhost:8000/api/schema/` by default.

Documentation is available at `http://localhost:8000/api/schema/swagger-ui/` by default.


