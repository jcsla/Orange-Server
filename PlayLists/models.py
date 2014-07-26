from django.db import models

# Create your models here.
class PlayList(models.Model):
	name = models.CharField(max_length=200)
	cnt = models.IntegerField()
	def __unicode__(self):
		return self.name
	#def __unicode__(self):
	#	return u'%s %s' % (self.name, self.cnt)