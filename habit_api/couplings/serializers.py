from rest_framework import serializers
from .models import Coupling

class CouplingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Coupling
        fields = ['id', 'owner', 'habit1', 'habit2', 'created_at']