import pytest
from rest_framework.test import APIClient

from core.models import School, Employee
from core.serializers import SchoolSerializer


@pytest.mark.django_db
def test_create_school_with_new_director():
    data = {
        "title": "Test School",
        "year": 2020,
        "rating": 9,
        "director": {"fio": "Ivan Ivanov", "birth_date": 1990},
    }

    serializer = SchoolSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    school = serializer.save()

    assert School.objects.count() == 1
    assert Employee.objects.count() == 1
    assert school.director.fio == "Ivan Ivanov"
    assert school.director.birth_date == 1990


@pytest.mark.django_db
def test_create_school_with_existing_director_full_match():
    director = Employee.objects.create(fio="Maria Petrova", birth_date=1985)

    data = {
        "title": "School 2",
        "year": 2018,
        "rating": 8,
        "director": {
            "id": director.id,
            "fio": "Maria Petrova",
            "birth_date": 1985,
        },
    }

    serializer = SchoolSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    school = serializer.save()

    assert school.director.id == director.id
    assert Employee.objects.count() == 1


@pytest.mark.django_db
def test_create_school_with_existing_director_partial_mismatch():
    director = Employee.objects.create(fio="Alex Smirnov", birth_date=1970)

    data = {
        "title": "School 3",
        "year": 2019,
        "rating": 7,
        "director": {
            "id": director.id,
            "fio": "Alex Smirnov Jr",
            "birth_date": 1970,
        },
    }

    serializer = SchoolSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    school = serializer.save()

    assert school.director.id != director.id
    assert school.director.fio == "Alex Smirnov Jr"
    assert Employee.objects.count() == 2


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_school_list(api_client):
    director = Employee.objects.create(fio="Director 1", birth_date=1975)
    School.objects.create(
        title="School 1", year=2000, rating=8, director=director
    )
    School.objects.create(
        title="School 2", year=2010, rating=9, director=director
    )

    response = api_client.get("/api/schools/")
    assert response.status_code == 200
    assert "list" in response.json()
    assert len(response.json()["list"]) == 2


@pytest.mark.django_db
def test_get_school_detail(api_client):
    director = Employee.objects.create(fio="Director 2", birth_date=1980)
    school = School.objects.create(
        title="School Detail", year=2005, rating=7, director=director
    )

    response = api_client.get(f"/api/schools/{school.id}/")
    assert response.status_code == 200
    data = response.json()["school"]
    assert data["id"] == school.id
    assert data["title"] == "School Detail"
    assert data["director"]["fio"] == "Director 2"


@pytest.mark.django_db
def test_create_school(api_client):
    data = {
        "school": {
            "title": "New School",
            "year": 2021,
            "rating": 9,
            "director": {"fio": "New Director", "birth_date": 1990},
        }
    }

    response = api_client.post("/api/schools/", data, format="json")
    assert response.status_code == 200
    resp_data = response.json()["school"]
    assert resp_data["title"] == "New School"
    assert Employee.objects.filter(fio="New Director").exists()


@pytest.mark.django_db
def test_patch_school(api_client):
    director = Employee.objects.create(fio="Director Patch", birth_date=1970)
    school = School.objects.create(
        title="Patch School", year=2000, rating=5, director=director
    )

    new_director = {"fio": "Updated Director", "birth_date": 1985}
    response = api_client.patch(
        f"/api/schools/{school.id}/",
        {"school": {"title": "Updated School", "director": new_director}},
        format="json",
    )

    assert response.status_code == 200
    school.refresh_from_db()
    assert school.title == "Updated School"
    assert school.director.fio == "Updated Director"


@pytest.mark.django_db
def test_delete_school(api_client):
    director = Employee.objects.create(fio="Director Delete", birth_date=1965)
    school = School.objects.create(
        title="Delete School", year=1990, rating=6, director=director
    )

    response = api_client.delete(f"/api/schools/{school.id}/")
    assert response.status_code == 202
    assert not School.objects.filter(id=school.id).exists()
