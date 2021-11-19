from django.db import models
import re

class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) < 2:
            errors['first_name'] = "First name is too short"
        if len(reqPOST['last_name']) < 1:
            errors['last_name'] = "Last name is too short"
        if len(reqPOST['user_email']) < 6:
            errors['user_email'] = "Email is too short"
        if len(reqPOST['user_password']) < 8:
            errors['user_password'] = "Password is too short"
        if reqPOST['user_password'] != reqPOST['user_password_conf']:
            errors['user_password_conf'] = "Passwords do not match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['user_email']):
            errors["regex_issue"] = "Invalid email address"
        existing_emails = User.objects.filter(email=reqPOST['user_email'])
        if len(existing_emails) >= 1:
            errors['duplicate_email'] = "This email already exists"
        return errors

class PollManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['question_text']) < 2:
            errors['no_text_error'] = "Not enough text! Add a little more..."
        return errors

class AnswerManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['answer_text']) < 1:
            errors['no_text_error'] = "Answer choice is too short. Add a little more!"
        return errors

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Poll(models.Model):
    question_text = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name="Polls", on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="polls")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PollManager()

class Answer(models.Model):
    answer_text = models.CharField(max_length=255)
    related_poll = models.ForeignKey(Poll, related_name="answers", on_delete= models.CASCADE)
    percentage = models.IntegerField(null=True, blank=True)
    chooser = models.ManyToManyField(User, related_name="chosen_answers")
    objects = UserManager()

# Create your models here.
