# -*- coding: utf-8 -*-
import redis
from ast import literal_eval
import random
# todo exclude to settings.py
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'

PART_CHAPTER_DICT = {
    1: (1, 25),
    2: (25, 114),
    3: (115, 212),
}

def get_part(chapter):
    for part, chapter_range in PART_CHAPTER_DICT.items():
        if chapter in range(chapter_range[0], chapter_range[1]):
            return part

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

def add_question_to_db(question_str, variants, right_variant_index, chapter_num, href=None):
    from pddtest.resource import PddQuestion
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    question = PddQuestion(question_str, variants, right_variant_index, chapter_num, href=href)
    chapter_num_int = int(float(chapter_num))
    return server.sadd('chapter.{}.question'.format(get_part(chapter_num_int)), question.to_dict())

def store_answer(login, chapter, result):
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    server.incr('{}.{}.{}'.format(login, int(float(chapter)), result))

def get_question_count():
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    return {k: len(server.smembers('chapter.{}.question'.format(k))) for k in PART_CHAPTER_DICT.keys()}

def main():
    s = u'''Что должен делать водитель при ослеплении?
Включить аварийную световую сигнализацию и, не перестраиваясь, снизить скорость и остановиться.
Не перестраиваясь, остановиться и включить аварийную сигнализацию.
Включить аварийную сигнализацию, перестроиться на правую полосу и остановиться.
Включить аварийную сигнализацию, съехать на обочину и остановиться.
Перестроиться на правую полосу, включить аварийную сигнализацию, снизить скорость и остановиться.
    '''
    question = s.split('\n')[0]
    variants_list = [item.replace('\n', '') for item in s.split('\n')[1:]]
    chapter = 163.1
    right = 4
    variants_list = [item.replace('\n', '') for item in variants_list]
    variants = {i + 1: x for i, x in enumerate(variants_list)}
    res = add_question_to_db(
        question,
        variants,
        right,
        chapter,
        'http://pdd.by/pdd/ru/{chapter}/#i{chapter}'.format(chapter=chapter),
    )
    print(res)
    print(get_question_count())

if __name__ == '__main__':
    main()
