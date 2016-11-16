from django.db import models

import intake


class Applicant(models.Model):

    def log_event(self, name, data=None):
        data = data or {}
        return intake.models.ApplicationEvent.create(
            name=name,
            applicant_id=self.id,
            **data
        )
