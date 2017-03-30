from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    """
        Contains fields for frequently asked questions and their answer.
    """
    question = models.CharField('question', max_length=80)
    answer = models.TextField('answer')
    order = models.IntegerField('order')

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.question
