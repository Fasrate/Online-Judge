from django.db import models
from django.utils import timezone

# Create your models here.

class Problem(models.Model):
    probid = models.CharField(max_length=200)
    statement = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    difficulty= models.CharField(max_length=200,default="easy")

    def __str__(self):
        return self.probid

class Solution(models.Model):
    probid = models.CharField(max_length=200)
    verdict = models.CharField(max_length=200)
    submittedat=models.DateTimeField(default=timezone.now)
 
class TestCase(models.Model):
    probid = models.CharField(max_length=200)
    input = models.CharField(max_length=200)
    output = models.CharField(max_length=200)
 
