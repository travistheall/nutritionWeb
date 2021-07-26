from django.apps import AppConfig


class CustomprofileConfig(AppConfig):
    name = 'customProfile'

    def ready(self):
    	import customProfile.signals

