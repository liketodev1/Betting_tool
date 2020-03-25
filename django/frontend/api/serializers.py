from rest_framework import serializers
from frontend.models import Scores

class FrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = ('title', 'content')
