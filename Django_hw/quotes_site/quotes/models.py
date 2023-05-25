from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False)
    born_date = models.CharField()
    born_location = models.CharField(max_length=300, null=False)
    description = models.CharField()

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"




