from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # def get_all_users(self):
    #     return User.objects.all()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "users"
        verbose_name_plural = "users"
        db_table = "users"


