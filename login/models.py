from django.db import models

# Create your models here.


class User(models.Model):

    GENDERS = [
        (0, '未知'),
        (1, '男性'),
        (2, '女性'),
    ]

    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    sex = models.IntegerField(choices=GENDERS, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-create_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Confirm(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=256)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.code

    class Meta:
        ordering = ['-created_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'