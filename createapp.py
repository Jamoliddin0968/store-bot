import argparse
import os

"""
from fastapi import APIRouter

router = APIRouter(prefix="dmtt")


@router.get("/all")
def get_all_dmtt():
    return {"hello": "world"}

"""


def create_app_structure(app_name):
    base_path = 'src'
    models_path = os.path.join(base_path, 'models')
    services_path = os.path.join(base_path, 'services')
    schemas_path = os.path.join(base_path, 'schemas')
    routers_path = os.path.join(base_path, 'routers')
    os.makedirs(models_path, exist_ok=True)
    os.makedirs(services_path, exist_ok=True)
    os.makedirs(schemas_path, exist_ok=True)
    os.makedirs(routers_path, exist_ok=True)

    # Creating app_name.py files in each directory
    with open(os.path.join(models_path, f'{app_name}.py'), 'w') as models_file:
        models_file.write("""#Your models for the app
from sqlalchemy import Boolean, Column, Integer, String

from src.models.base import BaseModel
""")

    with open(os.path.join(services_path, f'{app_name}.py'), 'w') as services_file:
        services_file.write("""# new_user = models.User(name=request.name, email=request.email, password=request.password)
    # database.add(new_user)
    # database.commit()
    # database.refresh(new_user)
    # return new_user""")

    with open(os.path.join(schemas_path, f'{app_name}.py'), 'w') as schemas_file:
        schemas_file.write("from pydantic import BaseModel")
    with open(os.path.join(routers_path, f'{app_name}.py'), 'w') as routers_file:
        routers_file.write(f"""
from fastapi import APIRouter

router = APIRouter(prefix='{app_name}')


@router.get("/all")
def get_all_{app_name}():
    return {{"hello": "world"}}

""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create app structure')
    parser.add_argument('appname', type=str, help='Name of the app')

    args = parser.parse_args()
    app_name = args.appname

    create_app_structure(app_name)
