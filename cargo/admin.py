from django.contrib import admin
from cargo import models

@admin.register(models.Drivers)
class DriversAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'employment_date', 'gender', 'photo')

@admin.register(models.Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance', 'travel_days', 'payment', 'created_at', 'updated_at')

@admin.register(models.Transportations)
class TransportationsAdmin(admin.ModelAdmin):
    list_display = ('departure_date', 'return_date', 'is_bonus')

@admin.register(models.DriversTransportations)
class DriversTransportationsAdmin(admin.ModelAdmin):
    list_display = ('driver', 'transportation', 'driving_hours')

@admin.register(models.Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'model', 'capacity')

@admin.register(models.TransportationDetails)
class TransportationDetailsAdmin(admin.ModelAdmin):
    list_display = ('transportation', 'description', 'document_number', 'insurance')