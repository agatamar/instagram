from django.contrib.auth.models import User
from django.db import models

# Create your models here.
INSTAGRAM_MAXIMUM_COMMENT_LENGTH=100

class Photo(models.Model):
    title = models.CharField(max_length=50)
    path=models.CharField(max_length=200)
    creation_date=models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo,on_delete=models.CASCADE)
    # value, is an IntegerField, which will hold the value of the like. 1= like. 2=dislike.
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.photo) + ':' + str(self.value)

    class Meta:
        unique_together = ("user", "photo", "value")


class Comment(models.Model):
    text = models.CharField(max_length=INSTAGRAM_MAXIMUM_COMMENT_LENGTH)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo=models.ForeignKey(Photo,on_delete=models.CASCADE)

    def __str__(self):
        return self.text


