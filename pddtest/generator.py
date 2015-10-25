# -*- coding: utf-8 -*-
import redis
from ast import literal_eval
import random
# todo exclude to settings.py
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'

def generate_test(parts=[1, 2, 3, 4, 5, 6, 7], length=10, login=None):
    from pddtest.resource import PddQuestion, PddTestWSResource
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    if not isinstance(parts, list):
        parts = [int(parts)]
    questions_dict = {}
    for part in parts:
        questions = server.smembers('chapter.{}.question'.format(part))
        questions_dict[part] = [PddQuestion.from_dict(literal_eval(question)) for question in questions]
    if login:
        # todo rebuild for each person
        all_questions = []
        for question_list in questions_dict.values():
            all_questions.extend(question_list)
        questions = random.sample(all_questions, min(length, len(all_questions)))
    else:
        all_questions = []
        for question_list in questions_dict.values():
            all_questions.extend(question_list)
        questions = random.sample(all_questions, min(length, len(all_questions)))
    pdd_test_resource = PddTestWSResource(questions)
    return pdd_test_resource

def add_question_to_db(question, variants, right_variant_index, chapter_num, href=None):
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    question = PddQuestion(question, variants, right_variant_index, chapter_num, href=href)
    return server.sadd('chapter.{}.question'.format(int(float(chapter_num))), question.to_dict())

def store_answer(login, chapter, result):
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    server.incr('{}.{}.{}'.format(login, int(float(chapter)), result))

if __name__ == '__main__':
    # pdd_test_generator = PddTestGenerator()
    res = generate_test([2])
    print(res.to_json())
    res = res.is_right_variant(0, 2)
    # res = pdd_test_generator.add_question_to_db(
    #     u'Является ли водителем лицо, обучаемое управлению механическим транспортным средством?',
    #     {
    #         1: u'Не является',
    #         2: u'Является только при движении учебного транспортного средства по автодрому или площадке, закрытой для дорожного движения',
    #         3: u'Является только при движении учебного транспортного средства по дорогам общего пользования',
    #         4: u'Является только при нахождении в учебном транспортном средстве',
    #     },
    #     1,
    #     2.8,
    #     'http://pdd.by/pdd/ru/2.8/#i2.8',
    # )
    print(res)
