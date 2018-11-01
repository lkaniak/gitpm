from djongo import models
from django import forms

class User(models.Model):
  _id = models.ObjectIdField()
  username = models.CharField(max_length=128)
  password = models.CharField(max_length=32)
  name = models.CharField(max_length=128)
  email = models.CharField(max_length=128)

  class Meta:
    db_table = "User"

class ModifiedFiles(models.Model):
  _id = models.ObjectIdField()
  modifiedFile = models.CharField(max_length=200)
  additions = models.IntegerField()
  changes = models.IntegerField()
  deletions = models.IntegerField()
  status = models.CharField(max_length=30)

  class Meta:
    abstract = True

class ModifiedFilesForm(forms.ModelForm):
  class Meta:
    model = ModifiedFiles
    fields = (
        'modifiedFile',
        'additions',
        'changes',
        'deletions',
        'status'
    )

class Repository(models.Model):
  _id = models.ObjectIdField()
  name = models.CharField(max_length=128)
  onwer = models.CharField(max_length=128)
  url = models.CharField(max_length=128)

  class Meta:
    db_table = "Repository"


class Commit(models.Model):
  _id = models.ObjectIdField()
  repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
  user = models.CharField(max_length=128)
  hashID = models.CharField(max_length=40)
  email = models.EmailField()
  date = models.DateTimeField()
  message = models.CharField(max_length=1024)
  modifiedFiles = models.ArrayModelField(
        model_container=ModifiedFiles,
        model_form_class=ModifiedFilesForm
    )
  objects = models.DjongoManager()

  class Meta:
    db_table = "Commit"

  # def __str__(self):
  #   return 'id: {} hash: {}'.format(self._id, self.hashID)


class EventLog(models.Model):
  _id = models.ObjectIdField()
  repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
  name = models.CharField(max_length=128)
  created_at = models.DateTimeField()

  class Meta:
    db_table = "EventLog"

class EventLogFields(models.Model):
  _id = models.ObjectIdField()
  log = models.ForeignKey(EventLog, on_delete=models.CASCADE)
  caseID = models.IntegerField()
  activity = models.CharField(max_length=255)
  timestamp = models.DateTimeField()
  commit = models.CharField(max_length=40)

  class Meta:
    db_table = "EventLogFields"

class EventLogFieldsForm(forms.ModelForm):
  class Meta:
    model = EventLogFields
    fields = (
        'caseID',
        'activity',
        'timestamp',
        'commit'
    )


class ProcessModelFields(models.Model):
  template = models.CharField(max_length=32)
  parameters = models.ListField()
  support = models.CharField(max_length=10)
  confidence = models.CharField(max_length=10)
  interestFactor = models.CharField(max_length=10)

  class Meta:
    abstract = True


class ProcessModel(models.Model):
  _id = models.ObjectIdField()
  eventlog = models.ForeignKey(EventLog, on_delete=models.CASCADE)
  name = models.CharField(max_length=152)
  tasks = models.ListField()
  constraints = models.ArrayModelField(
        model_container=ProcessModelFields
    )

  class Meta:
    db_table: "ProcessModel"


  objects = models.DjongoManager()
