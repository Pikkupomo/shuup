from shuup.tasks.models import TaskType, Task, TaskComment


def create_task(shop, contact, text, type=TaskType.GENERIC):

    task = Task.objects.create(author=contact, type=type, shop=shop)
    TaskComment.objects.create(body=text, author=contact, task=task)
    return task
