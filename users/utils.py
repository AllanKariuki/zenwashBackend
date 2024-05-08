from math import radians, sin, cos, sqrt, atan2
from vendors.models import VendorService


def get_nearby_services(core_services, user_lat, user_long):
    services = []
    vendor_services = VendorService.objects.filter(service=core_services)
    for vendor_service in vendor_services:
        vendor = vendor_service.vendor
        distance = get_distance(user_lat, user_long, vendor.user.location_lat, vendor.user.location_lon)
        print(distance)
        if distance <= 7:
            services.append(vendor_service)
    return services


def get_distance(lat1, long1, lat2, long2):
    R = 6371
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(float(lat2))
    long2 = radians(float(long2))
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlong / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
