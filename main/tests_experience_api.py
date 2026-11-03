import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="test-password",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.get(name="Editor"))
        self.visitor = User.objects.create_user(
            username="visitor", email="private@example.com", password="test-password",
        )
        self.experience = Experience.objects.create(
            order=1, title="Teaching Assistant", company="Fasilkom UI",
            period="2026", category="Teaching", description="Teaching Django",
            tags="Django, Teaching",
        )
        self.payload = {
            "title": "Research Intern", "company": "Research Lab",
            "period": "2026", "category": "Internship",
            "description": "Researching data", "tags": "Python, Data",
        }
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.pk])
        self.star_url = reverse("api:experience-star", args=[self.experience.pk])

    def test_public_list_and_detail_keep_private_account_data_out(self):
        self.experience.starred_by.add(self.visitor)
        for url in (self.list_url, self.detail_url):
            response = self.client.get(url, HTTP_ACCEPT="application/json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.data[0] if url == self.list_url else response.data
            self.assertEqual(data["id"], str(self.experience.pk))
            self.assertEqual(data["title"], "Teaching Assistant")
            self.assertEqual(data["star_count"], 1)
            self.assertFalse(data["is_starred"])
            self.assertNotIn("starred_by", data)
            self.assertNotIn("starred_by_names", data)
            self.assertNotIn("email", data)
        self.client.force_authenticate(user=self.visitor)
        self.assertTrue(self.client.get(self.detail_url).data["is_starred"])

    def test_filter_search_sort_and_empty_results_match_existing_page(self):
        Experience.objects.create(
            order=2, title="Community Lead", company="Campus Club",
            period="2025", category="Community", description="Leading events",
            tags="Leadership",
        )
        response = self.client.get(self.list_url, {"search": "fasilkom"})
        self.assertEqual([item["title"] for item in response.data], ["Teaching Assistant"])
        response = self.client.get(self.list_url, {"category": "Community"})
        self.assertEqual([item["title"] for item in response.data], ["Community Lead"])
        response = self.client.get(self.list_url, {"sort": "z-a"})
        self.assertEqual(
            [item["title"] for item in response.data],
            ["Teaching Assistant", "Community Lead"],
        )
        self.experience.starred_by.add(self.visitor)
        response = self.client.get(self.list_url, {"sort": "most-starred"})
        self.assertEqual(response.data[0]["title"], "Teaching Assistant")
        response = self.client.get(self.list_url, {"search": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_experience_returns_404(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_regular_user_cannot_manage_experiences(self):
        for user in (None, self.visitor):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                self.assertEqual(
                    self.client.post(self.list_url, self.payload, format="json").status_code,
                    status.HTTP_403_FORBIDDEN,
                )
                self.assertEqual(
                    self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code,
                    status.HTTP_403_FORBIDDEN,
                )
                self.assertEqual(
                    self.client.delete(self.detail_url).status_code,
                    status.HTTP_403_FORBIDDEN,
                )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url, {"title": "Edited by Editor"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Edited by Editor")
        response = self.client.put(
            self.detail_url, {**self.payload, "title": "Replaced by Editor"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Replaced by Editor")
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.delete(self.detail_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Replaced by Editor")
        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_create_put_and_delete_with_existing_ordering(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url,
            {**self.payload, "order": 999, "star_count": 99, "is_starred": True,
             "starred_by": [self.visitor.pk]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["order"], 2)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(
            Experience.objects.get(pk=response.data["id"]).starred_by.count(), 0,
        )
        new_url = reverse("api:experience-detail", args=[response.data["id"]])
        response = self.client.put(new_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(
            new_url, {**self.payload, "title": "Updated", "order": 999}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated")
        self.assertEqual(Experience.objects.get(pk=response.data["id"]).order, 2)
        response = self.client.delete(new_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertEqual(Experience.objects.count(), 1)

    def test_validation_rejects_html_only_and_invalid_category(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in (
            ({"title": "<b></b>"}, "title"),
            ({"company": "<img src=x>"}, "company"),
            ({"period": "<b></b>"}, "period"),
            ({"description": "<b></b>"}, "description"),
            ({"tags": "<b></b>"}, "tags"),
            ({"category": "Invalid"}, "category"),
        ):
            with self.subTest(changes=changes):
                response = self.client.post(
                    self.list_url, {**self.payload, **changes}, format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        cleaned = {
            field: f"<b>{value}</b>"
            for field, value in self.payload.items() if field != "category"
        }
        response = self.client.post(self.list_url, {
            **self.payload, **cleaned,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for field in cleaned:
            self.assertEqual(response.data[field], self.payload[field])

    def test_star_requires_login_and_uses_current_account(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url, {"user_id": self.owner.pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertNotIn("starred_by_names", response.data)
        self.assertTrue(self.experience.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertFalse(self.experience.starred_by.filter(pk=self.owner.pk).exists())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_wrong_methods_are_rejected(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_requires_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        self.assertEqual(
            client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        page = client.get(reverse("main:show_experience"))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
