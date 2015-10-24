from apps.task.models import SavedSignals
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

exclude_models_name = ['SavedSignals', 'ContentType',
                       'LogEntry', 'MigrationHistory']


@receiver(post_save)
def post_save_signal(sender, created, **kwargs):
    if created and sender.__name__ not in exclude_models_name:
        SavedSignals.objects.create(title=sender.__name__, status='Create')
    elif not created and sender.__name__ not in exclude_models_name:
        SavedSignals.objects.create(title=sender.__name__, status='Update')


@receiver(post_delete)
def post_delete_signal(sender, **kwargs):
    if sender.__name__ not in exclude_models_name:
        SavedSignals.objects.create(title=sender.__name__, status='Delete')
