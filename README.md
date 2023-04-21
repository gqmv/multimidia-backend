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

## Usage
The API is available at `http://localhost:8000/api/` by default.

An OpenAPI-compliant schema is available at `http://localhost:8000/api/schema/` by default.

Documentation is available at `http://localhost:8000/api/schema/redoc/` by default.

