from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # User is optional
    name = models.CharField(max_length=100, blank=True, null=True)  # New field
    country = models.CharField(max_length=100, blank=True, null=True)  # New field
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user and self.user.first_name:  
            return f"{self.user.first_name}'s Feedback"
        elif self.name:
            return f"{self.name}'s Feedback"  # Display entered name if available
        elif self.user:
            return f"{self.user.username}'s Feedback"
        else:
            return "Anonymous Feedback"
