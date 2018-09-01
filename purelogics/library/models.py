from django.db import models


class Rack(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_year = models.DateField()

    def __str__(self):
        return self.title + ' - ' + self.author
