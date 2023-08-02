from json import dumps

from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

APPLICATION_JSON = 'application/json'
faker = Faker()


class UsersTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.user = baker.make(
            'users.User',
            name=faker.name(),
            email=faker.email(),
        )
        self.other_user = baker.make(
            'users.User',
            name=faker.name(),
            email=faker.email(),
        )

        self.COUNT_OF_USER_POSTS = 3
        self.user_posts = [baker.make(
            'Post',
            title=faker.sentence(nb_words=10, variable_nb_words=False),
            body=faker.paragraph(nb_sentences=2, variable_nb_sentences=False),
            user=self.user
        ) for x in range(self.COUNT_OF_USER_POSTS)]

        self.COUNT_OF_OTHER_USER_POSTS = 4
        self.other_user_posts = [baker.make(
            'Post',
            title=faker.sentence(nb_words=10, variable_nb_words=False),
            body=faker.paragraph(nb_sentences=2, variable_nb_sentences=False),
            user=self.other_user
        ) for x in range(self.COUNT_OF_OTHER_USER_POSTS)]

        self.client.force_authenticate(self.user)

    def test_try_authorized_user(self):
        self.client.force_authenticate(None)

        rsp = self.client.post(
            reverse('token'),
            dumps({
                'name': self.user.name,
                'email': self.user.email,
            }),
            content_type=APPLICATION_JSON)

        data = rsp.data
        self.assertEqual(rsp.status_code, status.HTTP_200_OK, data)
        self.assertTrue("token" in data)
        self.assertIsNotNone(data["token"])

    def test_incorrect_authorization(self):
        self.client.force_authenticate(None)

        incorrect_data = {
            "123": "testmail.com",
            "undefined": "undefined@mail.com",
            "testmail.com": 123
        }
        for name, email in incorrect_data.items():
            rsp = self.client.post(
                reverse('token'),
                dumps({
                    'name': name,
                    'email': email,
                }),
                content_type=APPLICATION_JSON)

            self.assertEqual(rsp.status_code, status.HTTP_400_BAD_REQUEST, rsp.data)

    def test_get_user(self):
        rsp = self.client.get(
            reverse('apis:users-detail', args=[self.user.id])
        )
        self.assertEqual(rsp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, rsp.data)

    def test_get_list_users_as_html(self):
        rsp = self.client.get(reverse('apis:users-list'))
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertTrue("text/html" in rsp.headers.get("Content-Type"))

    def test_get_list_users_as_json(self):
        rsp = self.client.get(
            reverse('apis:users-list'),
            headers={"Accept": "application/json"}
        )
        self.assertEqual(rsp.status_code, status.HTTP_200_OK, rsp.data)
        self.assertEqual(len(rsp.data["results"]), User.objects.all().count())

    def test_get_user_posts_as_html(self):
        rsp = self.client.get(
            reverse('apis:users-user-posts', args=[self.user.id])
        )
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)

        rsp = self.client.get(
            reverse('apis:users-user-posts', args=[self.other_user.id])
        )
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)

    def test_get_user_posts_as_json(self):
        rsp = self.client.get(
            reverse('apis:users-user-posts', args=[self.user.id]),
            headers={"Accept": "application/json"}
        )
        self.assertEqual(rsp.status_code, status.HTTP_200_OK, rsp.data)
        self.assertEqual(len(rsp.data), self.COUNT_OF_USER_POSTS)

        rsp = self.client.get(
            reverse('apis:users-user-posts', args=[self.other_user.id]),
            headers={"Accept": "application/json"}
        )
        self.assertEqual(rsp.status_code, status.HTTP_200_OK, rsp.data)
        self.assertEqual(len(rsp.data), self.COUNT_OF_OTHER_USER_POSTS)
