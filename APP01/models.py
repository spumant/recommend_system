from django.db import models
import mongoengine
from recommend_system.settings import DATABASES

mongoengine.connect(DATABASES['mongodb']['NAME'], username='root', password='adc21nii754bew23facn',
                    authentication_source='admin',
                    # host='mongodb://root:root@43.138.33.205:27017/'
                    host='43.138.33.205', port=27017
                    )


class Item(mongoengine.Document):
    id = mongoengine.StringField()
    title = mongoengine.StringField()
    txt = mongoengine.ListField()
    img = mongoengine.StringField()
    tag = mongoengine.StringField()
    like = mongoengine.IntField()
    collection = mongoengine.IntField()
    meta = {'collection': 'item', 'strict': False}


class Video(mongoengine.Document):
    id = mongoengine.StringField()
    title = mongoengine.StringField()
    txt = mongoengine.ListField()
    img = mongoengine.StringField()
    tag = mongoengine.StringField()
    like = mongoengine.IntField()
    collection = mongoengine.IntField()
    meta = {'collection': 'shipin', 'strict': False}


class Collection(models.Model):
    user = models.IntegerField()
    collection = models.CharField(max_length=99)
    category = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'collection'


class Love(models.Model):
    user = models.IntegerField()
    love = models.CharField(max_length=99)
    category = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'love'


class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.IntegerField()
    itemid = models.IntegerField()
    tagid = models.IntegerField()
    time = models.IntegerField()
    love = models.IntegerField()
    col = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'log'


class Question(models.Model):
    qid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'question'


class Special(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'special'


class Users(models.Model):
    name = models.CharField(max_length=99)
    password = models.CharField(max_length=99)

    class Meta:
        managed = False
        db_table = 'users'


class Week(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=255)
    year = models.IntegerField()
    time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'week'


class Wrong(models.Model):
    userid = models.IntegerField()
    title = models.CharField(max_length=255, db_collation='utf8_general_ci')
    a = models.CharField(max_length=255, db_collation='utf8_general_ci')
    b = models.CharField(max_length=255, db_collation='utf8_general_ci')
    c = models.CharField(max_length=255, db_collation='utf8_general_ci')
    d = models.CharField(max_length=255, db_collation='utf8_general_ci')
    ans = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wrong'


class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tag'
