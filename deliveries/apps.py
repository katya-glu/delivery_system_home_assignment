from django.apps import AppConfig

class DeliveriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deliveries'
    def ready(self):
        #from .upload_timeslots_on_startup import load_courier_timeslots
        #load_courier_timeslots('deliveries/courier_timeslots.json')
        pass
