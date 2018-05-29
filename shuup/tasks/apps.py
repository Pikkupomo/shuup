# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "shuup.tasks"
    label = "shuup_tasks"
    provides = {
        # "admin_module": [
        #     "shuup.gdpr.admin_module.GDPRModule"
        # ],
        # "front_urls": [
        #     "shuup.gdpr.urls:urlpatterns"
        # ],
        # "customer_dashboard_items": [
        #     "shuup.gdpr.dashboard_items:GDPRDashboardItem"
        # ],
        # "admin_contact_toolbar_action_item": [
        #     "shuup.gdpr.admin_module.toolbar:AnonymizeContactToolbarButton",
        #     "shuup.gdpr.admin_module.toolbar:DownloadDataToolbarButton",
        # ],
        # "xtheme_resource_injection": [
        #     "shuup.gdpr.resources:add_gdpr_consent_resources"
        # ]
    }

    def ready(self):
        from django.db.models.signals import post_save
        from shuup.tasks.models import Task
        from shuup.tasks.signal_handlers import ensure_queue_entry
        post_save.connect(
            ensure_queue_entry,
            sender=Task,
            dispatch_uid="shuup_tasks:ensure_task_queue_entry"
        )
