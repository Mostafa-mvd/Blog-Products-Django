from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MyOrdersViewTestCase(TestCase):

    def setUp(self) -> None:
        """initial test environment"""
        pass

    def test_auth_required(self):
        response = self.client.get(reverse("store:show_finalized_order"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        response = self.client.get(reverse("store:show_finalized_order"), follow=True)
        self.assertContains(response, "Please login")

    def test_empty_order_history_for_user(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)

        response = self.client.get(reverse("store:show_finalized_order"))
        self.assertContains(response, "DataTime")
        self.assertEqual(response.context_data['paginator'].count, 0)
