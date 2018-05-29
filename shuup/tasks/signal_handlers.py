from shuup.tasks.models import TaskQueue


def ensure_queue_entry(sender, instance, **kwargs):
    TaskQueue.objects.get_or_create(task=instance)
