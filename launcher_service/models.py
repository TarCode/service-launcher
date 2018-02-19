import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField



class DateModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)


class Company(DateModel):
    identifier = models.CharField(max_length=100, unique=True, db_index=True)
    admin = models.OneToOneField('launcher_service.User',
        related_name='admin_company')
    secret = models.UUIDField()
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.identifier

    def natural_key(self):
        return (self.identifier,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.secret = uuid.uuid4()

        return super(Company, self).save(*args, **kwargs)


class User(DateModel):
    identifier = models.UUIDField()
    token = models.CharField(max_length=200, null=True)
    company = models.ForeignKey('launcher_service.Company', null=True)

    def __str__(self):
        return str(self.identifier)


class Currency(DateModel):
    company = models.ForeignKey('launcher_service.Company')
    code = models.CharField(max_length=12, db_index=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    symbol = models.CharField(max_length=30, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    divisibility = models.IntegerField(default=2)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code)


class Join(DateModel):
    email = models.EmailField()
    group = models.CharField(max_length=20)
    share_id = models.CharField(max_length=20)


class Campaign(DateModel):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rewards = JSONField(default=dict)
    status = models.BooleanField(default=True)
    volume = models.IntegerField()
    limit = models.IntegerField()



