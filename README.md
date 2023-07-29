# This is boilerplate of flask restful
### This boilerplate consists of following
- SqlAlchemy
- Redis
- jwt authentication and authorization
- Logger
- swagger
- docker

#### First go to the web directory
    cd web
### Python 3.6 Virtual environment:
    
    python3 -m venv venv  # if not created already
    source venv/bin/activate
    pip install --upgrade pip

### Install requirements:

    pip install -r requirements.txt

### Export environment variables:

    export FLASK_SECRET=my_secret  # depending on deployment
    export FLASK_ENV=production/development  # depending on deployment
