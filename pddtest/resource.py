# -*- coding: utf-8 -*-
import json
from pddtest.generator import store_answer
import logging

HREF = 'href'
RIGHT_VARIANT_INDEX = 'right_variant_index'
VARIANTS = 'variants'
QUESTION = 'question'
CHAPTER_NUM = 'chapter_num'

class PddQuestion(object):
    """
    Question class
    """
    def __init__(self, question, variants, right_variant_index, chapter_num, href=None):
        self.question = question
        self.variants = variants
        self.right_variant_index = int(right_variant_index)
        self.chapter_num = float(chapter_num)
        self.href = href

    @classmethod
    def from_dict(cls, dict_question):
        return PddQuestion(
            dict_question.get(QUESTION),
            dict_question.get(VARIANTS),
            dict_question.get(RIGHT_VARIANT_INDEX),
            dict_question.get(CHAPTER_NUM),
            dict_question.get(HREF),
        )

    def to_dict_without_right_variant(self):
        return {
            QUESTION: self.question,
            VARIANTS: self.variants,
            CHAPTER_NUM: self.chapter_num,
            HREF: self.href,
        }
    
    def is_right_variant(self, variant_num):
        return bool(int(variant_num) == self.right_variant_index)

    def to_dict(self):
        return {
            QUESTION: self.question,
            VARIANTS: self.variants,
            RIGHT_VARIANT_INDEX: self.right_variant_index,
            CHAPTER_NUM: self.chapter_num,
            HREF: self.href,
        }

class PddTestWSResource(object):

    def __init__(self, questions):
        self.questions = questions

    def is_right_variant(self, question_num, variant_num):
        return self.questions[question_num].is_right_variant(variant_num)

    def to_json(self):
        return json.dumps([question.to_dict_without_right_variant() for question in self.questions])

class TestFailed(Exception):
    pass

class TestSuccess(Exception):
    pass

class AnswerAlreadyRegister(Exception):
    pass

class PddTest(PddTestWSResource):

    def __init__(self, questions, max_mistakes=1, login=None):
        self.curriculum = [None] * len(questions)
        self.login = login
        self.max_mistakes = max_mistakes
        self.mistakes = 0
        PddTestWSResource.__init__(self, questions)

    def is_right_variant(self, question_num, variant_num):
        if self.curriculum[question_num] is not None:
            raise AnswerAlreadyRegister
        question = self.questions[question_num]
        chapter_num = question.chapter_num
        result = question.is_right_variant(variant_num)
        store_answer(self.login, chapter_num, result)
        if not result:
            self.mistakes += 1
            if self.mistakes > self.max_mistakes:
                raise TestFailed
        self.curriculum[question_num] = result
        if not len(filter(lambda x: x is None, self.curriculum)):
            raise TestSuccess
        return result

    @classmethod
    def wrap(cls, resource, max_mistakes, login=None):
        return PddTest(resource.questions, max_mistakes, login)
