from django.db import models

# Create your models here.


class Sales(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProcessBusiness(models.Model):
    title = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title
