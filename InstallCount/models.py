from django.db import models

# Create your models here.
class InstallCount(models.Model):
	count = models.IntegerField()
	def __unicode__(self):
		return self.count