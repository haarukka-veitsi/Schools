from rest_framework import serializers

from core.models import Employee, SchoolClass, Student, School


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class SchoolClassSerializer(serializers.ModelSerializer):
    director = EmployeeSerializer()

    class Meta:
        model = SchoolClass
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class_field = SchoolClassSerializer(source="classroom")

    class Meta:
        model = Student
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    director = EmployeeSerializer()

    class Meta:
        model = School
        fields = "__all__"

    def _get_or_create_director(self, director_data):
        director_id = director_data.get("id")
        fio = director_data.get("fio")
        birth_date = director_data.get("birth_date")

        if director_id:
            try:
                director = Employee.objects.get(id=director_id)
                if director.fio == fio and director.birth_date == birth_date:
                    return director
                else:
                    return Employee.objects.create(**director_data)
            except Employee.DoesNotExist:
                return Employee.objects.create(**director_data)

        director, _ = Employee.objects.get_or_create(
            fio=fio, birth_date=birth_date, defaults=director_data
        )
        return director

    def create(self, validated_data):
        director_data = validated_data.pop("director")
        director = self._get_or_create_director(director_data)

        return School.objects.create(director=director, **validated_data)

    def update(self, instance, validated_data):
        if "director" in validated_data:
            director_data = validated_data.pop("director")
            instance.director = self._get_or_create_director(director_data)

        return super().update(instance, validated_data)
