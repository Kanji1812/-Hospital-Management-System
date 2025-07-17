# hospital/models.py
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.conf import settings
# base model
class BaseModel(models.Model):
    # Automatically set these fields for all models inheriting from BaseModel
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_updated', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True  # Makes this class an abstract base class
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (("doctor", "Doctor"), ("patient", "Patient"))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    objects = CustomUserManager() 

class Slot(BaseModel):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    @staticmethod
    def available_slots(doctor):
        return Slot.objects.filter(doctor=doctor, is_booked=False)
    
class Appointment(BaseModel):
    STATUS_CHOICES = (("pending", "Pending"), ("completed", "Completed"), ("cancelled", "Cancelled"))

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments", limit_choices_to={'role': 'patient'})
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    def __str__(self):
        return f"Appointment for {self.patient.email} with {self.doctor.email} on {self.slot.date} from {self.slot.start_time} to {self.slot.end_time}"

    @property
    def doctor(self):
        return self.slot.doctor
