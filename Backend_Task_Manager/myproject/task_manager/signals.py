
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from task_manager.models import Task, Notification


@receiver(post_save, sender=Task)
def task_saved_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            user=instance.user,
            message=f'Created "{instance.title}"'
        )

    else:

        Notification.objects.create(
            user=instance.user,
            message=f'Updated "{instance.title}"'
        )


@receiver(post_delete, sender=Task)
def task_deleted_notification(sender, instance, **kwargs):

    Notification.objects.create(
        user=instance.user,
        message=f'Deleted "{instance.title}"'
    )