from django.contrib.auth.models import AbstractUser
from django.db import models


class CreateUserModel(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)


class Event(models.Model):
    autor_id = models.OneToOneRel(CreateUserModel, on_delete=models.CASCADE)  # User table
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    start_at = models.DateField()
    end_at = models.DateField()
    description = models.TextField()
    status_id = models.OneToOneRel(Status, on_delete=models.CASCADE)  # Status table
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Event: {self.name} (start at: {self.start_at}, end at: {self.end_at})'


class Comment(models.Model):
    author_id = models.OneToOneField(CreateUserModel, on_delete=models.CASCADE)
    event_id = models.OneToOneField(Event, on_delete=models.CASCADE)
    contnent = models.TextField()
    event_date = models.DateTimeField(auto_now_add=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''
        Author{self.author_id}      Event {self.event_id}
        '''


class Subscriptoion(models.Model):
    user_id = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''
        user_id{self.user_id}      Event {self.event_id}
        '''


class Status(models.Model):
    STATUS_CHOICE = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status_id = models.OneToOneField(Event, on_delete=models.CASCADE)
    name = models.CharField(choices=STATUS_CHOICE, max_length=50, default=STATUS_CHOICE[1][0])
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''
        status_id{self.status_id}      Status: {self.name}
        '''


# Artem


class Category(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Category: {self.category_name}'


class Event_category(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Event_id: {self.event_id}, category_id: {self.category_id}'
