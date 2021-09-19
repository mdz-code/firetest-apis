from fastapi import status
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import json
import ast

from ..database.mongo_db import MongoDatabase
from ..database.schemas import ObjectInfos, FeedbackRegister
from ..config.mailing import Mailing


class QuestionService:

    def __init__(self):
        self.__mongo_instance = MongoDatabase()
        self.__mailing = Mailing()
        self.__mode_dict = {
            'train': self.__train_mode,
            'select': self.__select_mode
        },
        self.__forget_goals = {
            'easy': timedelta(days=7),
            'medium': timedelta(days=3),
            'hard': timedelta(days=1),
 
        }
        pass

    async def register_feedback(self, dto: FeedbackRegister, user_id: str):

        print(dto)
        # buscar questões por uuid do usuário - OK
        response = await self.__mongo_instance.get_one('feedbacks', { 'user_id': user_id })
        
        question_id = dto.question_id
        feedback = dto.feedback
        answer = 'correct_answer' if dto.correct else 'wrong_answer'
        
        feedback_list = [x for x in response[feedback]]
        answer_list = [x for x in response[answer]]

        # registrar nova question_id no correct or false
        answer_list.append(question_id)
        response[answer] = answer_list

        # registrar nova question_id no easy, medium ou hard
        feedback_list.append(question_id)
        response[feedback] = feedback_list

        # calculo de revisão para adicionar no registro
        now_datetime = datetime.now()
        goal_datetime = self.__forget_goals[feedback]
        review_gol = now_datetime + goal_datetime

        # adicionar o module_id da questão
        to_review_list = [x for x in response['to_review']]
        question_response = await self.__mongo_instance.get_one('questions', {'_id': ObjectId(question_id)})
        print(question_response)

        if question_response['module_id'] != None:
            for module_id in question_response['module_id']:
                to_review_list.append({ 'module_id': module_id, 'start_at': review_gol})

            response['to_review'] = to_review_list

        # update no registro resgatado pelo uuid
        await self.__mongo_instance.update_one('feedbacks', { 'user_id': user_id }, response)

        return {
            "status": status.HTTP_204_NO_CONTENT,
            "response": {}
        }

    async def get_all_subjects(self):
        return await self.__mongo_instance.get_all_itens()

    async def start_simulate(self, train_mode: bool, user_id: str, object_infos: dict = None):

        dict_functions = {
            'train': self.__train_mode,
            'select': self.__select_mode
        }

        mode = 'train' if train_mode else 'select'
        execute_function = dict_functions[mode]
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

    async def get_question_by_simulate(self, simulate_id: str, user_id: str):
        simulate_infos = await self.__mongo_instance.get_one('simulates', { '_id': ObjectId(simulate_id)})
        if simulate_infos['mode'] == 'train':

            train_questions = await self.__mongo_instance.train_mode_questions(user_id)
            random.shuffle(train_questions)

            return {
                "status": status.HTTP_200_OK,
                "response": train_questions
            }


        selected_questions = await self.__mongo_instance.complex_query(
                'questions', 
                year=simulate_infos['years'], 
                subjects=simulate_infos['subjects'], 
                questions=simulate_infos['questions']
            )

        random.shuffle(selected_questions)

        return {
            "status": status.HTTP_200_OK,
            "response": selected_questions
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
        dict_simulate = self.__create_dict_simulate(user_id, 'select', object_infos.years, object_infos.subjects)
        simulate_id = await self.__mongo_instance.insert_one('simulates', dict_simulate, True)
        return str(simulate_id)

    def __create_dict_simulate(self, user_id: str, mode='train', years: list = [], subjects: list = []):
        return {
            'user_id': user_id,
            'mode': mode,
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
