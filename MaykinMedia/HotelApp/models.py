from django.db import models

class City(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Hotel(models.Model):
    city = models.ForeignKey(to=City, max_length=3, on_delete=models.CASCADE)
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.city.name}, {self.id})"