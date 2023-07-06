from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from main.permissions import IsDoctor, IsPatientOrReadOnly

from .models import Doctor, Hospital, HospitalSection
from .serializers import (
    ConsultationSerializer,
    DoctorDetailsSerializer,
    DoctorSerializer,
    HospitalSectionSerializer,
    HospitalSerializer,
    ReservationsSerializer,
    UserRegisterSerializer,
)

# Create your views here.


class HospitalSectionListAPIView(ListAPIView):
    serializer_class = HospitalSectionSerializer
    queryset = HospitalSection.objects.all()#هتطلعلي كل الاقسام اللي موجودة عندي
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("hospital__id",)


class DoctorListAPIView(ListAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("section__id", "section__hospital__id")


class HospitalListAPIView(ListAPIView):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("type",)


class UserRegisterView(CreateAPIView):
    permission_classes = ()
    serializer_class = UserRegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.validated_data["role"] = (
            "doctor" if hasattr(serializer.user, "doctor_profile") else "patient"
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class DoctorDetailsView(RetrieveUpdateAPIView):
    serializer_class = DoctorDetailsSerializer
    permission_classes = (IsAuthenticated, IsDoctor)

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


class MyReservationsView(ListCreateAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = (IsAuthenticated, IsPatientOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return user.doctor_profile.reservations.all()
        elif hasattr(user, "patient"):
            return user.patient.reservations.all()
        return []

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient)


class MyConsultationsView(ListCreateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = (IsAuthenticated, IsPatientOrReadOnly)
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return user.doctor_profile.section.consultations.all()
        elif hasattr(user, "patient"):
            return user.patient.consultations.all()
        return []
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient)
    

class ReplyToConsultationView(RetrieveUpdateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = (IsAuthenticated, IsDoctor)
    http_method_names = ["patch", "get"]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return user.doctor_profile.section.consultations.all()
        return []

    def perform_update(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)     