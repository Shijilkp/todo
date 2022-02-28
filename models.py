from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    due = models.DateField()

    def __str__(self):
        return self.title

    class Meta():
        ordering = ['complete']
