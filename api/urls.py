from django.urls import path
from . import views

urlpatterns = [
    path("api/get/", views.get_data),
    path("api/post/", views.post_request)
]