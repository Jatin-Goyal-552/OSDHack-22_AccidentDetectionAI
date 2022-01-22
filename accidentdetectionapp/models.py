from django.db import models

# Create your models here.

# from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Notifications(models.Model):
    n_id=models.AutoField(primary_key=True)
    notification = models.CharField(max_length=1000)
    accident_date = models.DateTimeField(auto_now_add=True)
    lattitude=models.FloatField(blank=True,null=True)
    longitude= models.FloatField(blank=True,null=True)
    accepted = models.IntegerField(blank=True,null=True)
    # semester = models.IntegerField(null=True)
    # other_qualifications=models.TextField(blank=True,null=True)
    # stipend=models.FloatField(blank=True,null=True)
    # date=models.CharField(max_length=100,null=True)
    def __str__(self):
        return f"{self.n_id}"


class Hospital(models.Model):
    h_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    email=models.EmailField()
    h_lattitude=models.FloatField(blank=True,null=True)
    h_longitude= models.FloatField(blank=True,null=True)
    def __str__(self):
        return f"{self.h_id}-{self.name}"