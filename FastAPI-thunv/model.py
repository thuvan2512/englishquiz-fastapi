from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import String, Integer, Text
from database import *
model_orm = get_model_orm()

class CategoriesORM(model_orm):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    questions = relationship('QuestionORM', lazy = True, backref = 'category')
    def __str__(self):
        return "{} - {}".format(self.id, self.name)

class QuestionORM(model_orm):
    __tablename__ = "question"
    id = Column(String, primary_key=True)
    content = Column(String)
    category_id = Column(Integer, ForeignKey(CategoriesORM.id))
    choices = relationship('ChoiceORM', lazy=False, backref='question')
    def __str__(self):
        return "{} - {}".format(self.id, self.content)

class ChoiceORM(model_orm):
    __tablename__ = "choice"
    id = Column(String, primary_key=True)
    content = Column(String)
    is_correct = Column(Integer)
    question_id = Column(String, ForeignKey(QuestionORM.id))
    def __str__(self):
        return "{} - {}".format(self.content, self.is_correct)
