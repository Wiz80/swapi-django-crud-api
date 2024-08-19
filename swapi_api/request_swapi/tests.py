import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from request_swapi.models import Planet
import numpy as np

@pytest.mark.django_db
class TestPlanetCRUD:
    def setup_method(self):
        self.client = APIClient()

    def test_create_planet(self):
        # Create a Planet
        url = reverse('planet-create')
        data = {
            "name": "Tatooine",
            "population": "200000",
            "terrains": "desert",
            "climates": "arid"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert Planet.objects.filter(name="Tatooine").exists()

    def test_create_planet_with_null_population(self):
        url = reverse('planet-create')
        data = {
            "name": "Hoth",
            "population": None,
            "terrains": "ice caves, mountains",
            "climates": "frozen"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        planet = Planet.objects.get(name="Hoth")
        assert planet.population == ""
    
    def test_create_planet_with_negative_population(self):
        url = reverse('planet-create')
        data = {
            "name": "Alderaan",
            "population": "-500000",  # Población negativa
            "terrains": "grasslands, mountains",
            "climates": "temperate"
        }
        
        # We wait for validationError
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == 400
        assert 'Population cannot be a negative number.' in str(response.data)

    def test_list_planets(self):
        # List Planet: create some planets to list
        Planet.objects.create(name="Naboo", population="450000", terrains="grassy hills, swamps, forests", climates="temperate")
        Planet.objects.create(name="Kamino", population="1000000000", terrains="ocean", climates="rainy")

        url = reverse('planet-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_retrieve_planet(self):
        planet = Planet.objects.create(name="Mustafar", population="20000", terrains="volcanic", climates="hot")
        url = reverse('planet-detail', kwargs={'pk': planet.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == "Mustafar"

    def test_update_planet(self):
        planet = Planet.objects.create(name="Dagobah", population="unknown", terrains="swamp", climates="murky")
        url = reverse('planet-update', kwargs={'pk': planet.id})
        data = {
            "name": "Dagobah",
            "population": "unknown",
            "terrains": "swamp, jungle",
            "climates": "humid"
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == 200
        planet.refresh_from_db()
        assert planet.population == ""
        assert planet.terrains == "swamp, jungle"
        assert planet.climates == "humid"

    def test_delete_planet(self):
        planet = Planet.objects.create(name="Yavin IV", population="1000", terrains="jungle, rainforests", climates="temperate")
        url = reverse('planet-delete', kwargs={'pk': planet.id})
        response = self.client.delete(url)
        assert response.status_code == 204
        assert not Planet.objects.filter(name="Yavin IV").exists()
