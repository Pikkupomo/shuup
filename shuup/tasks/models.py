# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from enumfields import Enum, EnumIntegerField
from six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from shuup.core.models import Contact, Shop
from shuup.utils.analog import define_log_model


class TaskType(Enum):
    GENERIC = 1
    QUESTION = 2
    FEEDBACK = 3
    REQUEST = 4


class TaskStatus(Enum):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    DELETED = 4

    class Labels:
        NEW = _("New")
        IN_PROGRESS = _("In progress")
        COMPLETED = _("Completed")


class TaskCommentVisibility(Enum):
    ALL = 1
    ADMINS_ONLY = 2
    HIDDEN = 3  # todo: think about this?

    class Labels:
        ALL = _("All")
        ADMINS_ONLY = _("Admins Only")


@python_2_unicode_compatible
class Task(models.Model):
    shop = models.ForeignKey(Shop)
    type = EnumIntegerField(TaskType, default=TaskType.GENERIC)
    status = EnumIntegerField(TaskStatus, default=TaskStatus.NEW)

    author = models.ForeignKey(Contact, blank=True, null=True)
    assigned_to = models.ForeignKey(Contact, blank=True, null=True)

    completed_by = models.ForeignKey(Contact, blank=True, null=True)
    completed_on = models.DateTimeField(verbose_name=_("completed on"), null=True)

    created_on = models.DateTimeField(auto_now_add=True, editable=False, db_index=True, verbose_name=_("created on"))
    modified_on = models.DateTimeField(auto_now=True, editable=False, db_index=True, verbose_name=_("modified on"))

    def assign(self, user):
        self.assigned_to = user
        self.status = TaskStatus.IN_PROGRESS
        self.save()

    def comment(self, contact, comment, visibility=TaskCommentVisibility.ALL):
        return TaskComment.objects.create(task=self, author=contact, body=comment, visibility=visibility)

    def complete(self, contact):
        self.completed_by = contact
        self.completed_on = now()
        self.status = TaskStatus.COMPLETED
        self.save()

    def get_comments_for_contact(self, contact):
        comments = self.comments.all()
        if not contact.user or (contact.user and not contact.user.is_superuser):
            comments = comments.exclude(visibility=TaskCommentVisibility.ADMINS_ONLY)
        return comments

    def get_completion_time(self):
        if self.completed_on:
            return self.created_on - self.completed_on


class TaskComment(models.Model):
    task = models.ForeignKey(Task, related_name="comments")
    author = models.ForeignKey(Contact, blank=True, null=True, related_name="task_comments")
    visibility = EnumIntegerField(TaskCommentVisibility, default=TaskCommentVisibility.ALL)

    body = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True, editable=False, db_index=True, verbose_name=_("created on"))
    modified_on = models.DateTimeField(auto_now=True, editable=False, db_index=True, verbose_name=_("modified on"))

    def reply(self, user, body):
        return TaskComment.objects.create(task=self.task, comment_author=user, body=body)

    def as_html(self):
        return mark_safe(force_text(self.body))

    def can_see(self, user):
        # Todo: add cache for shop managers
        if not user.is_superuser:
            return self.visibility == TaskCommentVisibility.ALL
        return True


class TaskQueueQuerySet(models.QuerySet):  # doccov: ignore
    def completed(self):
        return self.filter(task__status=TaskStatus.COMPLETED)

    def in_progress(self):
        return self.filter(task__status=TaskStatus.IN_PROGRESS)


class TaskQueue(models.Model):
    task = models.ForeignKey(Task)

    # priority = ()

    created_on = models.DateTimeField(auto_now_add=True, editable=False, db_index=True, verbose_name=_("created on"))
    modified_on = models.DateTimeField(auto_now=True, editable=False, db_index=True, verbose_name=_("modified on"))

    objects = TaskQueueQuerySet.as_manager()


# TaskLogEntry = define_log_model(Task)
