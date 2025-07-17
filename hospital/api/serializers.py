# hospital/serializers.py
from rest_framework import serializers
from hospital.api.models import User, Slot, Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.username", read_only=True)
    doctor_name = serializers.CharField(source="slot.doctor.username", read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'slot', 'status', 'patient_name', 'doctor_name']
