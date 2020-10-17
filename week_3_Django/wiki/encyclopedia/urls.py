from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.page, name="page"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("new/", views.new, name="new")
]
