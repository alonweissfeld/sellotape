from django.db import models
from django.contrib.auth.models import User

class Stream(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(max_length=500, blank=False)
    title = models.CharField(max_length=50, default='')
    airs_on = models.DateTimeField()
    ends_on = models.DateTimeField(null=True)
    added_on = models.DateTimeField()

    class Meta:
        ordering = ['airs_on', 'author']
        db_table = 'streams'
