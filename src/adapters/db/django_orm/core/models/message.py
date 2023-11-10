from django.db import models


class RoleType(models.TextChoices):
    HUMAN = "human", "HUMAN"
    AI = "ai", "AI"


class Message(models.Model):
    interaction = models.ForeignKey(
        "Interaction", on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=RoleType.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
