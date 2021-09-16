from fastapi import status
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import json
import ast

from ..database.mongo_db import MongoDatabase
from ..database.schemas import ObjectInfos
from ..config.mailing import Mailing


class QuestionService:

    def __init__(self):
        self.__mongo_instance = MongoDatabase()
        self.__mailing = Mailing()
        self.__mode_dict = {
            'train': self.__train_mode,
            'select': self.__select_mode
        }
        pass

    async def get_all_subjects(self):
        return await self.__mongo_instance.get_all_itens()

    async def start_simulate(self, train_mode: bool, user_id: str, object_infos: dict = None):
        mode = 'train' if train_mode else 'select'
        execute_function = self.__mode_dict[mode]
        response = await execute_function(user_id, object_infos)
        return {
            "status": status.HTTP_201_CREATED,
            "response": { "simulate_id": response }
        }

    async def finsh_simulate(self, simulate_id: str):
        is_finished = await self.__is_finished(simulate_id)
        if not is_finished:
            finsh_time = { 'end_time': datetime.utcnow() }
            await self.__mongo_instance.update_one('simulates', { '_id': ObjectId(simulate_id) }, finsh_time)
            return {
            "status": status.HTTP_204_NO_CONTENT,
            "response": { }
        }

        return {
            "status": status.HTTP_409_CONFLICT,
            "response": { "mensagem": "Esta nota já foi cancelada" }
        }

    async def get_question_by_simulate(self, simulate_id: str):
        response_list = []
        simulate_infos = await self.__mongo_instance.get_one('simulates', { '_id': ObjectId(simulate_id)})

        selected_questions = await self.__mongo_instance.complex_query(
                'questions', 
                year=simulate_infos['years'], 
                subjects=simulate_infos['subjects'], 
                questions=simulate_infos['questions']
            )

        print(len(selected_questions))

        for question_dict in selected_questions:
            for key in question_dict:
                if '[' in question_dict[key]:
                    question_dict[key] = ast.literal_eval(question_dict[key])

            response_list.append(question_dict)

        random.shuffle(response_list)

        return {
            "status": status.HTTP_200_OK,
            "response": response_list
        }

    async def __is_finished(self, simulate_id: str):
        response = await self.__mongo_instance.get_one('simulates', { '_id': ObjectId(simulate_id) })
        end_time = response['end_time']
        return True if end_time is not None else False

    async def __train_mode(self, user_id: str, object_infos=None):
        dict_simulate = self.__create_dict_simulate(user_id)
        simulate_id = await self.__mongo_instance.insert_one('simulates', dict_simulate, True)
        return str(simulate_id)

    async def __select_mode(self, user_id: str, object_infos: ObjectInfos = None):
        dict_simulate = self.__create_dict_simulate(user_id, object_infos.years, object_infos.subjects)
        simulate_id = await self.__mongo_instance.insert_one('simulates', dict_simulate, True)
        return str(simulate_id)

    def __create_dict_simulate(self, user_id: str, years: list = [], subjects: list = []):
        return {
            'user_id': user_id,
            'questions': [],
            'subjects': subjects,
            'years': years,
            'start_time': datetime.utcnow(),
            'end_time': None,
        }

    async def send_report(self, user_id: str, question_id: str, text_report: str):
        dict_report = self.__create_dict_report(user_id, question_id, text_report)
        await self.__mongo_instance.insert_one('reports', dict_report)
        for dev_email in ['lameranha@gmail.com', 'leolamerabr@gmail.com']:
            self.__mailing.send_email(dev_email, { 'subject': '🚨 DEU ERRO NO APP!', 'text': text_report}, 'report')
        return {
            "status": status.HTTP_204_NO_CONTENT,
            "response": {}
        }

    def __create_dict_report(self, user_id: str, question_id: str, text_report: str):
        return {
            'user_id': user_id,
            'question_id': question_id,
            'text_report': text_report,
        }


    




"""
    OK - start
    OK - stop
    OK - find_by_simulate_id
    answers and feedback
    subjects
    reporter  
"""
