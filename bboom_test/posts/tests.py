from json import dumps

from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post

APPLICATION_JSON = 'application/json'
faker = Faker()


class PostsTestCase(APITestCase):
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

        self.COUNT_OF_USER_POSTS = 2
        self.user_posts = [baker.make(
            'Post',
            title=faker.sentence(nb_words=10, variable_nb_words=False),
            body=faker.paragraph(nb_sentences=2, variable_nb_sentences=False),
            user=self.user
        ) for x in range(self.COUNT_OF_USER_POSTS)]

        self.COUNT_OF_OTHER_USER_POSTS = 3
        self.other_user_posts = [baker.make(
            'Post',
            title=faker.sentence(nb_words=10, variable_nb_words=False),
            body=faker.paragraph(nb_sentences=2, variable_nb_sentences=False),
            user=self.other_user
        ) for x in range(self.COUNT_OF_OTHER_USER_POSTS)]

        self.client.force_authenticate(self.user)

    def test_create_post_by_user(self):
        new_post_title = faker.sentence(nb_words=10, variable_nb_words=False)
        new_post_body = faker.paragraph(nb_sentences=2, variable_nb_sentences=False)
        rsp = self.client.post(
            reverse('apis:posts-list'),
            dumps({
                'title': new_post_title,
                'body': new_post_body,
            }),
            content_type=APPLICATION_JSON
        )
        self.assertEqual(rsp.status_code, status.HTTP_201_CREATED, rsp.data)

        data = rsp.data
        self.assertEqual(data['user'], self.user.id, data)
        self.assertEqual(data['title'], new_post_title, data)
        self.assertEqual(data['body'], new_post_body, data)

    def test_delete_post_by_user(self):
        removable_post_id = self.user_posts[0].id
        rsp = self.client.delete(reverse('apis:posts-detail', args=[removable_post_id]))
        self.assertEqual(rsp.status_code, status.HTTP_204_NO_CONTENT, rsp.data)

        self.assertFalse(Post.objects.filter(id=removable_post_id).exists())

    def test_create_post_unauthorized_user(self):
        self.client.force_authenticate(None)
        rsp = self.client.post(reverse('apis:posts-list'))
        self.assertEqual(rsp.status_code, status.HTTP_401_UNAUTHORIZED, rsp.data)

    def test_delete_post_unauthorized_user(self):
        self.client.force_authenticate(None)
        for post_id in [self.user_posts[0].id, self.other_user_posts[0].id]:
            rsp = self.client.delete(reverse('apis:posts-detail', args=[post_id]))
            self.assertEqual(rsp.status_code, status.HTTP_401_UNAUTHORIZED, rsp.data)

    def test_delete_post_another_user(self):
        rsp = self.client.delete(reverse('apis:posts-detail', args=[self.other_user_posts[0].id]))
        self.assertEqual(rsp.status_code, status.HTTP_403_FORBIDDEN, rsp.data)

        self.client.force_authenticate(self.other_user)

        rsp = self.client.delete(reverse('apis:posts-detail', args=[self.user_posts[0].id]))
        self.assertEqual(rsp.status_code, status.HTTP_403_FORBIDDEN, rsp.data)
