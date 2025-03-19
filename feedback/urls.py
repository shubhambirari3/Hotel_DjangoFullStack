from django.urls import path
from .views import feedback_view, feedback_list  # Import both views

app_name = 'feedback'  # Namespace for the app

urlpatterns = [
    path('', feedback_view, name='feedback_view'),          # Feedback form page
    path('list/', feedback_list, name='feedback_list'),     # Feedback list page
]
