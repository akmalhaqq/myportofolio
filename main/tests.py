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

    def test_last_login_cookie_lifecycle(self):
        User.objects.create_user(
            username="visitor",
            password="SafePassword123!",
        )

        login_response = self.client.post(reverse("main:login"), {
            "username": "visitor",
            "password": "SafePassword123!",
        })

        self.assertIn("last_login", login_response.cookies)
        self.assertTrue(login_response.cookies["last_login"].value)

        main_response = self.client.get(reverse("main:show_main"))
        self.assertContains(main_response, "Terakhir login:")
        self.assertContains(
            main_response,
            login_response.cookies["last_login"].value,
        )

        logout_response = self.client.get(reverse("main:logout"))
        self.assertEqual(logout_response.cookies["last_login"].value, "")
        self.assertEqual(logout_response.cookies["last_login"]["max-age"], 0)

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

    def test_experience_controls_are_only_visible_to_superuser(self):
        create_url = reverse("main:create_experience")
        update_url = reverse("main:update_experience", args=[self.experience.id])
        delete_url = reverse("main:delete_experience", args=[self.experience.id])

        anonymous_response = self.client.get(reverse("main:show_experience"))
        self.assertNotContains(anonymous_response, f'href="{create_url}"')
        self.assertNotContains(anonymous_response, f'href="{update_url}"')
        self.assertNotContains(anonymous_response, f'action="{delete_url}"')

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        regular_response = self.client.get(reverse("main:show_experience"))
        self.assertNotContains(regular_response, f'href="{create_url}"')
        self.assertNotContains(regular_response, f'href="{update_url}"')
        self.assertNotContains(regular_response, f'action="{delete_url}"')

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(reverse("main:show_experience"))
        self.assertContains(owner_response, f'href="{create_url}"')
        self.assertContains(owner_response, f'href="{update_url}"')
        self.assertContains(owner_response, f'action="{delete_url}"')

    def test_create_experience_requires_superuser(self):
        create_url = reverse("main:create_experience")

        anonymous_response = self.client.get(create_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("main:login")}?next={create_url}',
        )

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        self.assertEqual(self.client.get(create_url).status_code, 403)

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(create_url)
        self.assertEqual(owner_response.status_code, 200)
        self.assertTemplateUsed(owner_response, "experience_form.html")
        self.assertNotContains(owner_response, "Secret Code")

    def test_superuser_can_create_experience_without_secret_code(self):
        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)

        response = self.client.post(reverse("main:create_experience"), {
            "title": "New Experience",
            "company": "New Company",
            "period": "2024",
            "category": "Internship",
            "description": "New description",
            "tags": "Python, Django",
        })

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="New Experience").exists())

    def test_update_experience_requires_superuser(self):
        update_url = reverse("main:update_experience", args=[self.experience.id])

        anonymous_response = self.client.get(update_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("main:login")}?next={update_url}',
        )

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        self.assertEqual(self.client.get(update_url).status_code, 403)

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(update_url)
        self.assertEqual(owner_response.status_code, 200)
        self.assertTemplateUsed(owner_response, "experience_form.html")
        self.assertNotContains(owner_response, "Secret Code")

    def test_superuser_can_update_experience_without_secret_code(self):
        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)

        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Updated Title",
                "company": self.experience.company,
                "period": self.experience.period,
                "category": self.experience.category,
                "description": self.experience.description,
                "tags": self.experience.tags,
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Title")

    def test_delete_experience_requires_superuser(self):
        delete_url = reverse("main:delete_experience", args=[self.experience.id])

        anonymous_response = self.client.post(delete_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("main:login")}?next={delete_url}',
        )
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        self.assertEqual(self.client.post(delete_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.post(delete_url)
        self.assertRedirects(owner_response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())

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

    def test_project_controls_are_only_visible_to_superuser(self):
        create_url = reverse("main:create_project")
        delete_url = reverse("main:delete_project", args=[self.project.id])

        anonymous_response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(anonymous_response, f'href="{create_url}"')
        self.assertNotContains(anonymous_response, f'action="{delete_url}"')

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        regular_response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(regular_response, f'href="{create_url}"')
        self.assertNotContains(regular_response, f'action="{delete_url}"')

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(reverse("main:show_projects"))
        self.assertContains(owner_response, f'href="{create_url}"')
        self.assertContains(owner_response, f'action="{delete_url}"')

    def test_create_project_requires_superuser(self):
        create_url = reverse("main:create_project")

        anonymous_response = self.client.get(create_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("main:login")}?next={create_url}',
        )

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        self.assertEqual(self.client.get(create_url).status_code, 403)

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(create_url)
        self.assertEqual(owner_response.status_code, 200)
        self.assertTemplateUsed(owner_response, "projects_form.html")
        self.assertNotContains(owner_response, "Secret Code")

    def test_superuser_can_create_project_without_secret_code(self):
        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)

        response = self.client.post(reverse("main:create_project"), {
            "title": "Authorized Project",
            "category": "Web Development",
            "description": "Created by the portfolio owner.",
            "tech_stack": "Django, Python",
            "achievement": "",
            "github_url": "",
            "external_url": "",
            "image": "",
            "year": 2026,
        })

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Authorized Project").exists())

    def test_delete_project_requires_superuser(self):
        delete_url = reverse("main:delete_project", args=[self.project.id])

        anonymous_response = self.client.post(delete_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("main:login")}?next={delete_url}',
        )
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        self.assertEqual(self.client.post(delete_url).status_code, 403)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.post(delete_url)
        self.assertRedirects(owner_response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_project_star_relation_and_reverse_relation(self):
        user = User.objects.create_user(
            username="star_user",
            password="SafePassword123!",
        )

        self.project.starred_by.add(user)

        self.assertTrue(self.project.starred_by.filter(pk=user.pk).exists())
        self.assertTrue(user.starred_projects.filter(pk=self.project.pk).exists())

    def test_toggle_star_requires_login_and_only_changes_on_post(self):
        star_url = reverse("main:toggle_star", args=[self.project.id])

        anonymous_response = self.client.post(star_url)
        self.assertRedirects(
            anonymous_response,
            f'{reverse("main:login")}?next={star_url}',
        )
        self.assertEqual(self.project.starred_by.count(), 0)

        user = User.objects.create_user(
            username="star_user",
            password="SafePassword123!",
        )
        self.client.force_login(user)

        get_response = self.client.get(star_url)
        self.assertRedirects(get_response, reverse("main:show_projects"))
        self.assertEqual(self.project.starred_by.count(), 0)

        add_response = self.client.post(star_url)
        self.assertRedirects(add_response, reverse("main:show_projects"))
        self.assertTrue(self.project.starred_by.filter(pk=user.pk).exists())

        remove_response = self.client.post(star_url)
        self.assertRedirects(remove_response, reverse("main:show_projects"))
        self.assertFalse(self.project.starred_by.filter(pk=user.pk).exists())

    def test_project_star_component_and_api_use_username(self):
        user = User.objects.create_user(
            username="star_user",
            password="SafePassword123!",
        )
        self.project.starred_by.add(user)
        self.client.force_login(user)

        page_response = self.client.get(reverse("main:show_projects"))
        self.assertContains(page_response, "Unstar")
        self.assertContains(
            page_response,
            f'action="{reverse("main:toggle_star", args=[self.project.id])}"',
        )

        api_response = self.client.get(reverse("main:get_projects_json"))
        project_data = next(
            item
            for item in api_response.json()
            if item["pk"] == str(self.project.pk)
        )
        self.assertEqual(project_data["fields"]["starred_by"], [["star_user"]])
