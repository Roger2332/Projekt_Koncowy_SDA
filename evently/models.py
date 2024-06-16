from django.db import models

# Create your models here.


# Artem

class Event(models.Model):
    autor_id = models.OneToOneRel(CreateUserModel, on_delete=models.CASCADE) # User table
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    start_at = models.DateField()
    end_at = models.DateField()
    description = models.TextField()
    status_id = models.OneToOneRel(Status, on_delete=models.CASCADE) # Status table
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Event: {self.name} (start at: {self.start_at}, end at: {self.end_at})'

class Event_category(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Event_id: {self.event_id}, category_id: {self.category_id}'


class Category(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Category: {self.category_name}'