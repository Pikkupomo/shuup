import pytest

from shuup.tasks.models import Task, TaskComment, TaskQueue, TaskStatus
from shuup.tasks.utils import create_task
from shuup.testing.factories import create_random_person, get_default_shop, create_random_user


@pytest.mark.django_db
def test_basic_tasks(admin_user):
    shop = get_default_shop()
    contact = create_random_person(shop=shop)
    # task gets created
    text = "derpy hooves"
    task = create_task(shop, contact, text)

    assert Task.objects.count() == 1
    assert TaskComment.objects.count() == 1
    assert TaskComment.objects.first().author == contact

    assert contact.task_comments.count() == 1

    assert not task.assigned_to
    assert task.status == TaskStatus.NEW

    # taskqueue
    assert TaskQueue.objects.count() == 1

    # someone handles it
    admin_contact = create_random_person()
    admin_contact.user = admin_user
    admin_contact.save()
    task.assign(admin_contact)

    task.refresh_from_db()

    assert task.assigned_to == admin_contact
    assert task.status == TaskStatus.IN_PROGRESS

    assert TaskQueue.objects.count() == 1

    comment_text = "this being handled now"
    task.comment(admin_contact, comment_text)

    task.refresh_from_db()

    assert task.comments.count() == 2
    assert task.comments.last().body == comment_text

    assert TaskComment.objects.count() == 2

    task.complete(admin_contact)

    task.refresh_from_db()

    assert task.completed_on
    assert task.completed_by == admin_contact

    assert TaskQueue.objects.completed().count() == 1


def test_comment_visibility():
    # admin sees ALL and Admin only
    # anonymous only those with "ALL"
    # nonsuperuser sees ALL only
    pass