from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("weather-form/",views.save,name="weather-form"),
    path("weather-list/",views.weather_data, name="weather-list"),
    path("delete-weather/<int:record_id>/", views.delete_data, name="delete-weather"),
    path("signup/",views.signup_page,name="signup"),
    path("login/",views.login_page,name="login"),
    path("logout/",views.logout_page, name="logout")
    
]