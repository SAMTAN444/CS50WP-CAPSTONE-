
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Ippt", views.Ippt, name="Ippt"),
    path("bookings", views.bookings, name="bookings"),
    path("BMI", views.BMI, name="BMI"),
    path("create", views.create, name="create"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("sumbitedit/<int:id>", views.submitedit, name="submitedit"),
    path("delete/<int:id>", views.delete, name="delete"),
]
