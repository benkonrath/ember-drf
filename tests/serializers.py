from rest_framework import serializers

from ember_drf.serializers import SideloadSerializer

from tests.models import ChildModel, ParentModel, OptionalChildModel, \
    OneToOne, ReverseOneToOne


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildModel

class OptionalChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionalChildModel

class OneToOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneToOne

class ReverseOneToOneSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'one_to_one')
        model = ReverseOneToOne

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentModel
        fields = ('id', 'text', 'children', 'old_children')

class NestedChildSerializer(ChildSerializer):
    parent = ParentSerializer()
    old_parent = ParentSerializer()

class NestedChildSideloadSerializer(SideloadSerializer):
    class Meta:
        base_serializer = NestedChildSerializer

class ChildSideloadSerializer(SideloadSerializer):
    class Meta:
        base_serializer = ChildSerializer
        sideloads = [(ParentModel, ParentSerializer, ParentModel.objects.prefetch_related('children', 'old_children'))]


class OptionalChildSideloadSerializer(SideloadSerializer):
    class Meta:
        base_serializer = OptionalChildSerializer
        sideloads = [(ParentModel, ParentSerializer)]

class OneToOneSideloadSerializer(SideloadSerializer):
    class Meta:
        base_serializer = OneToOneSerializer
        sideloads = [(ReverseOneToOne, ReverseOneToOneSerializer)]

class ReverseOneToOneSideloadSerializer(SideloadSerializer):
    class Meta:
        base_serializer = ReverseOneToOneSerializer
        sideloads = [(OneToOne, OneToOneSerializer)]
