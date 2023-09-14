from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, EmailField, DateTimeField
from djongo.models import ObjectIdField
from .models import (User, Repository, Commit, EventLog, ProcessModel, EventLogFields)

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class ModifiedFilesSerializer(serializers.Serializer):
  modifiedFile = CharField(max_length=200)
  additions = IntegerField()
  changes = IntegerField()
  deletions = IntegerField()
  status = CharField(max_length=30)

class CommitSerializer(serializers.ModelSerializer):
  _id = ObjectIdField()
  modifiedFiles = serializers.SerializerMethodField()
  user = CharField(max_length=128)
  hashID = CharField(max_length=40)
  email = EmailField()
  date = DateTimeField()
  message = CharField(max_length=510)

  class Meta:
    model = Commit
    exclude = ('_id',)

  def get_modifiedFiles(self, obj):
    resources_serializer = ModifiedFilesSerializer(obj.modifiedFiles, many=True)
    return resources_serializer.data

class GitRepositorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Repository
    fields = '__all__'

class EventLogSerializer(serializers.ModelSerializer):
  class Meta:
    model = EventLog
    exclude = ('_id', 'repository')

class EventLogFieldsSerializer(serializers.ModelSerializer):
  class Meta:
    model = EventLogFields
    exclude = ('_id', 'log')

class ProcessModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProcessModel
    exclude = ('_id',)

class GenericSerializer(serializers.Serializer):
  data = serializers.JSONField
