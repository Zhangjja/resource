

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Path(models.Model):
	url = models.CharField(max_length=300)

	def  __unicode__(self):
		return self.url

