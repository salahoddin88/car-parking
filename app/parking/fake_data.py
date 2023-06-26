import random
from parking.models import Parking


def generate_random_parking_data():
    for i in range(10):
        name = f"Parking {i+1}"
        address = "Orchid Baner, Pune"
        latitude = random.uniform(18.5488, 18.5545)
        longitude = random.uniform(73.7735, 73.7859)
        capacity = random.randint(50, 100)

        parking = {
            'name': name,
            'address': address,
            'latitude': str(latitude),
            'longitude': str(longitude),
            'capacity': capacity,
        }

        Parking.objects.create(**parking)
    return True

generate_random_parking_data()
