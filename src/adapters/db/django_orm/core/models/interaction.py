from django.db import models


class Interaction(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="interactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    settings = models.JSONField(default=dict)
