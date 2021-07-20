from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    pass

class Caption(models.Model):
    pass