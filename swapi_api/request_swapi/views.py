from django.shortcuts import render
from rest_framework import views, response, status
import requests
import logging

from request_swapi.models import Planet
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .serializers import PlanetSerializer

from request_swapi.helpers.validate_store import validate_before_store


# Query data of swapi GraphQL and store on Planet model
class StoreData(views.APIView):
    def post(self, request, *args, **kwargs):

        # Define the GraphQL query
        query = """
        query Query {
        allPlanets {
            planets {
            name
            population
            terrains
            climates
            }
        }
        }
        """

        # Define the URL del endpoint
        url = "https://swapi-graphql.netlify.app/.netlify/functions/index"

        # Hacer la solicitud a la API GraphQL
        response_ = requests.post(url, json={'query': query})

        # Verificar si la solicitud fue exitosa
        if response_.status_code == 200:
            data = response_.json()
            logging.info(f"len of data: {len(data)}")

            planets = data['data']['allPlanets']['planets']
            
            for planet_data in planets:
                # Use update_or_create in order to avoid duplicates
                Planet.objects.update_or_create(
                    name=planet_data['name'],
                    defaults={
                        'population': planet_data.get('population', 'unknown'),
                        'terrains': ', '.join(planet_data['terrains']),
                        'climates': ', '.join(planet_data['climates']),
                    }
                )
            return response.Response({"data": f"{data}"}, status=status.HTTP_200_OK)
        else:
            return response.Response({"Query failed": f"{response_.json()}"}, status=response.status_code)

# Create a new instance of Planet
class PlanetCreateView(generics.CreateAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def perform_create(self, serializer):
        planet_name = serializer.validated_data.get('name')
        
        # Verify if the Planet already exists
        if Planet.objects.filter(name=planet_name).exists():
            raise ValidationError(f"Planet with name '{planet_name}' already exists.")
        
        serializer = validate_before_store(serializer)
        
        # If not exists then store the Planet
        serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Read a Planet instance
class PlanetDetailView(generics.RetrieveAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def get(self, request, *args, **kwargs):
        planet = self.get_object()
        serializer = self.get_serializer(planet)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

# Update Planet instance
class PlanetUpdateView(generics.UpdateAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def perform_update(self, serializer, partial=False):
        # Validate before storing, pass the partial flag
        validate_before_store(serializer, partial=partial)
        # Store model
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Pass the partial flag to perform_update
        self.perform_update(serializer, partial=partial)
        return response.Response(serializer.data)


# Delete a Planet instance
class PlanetDeleteView(generics.DestroyAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    
# List all the instances of Planet
class PlanetListView(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
