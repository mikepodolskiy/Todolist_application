import pytest

from core.models import User


class TestUserSingUp:
    @pytest.mark.django_db
    def test_user_singup(self, password, client):
        data = {
            "first_name": "name",
            "last_name": "surname",
            "email": "",
            "username": "username",
            "password": password,
            "password_repeat": password,
        }

        response = client.post(
            "/core/signup",
            data=data,
            content_type="application/json",
        )
        assert response.status_code == 201, f"{response.status_code} instead 201"

        user = User.objects.last()
        assert response.status_code == 201, f"{response.status_code} instead 201"
        assert user.first_name == data["first_name"], "Incorrect user's first name"
        assert user.last_name == data["last_name"], "Incorrect user's last name"
        assert user.email == data["email"], "Incorrect user's email"
        assert user.username == data["username"], "Incorrect user's username"
