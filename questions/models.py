from __future__ import unicode_literals

from Users.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    favorites = models.IntegerField(default=0)
    has_accepted_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-update_date',)


    def __str__(self):
        return self.title


    @staticmethod
    def get_unanswered():
        return Question.objects.filter(has_accepted_answer=False)

    @staticmethod
    def get_answered():
        return Question.objects.filter(has_accepted_answer=True)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_accepted=True)

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    def get_description_preview(self):
        if len(self.description) > 255:
            return '{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_description_preview_as_markdown(self):
        return markdown.markdown(self.get_description_preview(),
                                 safe_mode='escape')


@python_2_unicode_compatible
class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    votes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)    


    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-is_accepted', '-votes', 'create_date',)

    def __str__(self):
        return self.description

    def accept(self):
        answers = Answer.objects.filter(question=self.question)
        for answer in answers:
            answer.is_accepted = False
            answer.save()
        self.is_accepted = True
        self.save()
        self.question.has_accepted_answer = True
        self.question.save()


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    question = models.ForeignKey(Question)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        unique_together = (('tag', 'question'),)
        index_together = [['tag', 'question'], ]

    def __str__(self):
        return self.tag        