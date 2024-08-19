from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=100)
    population = models.CharField(max_length=100, null=True, blank=True)
    terrains = models.CharField(max_length=255)
    climates = models.CharField(max_length=255)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'population', 'terrains', 'climates'], name='unique_planets_values')
        ]

    def __str__(self):
        return self.name