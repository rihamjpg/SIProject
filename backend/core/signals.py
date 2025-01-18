from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Contrat, Service

@receiver(post_save, sender=Contrat)
def update_service_effectif(sender, instance, created, **kwargs):
    if created:
        service = instance.employe.id_service
        service.effectif_actuel = service.employes.count()
        service.save()