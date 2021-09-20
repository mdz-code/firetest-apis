from sqlalchemy.orm.session import Session
from fastapi import status
from ..database.mongo_db import MongoDatabase
from ..database import schemas, postgres_sql
from ..config.jwt import JwtAuth
from ..config.hashed import Hash
from ..config.mailing import Mailing

from datetime import datetime, timedelta

hash_instance = Hash()


class UserService:

    def __init__(self):
        self.__mongo_instance = MongoDatabase()
        self.__postgres_instance = postgres_sql.PostgresSQL()
        self.__jwt_handler = JwtAuth()
        self.__mailing = Mailing()
        pass


    async def feedback_user_questions(self, user_id: str):
        response = await self.__mongo_instance.get_one('feedbacks', { 'user_id': user_id })
        return {
                "status": status.HTTP_200_OK,
                "response": {
                   "correct_answer": len(response['correct_answer']),
                   "wrong_answer": len(response['wrong_answer']),
                   "answered_questions": len(response['wrong_answer']) + len(response['correct_answer']),
                }
            } 

    def get_current_user(self, user_id, db):
        response_user = self.__postgres_instance.get_user_by_id(user_id, db)
        response_user_infos = self.__postgres_instance.get_user_infos_by_user_id(str(response_user.__dict__['id']), db)

        dict_response = { 
            'complete_name': response_user.__dict__['complete_name'], 
            'email': response_user.__dict__['email'], 
            'premium': True,
            'schooling': response_user_infos.__dict__['schooling'],
            'institution': response_user_infos.__dict__['institution']
        }

        return {
                "status": status.HTTP_200_OK,
                "response": dict_response
            }


    async def store_new_user(self, user: schemas.User, db: Session):
        founded_user = self.__postgres_instance.get_user_by_email(
            user.account.email, db)
        if not founded_user:
            response = self.__postgres_instance.create_user(user.account, db)
            user_id = str(response.__dict__['id'])
            user.infos.user_id = user_id
            self.__postgres_instance.create_user_infos(user.infos, db)
            await self.__register_feedback_user(user_id)

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
        print(update_dict)
        self.__update_user(user_id, update_dict.account, db)
        if update_dict.infos != None:
            self.__update_user_infos(user_id, update_dict.infos, db)

        return {
            "status": status.HTTP_204_NO_CONTENT,
            "response": { }
        }

    def __create_feedback_user(self, user_id: str):
        return {
            "user_id": user_id,
            "correct_answer": [],
            "wrong_answer": [],
            "hard": [],
            "medium": [],
            "easy": [],
            "to_review": []
        }
   
    async def __register_feedback_user(self, user_id: str):
        inserted_object = self.__create_feedback_user(user_id)
        response = await self.__mongo_instance.insert_one('feedbacks', inserted_object)
        pass


    def __update_user(self, user_id: str, update_dict: dict, db: Session):
        update_dict_cleaned = {}

        for key, value in update_dict:
            print('tey')
            if value:
                if key != 'password':
                    update_dict_cleaned[key] = value 
                if key == 'password':
                    update_dict_cleaned['hashed_password'] = hash_instance.get_hashed_password(value)

        self.__postgres_instance.update_user(user_id, update_dict_cleaned, db)
        pass

    def __update_user_infos(self, user_id: str, update_dict: dict, db: Session):
        update_dict_cleaned = {}

        for key, value in update_dict:
            if value:
                if key != 'password':
                    update_dict_cleaned[key] = value 
                if key == 'password':
                    update_dict_cleaned['hashed_password'] = hash_instance.get_hashed_password(value)

        self.__postgres_instance.update_user_infos(user_id, update_dict_cleaned, db)
        pass
        

    def logout_user(self, token: str):
        new_token = self.__jwt_handler.logout(token)
        return {
            "status": status.HTTP_205_RESET_CONTENT,
            "response": { "new_token": new_token }
        }

    def recover_user(self, email_dict: str, db):
        response = self.__postgres_instance.get_user_by_email(email_dict.email, db)

        user_uuid = str(response.__dict__['id'])
        user_fullname = str(response.__dict__['complete_name'])
        token = self.__jwt_handler.encode_token(user_uuid)
        recover_dict = { 'user_id': user_uuid, 'used': False, 'token': token, 'subscription_date': datetime.now()}
        new_register = self.__postgres_instance.create_recover(recover_dict, db)
        recover_uuid = str(new_register.__dict__['id'])
        
        self.__mailing.send_email(email_dict.email, { 'subject': '🔮 Vamos recuperar sua senha agora!', 'complete_name': user_fullname, 'uuid_recover': recover_uuid }, 'recover')

        return {
            "status": status.HTTP_201_CREATED,
            "response": { "recover_id": recover_uuid }
        }

    def get_recover_user(self, uuid: str, db):

        response = self.__postgres_instance.get_recover_by_id(uuid, db)

        if response == None:
            return {
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "response": { "mensagem": "O convite não foi encontrado em nosso banco de dados." }
            }

        subscription_date = response.__dict__['subscription_date']
        date_select = datetime.fromisoformat(subscription_date)
        now = datetime.now()


        if not date_select + timedelta(minutes=30) <= now:
            token = response.__dict__['token']
            user_uuid = str(response.__dict__['user_id'])

            return {
                "status": status.HTTP_200_OK,
                "response": { "token": token }
            }
        
        return {
            "status": status.HTTP_403_FORBIDDEN,
            "response": { "mensagem": "O convite já expirou, por favor realize a recuperação novamente." }
        }


"""
endpoint de retorno das informações
    - retornar sempre premium true OK
endpoint de recuperação de conta
    - service de e-mail OK
    - modelo de recuperação de conta OK
    
"""
