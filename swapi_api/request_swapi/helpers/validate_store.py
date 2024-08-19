from rest_framework.exceptions import ValidationError

def validate_before_store(serializer, partial=False):
    # Get the value of population
    population = serializer.validated_data.get('population')

    # If population is "unknown", convert it to an empty string
    if population == "unknown":
        serializer.validated_data['population'] = ""

    # If population is None, convert it to an empty string
    elif population is None:
        serializer.validated_data['population'] = ""

    # If population is a number, validate that it is not negative
    elif isinstance(population, str):
        try:
            population_value = int(population)
            if population_value < 0:
                raise ValidationError("Population cannot be a negative number.")
        except (ValueError, TypeError):
            # If population is not a valid number, ignore the validation
            pass

    # Additional handling for null fields if this is not a partial update
    if not partial:
        # If terrains is null, set it to 'unknown'
        terrains = serializer.validated_data.get('terrains')
        if terrains is None:
            serializer.validated_data['terrains'] = "unknown"

        # If climates is null, set it to 'unknown'
        climates = serializer.validated_data.get('climates')
        if climates is None:
            serializer.validated_data['climates'] = "unknown"

    return serializer
