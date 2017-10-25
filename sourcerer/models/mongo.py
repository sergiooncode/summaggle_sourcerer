# -*- coding: utf-8 -*-
from mongoengine import *


class InitialSearch(Document):
    source = StringField(max_length=50, required=True)
    result_links = ListField(StringField(max_length=500))
    search_terms = ListField(StringField(max_length=50))
    links_last_scraped_at = DateTimeField()


class Answer(EmbeddedDocument):
    answer_markup = StringField(max_length=10000, required=True)
    tags = ListField(StringField(max_length=50))


class QuestionAnswers(Document):
    question_markup = StringField(max_length=10000, required=True)
    source = StringField(max_length=50, required=True)
    tags = ListField(StringField(max_length=50))
    answers = EmbeddedDocumentListField(Answer)


class InitialSearchToLinkStringToQuestionAnswers(Document):
    initial_search = ReferenceField(InitialSearch)
    link_list_index = IntField()
    link_string = StringField(max_length=500)
    question_answers = ReferenceField(QuestionAnswers)
