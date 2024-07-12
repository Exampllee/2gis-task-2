import requests
from faker import Faker
import pytest

fake = Faker()


def get_token():
    url = 'https://regions-test.2gis.com/v1/auth/tokens'
    response = requests.post(url)
    cookie_set_token = response.headers['Set-Cookie']
    token = {
        "Cookie": cookie_set_token
    }
    return token


class TestAddFavourite:
    FAV_URL = 'https://regions-test.2gis.com/v1/favorites'

    @pytest.mark.parametrize(
        "title, lat, lon, color",
        [
            ("GUU", 22, 33, "green"),
            ("", 22, 33, "green"),
            ("G", 22, 33, "green"),
            (fake.password(length=999), 22, 33, "green"),
            (fake.password(length=1000), 22, 33, "green")
        ]
    )
    def test_add_favourite_title(self, title, lat, lon, color):

        if title.isspace():
            expected_status_code = 400  # Ожидаемый статус код, если title пустой
        elif 1 <= len(title) <= 999:
            expected_status_code = 200  # Ожидаемый статус код, если title в допустимом диапазоне
        else:
            expected_status_code = 400  # Ожидаемый статус код, если title выходит за пределы допустимого диапазона

        data = {
            "title": title,
            "lat": lat,
            "lon": lon,
            "color": color
        }

        response = requests.post(
            url=self.FAV_URL,
            data=data,
            headers=get_token()
        )
        print(response.json())
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "title, lat, lon, color",
        [
            ("GUU", 0.9999999999, 33, "green"),
            ("GUU", -90.1, 33, "green"),
            ("GUU", 90.1, 33, "green")
        ]
    )
    def test_add_favourite_lat(self, title, lat, lon, color):

        data = {
            "title": title,
            "lat": lat,
            "lon": lon,
            "color": color
        }

        response = requests.post(
            url=self.FAV_URL,
            data=data,
            headers=get_token()
        )
        print(response.json())
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "title, lat, lon, color",
        [
            ("GUU", 22, 3, "green"),
            ("GUU", 22, 180.1, "green"),
            ("GUU", 90.1, -180.1, "green")
        ]
    )
    def test_add_favourite_lon(self, title, lat, lon, color):
        data = {
            "title": title,
            "lat": lat,
            "lon": lon,
            "color": color
        }

        response = requests.post(
            url=self.FAV_URL,
            data=data,
            headers=get_token()
        )
        print(response.json())
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "title, lat, lon, color",
        [
            ("GUU", 22, 33, "blue"),
            ("GUU", 22, 33, "yellow"),
            ("GUU", 22, 33, "red"),
            ("GUU", 22, 33, "brown"),
            ("GUU", 22, 33, "321"),
        ]
    )
    def test_add_favourite_color(self, title, lat, lon, color):

        if color.isspace():
            expected_status_code = 400
        elif color not in ["green", "red", "yellow", "blue"]:
            expected_status_code = 400
        else:
            expected_status_code = 200

        data = {
            "title": title,
            "lat": lat,
            "lon": lon,
            "color": color
        }

        response = requests.post(
            url=self.FAV_URL,
            data=data,
            headers=get_token()
        )
        print(response.json())
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize(
        "title, lat, lon, color",
        [
            (None, 0.9999999999, 33, "green"),
            ("GUU", None, 33, "green"),
            ("GUU", 22, None, "green"),
            ("GUU", 22, 33, None)
        ]
    )
    def test_add_favourite_none(self, title, lat, lon, color):

        if title is None or lat is None or lon is None:
            expected_status_code = 400
        else:
            expected_status_code = 200

        data = {
            "title": title,
            "lat": lat,
            "lon": lon,
            "color": color
        }

        response = requests.post(
            url=self.FAV_URL,
            data=data,
            headers=get_token()
        )
        print(response.json())
        assert response.status_code == expected_status_code
