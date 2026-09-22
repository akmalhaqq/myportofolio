from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            order=1,
            title="Asisten Dosen PBP",
            company="Fasilkom UI",
            period="2026",
            description="Membantu mahasiswa memahami pengembangan web.",
            tags="Teaching, Mentoring",
        )

        self.project = Project.objects.create(
            order = 1,
            title="Score Prediction",
            category ="Data Science",
            description = "A data science project for predicting football match scores.",
            tech_stack = "Python, Pandas, Machince Learning",
            achievement="Ranked 39 of 236 participants",
            github_url="",
            external_url="",
            year=2026,
            image="img/gammafest.png",
        )

# Authentication Test
    def test_register_page_is_accessible(self):
        response = self.client.get(reverse("main:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_creates_user_with_hashed_password(self):
        response = self.client.post(reverse("main:register"), {
            "username": "new_user",
            "password1": "SafePassword123!",
            "password2": "SafePassword123!",
        })

        self.assertRedirects(response, reverse("main:login"))
        user = User.objects.get(username="new_user")
        self.assertTrue(user.check_password("SafePassword123!"))

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(reverse("main:register"), {
            "username": "invalid_user",
            "password1": "SafePassword123!",
            "password2": "DifferentPassword123!",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="invalid_user").exists())
        self.assertContains(response, "The two password fields didn’t match.")

    def test_login_logout_and_navbar_state(self):
        user = User.objects.create_user(
            username="visitor",
            password="SafePassword123!",
        )

        anonymous_response = self.client.get(reverse("main:show_main"))
        self.assertContains(anonymous_response, f'href="{reverse("main:login")}"')
        self.assertContains(anonymous_response, f'href="{reverse("main:register")}"')

        login_response = self.client.post(reverse("main:login"), {
            "username": "visitor",
            "password": "SafePassword123!",
        })
        self.assertRedirects(login_response, reverse("main:show_main"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

        authenticated_response = self.client.get(reverse("main:show_main"))
        self.assertContains(authenticated_response, "visitor")
        self.assertContains(authenticated_response, f'href="{reverse("main:logout")}"')

        logout_response = self.client.get(reverse("main:logout"))
        self.assertRedirects(logout_response, reverse("main:show_main"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_invalid_credentials(self):
        User.objects.create_user(
            username="visitor",
            password="SafePassword123!",
        )

        response = self.client.post(reverse("main:login"), {
            "username": "visitor",
            "password": "wrong-password",
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTrue(response.context["form"].non_field_errors())

# Experience Test
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.tag_list(), ["Teaching", "Mentoring"])

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.company)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Teaching")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_create_experience_success(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "New Experience",
            "company": "New Company",
            "period": "2024",
            "category": "Internship",
            "description": "New description",
            "tags": "Python, Django",
            "secret_code": "AkmalProjects2026"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Experience.objects.filter(title="New Experience").exists())

    def test_create_experience_wrong_secret(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "New Experience 2",
            "company": "New Company",
            "period": "2024",
            "category": "Internship",
            "description": "New description",
            "tags": "Python, Django",
            "secret_code": "wrongsecret"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Experience.objects.filter(title="New Experience 2").exists())

    def test_update_experience_success(self):
        response = self.client.post(reverse("main:update_experience", args=[self.experience.id]), {
            "title": "Updated Title",
            "company": self.experience.company,
            "period": self.experience.period,
            "category": self.experience.category,
            "description": self.experience.description,
            "tags": self.experience.tags,
            "secret_code": "AkmalProjects2026"
        })
        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Title")

    def test_update_experience_wrong_secret(self):
        response = self.client.post(reverse("main:update_experience", args=[self.experience.id]), {
            "title": "Updated Title 2",
            "company": self.experience.company,
            "period": self.experience.period,
            "category": self.experience.category,
            "description": self.experience.description,
            "tags": self.experience.tags,
            "secret_code": "wrongsecret"
        })
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertNotEqual(self.experience.title, "Updated Title 2")

    def test_delete_experience_success(self):
        response = self.client.post(reverse("main:delete_experience", args=[self.experience.id]), {
            "secret_code": "AkmalProjects2026"
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())

    def test_delete_experience_wrong_secret(self):
        response = self.client.post(reverse("main:delete_experience", args=[self.experience.id]), {
            "secret_code": "wrongsecret"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

# Projects Test

    def test_projects_url_is_accessible(self):
            response = self.client.get(
            reverse("main:show_projects")
        )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "projects.html")

    def test_project_is_displayed(self):
        response = self.client.get(
            reverse("main:show_projects")
        )

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.category)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Python")
        self.assertContains(response, "Pandas")
        self.assertContains(
            response,
            self.project.achievement
        )
    def test_empty_projects_page(self):
        Project.objects.all().delete()

        response = self.client.get(
            reverse("main:show_projects")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(
            response,
            "Belum ada project yang ditambahkan"
        )
