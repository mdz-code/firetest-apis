from sqlalchemy.orm.session import Session
from fastapi import status
from ..database.mongo_db import MongoDatabase
from ..database import schemas, postgres_sql
from ..config.jwt import JwtAuth
from ..config.hashed import Hash

hash_instance = Hash()


class UserService:

    def __init__(self):
        self.__mongo_instance = MongoDatabase()
        self.__postgres_instance = postgres_sql.PostgresSQL()
        self.__jwt_handler = JwtAuth()
        pass

    def get_current_user(self, user_id, db):
        response = self.__postgres_instance.get_user_by_id(user_id, db)
        dict_response = { 'complete_name': response.__dict__['complete_name'], 'email': response.__dict__['email']}
        return {
                "status": status.HTTP_200_OK,
                "response": dict_response
            }


    def store_new_user(self, user: schemas.User, db: Session):
        founded_user = self.__postgres_instance.get_user_by_email(
            user.email, db)
        if not founded_user:
            self.__postgres_instance.create_user(user, db)
            return {
                "status": status.HTTP_201_CREATED,
                "response": {
                    "message": "O usuário foi cadastrado com sucesso."
                }
            }

        return {
            "status": status.HTTP_409_CONFLICT,
            "response": {
                "message": "O e-mail informado já foi cadastrado anteriormente."
            }
        }

    def auth_user(self, user: schemas.UserAuth, db: Session):
        founded_user = self.__postgres_instance.get_user_by_email(
            user.email, db)
        if founded_user:
            database_password = founded_user.__dict__['hashed_password']
            if self.__postgres_instance.auth_user(database_password, user.password):
                user_id = str(founded_user.__dict__['id'])
                token = self.__jwt_handler.encode_token(user_id)
                return {
                    "status": status.HTTP_202_ACCEPTED,
                    "response": {
                        "token": token
                    }
                }

            return {
                "status": status.HTTP_403_FORBIDDEN,
                "response": {
                    "message": "A senha informada não é igual a registrada no banco de dados."
                }
            }

        return {
            "status": status.HTTP_404_NOT_FOUND,
            "response": {
                "message": "O e-mail informado não consta em nosso banco de dados."
            }
        }

    def update_user(self, user_id: str, update_dict: dict, db: Session):
        update_dict_cleaned = {}

        for key, value in update_dict:
            if value:
                if key != 'password':
                    update_dict_cleaned[key] = value 
                if key == 'password':
                    update_dict_cleaned['hashed_password'] = hash_instance.get_hashed_password(value)

        self.__postgres_instance.update_user(user_id, update_dict_cleaned, db)

        return {
            "status": status.HTTP_204_NO_CONTENT,
            "response": { }
        }

    def logout_user(self, token: str):
        new_token = self.__jwt_handler.logout(token)
        return {
            "status": status.HTTP_205_RESET_CONTENT,
            "response": { "new_token": new_token }
        }


"""
    OK - create
    OK - login
    OK - logout
    OK - update
    feedback
    recover
"""
