from django.urls import path
from .views import (
    DoctorDetailsView,
    DoctorListAPIView,
    HospitalListAPIView,
    HospitalSectionListAPIView,
    LoginView,
    MyConsultationsView,
    MyReservationsView,
    ReplyToConsultationView,
    UserRegisterView,
)
urlpatterns = [
    path("hospitals/", HospitalListAPIView.as_view()),
    path("sections/", HospitalSectionListAPIView.as_view()),
    path("doctors/", DoctorListAPIView.as_view()),
    path("register/", UserRegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("doctor-details/", DoctorDetailsView.as_view()),
    path("my-reservations/", MyReservationsView.as_view()),
    path("my-consulations/", MyConsultationsView.as_view()),
    path("my-consulations/<int:pk>/", ReplyToConsultationView.as_view()),
]
