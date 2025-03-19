from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s score: {self.score}"
