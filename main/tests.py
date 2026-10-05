from datetime import UTC, datetime
from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse

from main.forms import ExperienceForm
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
        main_response = self.client.get(reverse("main:show_main"))
        self.assertContains(main_response, "Sesi Terakhir Login")
        self.assertContains(
            main_response,
            "Belum ada sesi login / Cookie tidak ditemukan",
        )

        User.objects.create_user(
            username="visitor",
            password="SafePassword123!",
        )

        fixed_utc_time = datetime(2026, 7, 22, 16, 55, 15, tzinfo=UTC)
        with patch("main.views.timezone.now", return_value=fixed_utc_time):
            login_response = self.client.post(reverse("main:login"), {
                "username": "visitor",
                "password": "SafePassword123!",
            })

        self.assertIn("last_login", login_response.cookies)
        self.assertEqual(
            login_response.cookies["last_login"].value,
            "22 Juli 2026, 23:55:15 WIB",
        )

        main_response = self.client.get(reverse("main:show_main"))
        self.assertContains(main_response, "Sesi Terakhir Login")
        self.assertContains(
            main_response,
            login_response.cookies["last_login"].value,
        )

        logout_response = self.client.get(reverse("main:logout"))
        self.assertEqual(logout_response.cookies["last_login"].value, "")
        self.assertEqual(logout_response.cookies["last_login"]["max-age"], 0)

        main_response = self.client.get(reverse("main:show_main"))
        self.assertContains(
            main_response,
            "Belum ada sesi login / Cookie tidak ditemukan",
        )

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
        self.assertNotContains(response, self.experience.title)
        self.assertNotContains(response, self.experience.company)
        self.assertNotContains(response, self.experience.description)
        self.assertContains(response, 'id="experience-search-input"')
        self.assertContains(response, 'id="experience-loading"')
        self.assertContains(response, 'id="experience-error"')
        self.assertContains(response, 'id="experience-empty"')
        self.assertContains(response, 'id="experience-list"')
        self.assertEqual(
            self.client.get(reverse("main:get_experience_json")).json()[0]["fields"]["title"],
            self.experience.title,
        )
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_page_does_not_depend_on_json_view(self):
        with patch("main.views.get_experience_json", side_effect=AssertionError):
            response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.experience.title)

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("main:get_experience_json")).json(), [])

    def test_experience_form_strips_tags_from_text_fields(self):
        form = ExperienceForm({
            "category": "Teaching",
            "title": "<b>Teaching Assistant</b>",
            "company": "<i>Fasilkom UI</i>",
            "period": "<span>2026</span>",
            "description": "Helped <em>students</em>.",
            "tags": "<strong>Django</strong>, Teaching",
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Teaching Assistant")
        self.assertEqual(form.cleaned_data["company"], "Fasilkom UI")
        self.assertEqual(form.cleaned_data["period"], "2026")
        self.assertEqual(form.cleaned_data["description"], "Helped students.")
        self.assertEqual(form.cleaned_data["tags"], "Django, Teaching")

    def test_experience_form_rejects_html_only_text_fields(self):
        data = {
            "category": "Teaching",
            "title": "Teaching Assistant",
            "company": "Fasilkom UI",
            "period": "2026",
            "description": "Helping students.",
            "tags": "Django",
        }
        for field in ("title", "company", "period", "description", "tags"):
            with self.subTest(field=field):
                form = ExperienceForm({
                    **data,
                    field: '<img src="x" onerror="alert(1)">',
                })
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_experience_renderer_permissions_match_user_role(self):
        create_url = reverse("main:create_experience")

        anonymous_response = self.client.get(reverse("main:show_experience"))
        self.assertNotContains(anonymous_response, 'popovertarget="add-experience-modal"')
        self.assertNotContains(anonymous_response, 'id="experience-form"')
        self.assertContains(anonymous_response, 'const CAN_EDIT = "false"')
        self.assertContains(anonymous_response, 'const IS_SUPERUSER = "false"')

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        regular_response = self.client.get(reverse("main:show_experience"))
        self.assertNotContains(regular_response, 'popovertarget="add-experience-modal"')
        self.assertNotContains(regular_response, 'id="experience-form"')
        self.assertContains(regular_response, 'const CAN_EDIT = "false"')
        self.assertContains(regular_response, 'const IS_SUPERUSER = "false"')

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(reverse("main:show_experience"))
        self.assertContains(owner_response, 'popovertarget="add-experience-modal"')
        self.assertContains(owner_response, 'id="experience-form"')
        self.assertContains(owner_response, f'action="{create_url}"')
        self.assertContains(owner_response, 'const CAN_EDIT = "true"')
        self.assertContains(owner_response, 'const IS_SUPERUSER = "true"')

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
        page_response = self.client.get(reverse("main:show_projects"))
        self.assertContains(page_response, 'id="grid"')
        self.assertNotContains(page_response, self.project.title)

        api_response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(api_response.status_code, 200)
        project_data = next(
            item for item in api_response.json()
            if item["pk"] == str(self.project.pk)
        )
        fields = project_data["fields"]
        self.assertEqual(fields["title"], self.project.title)
        self.assertEqual(fields["category"], self.project.category)
        self.assertEqual(fields["description"], self.project.description)
        self.assertEqual(fields["tech_stack"], self.project.tech_stack)
        self.assertEqual(fields["achievement"], self.project.achievement)

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
        anonymous_response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(anonymous_response, 'popovertarget="add-project-modal"')
        self.assertNotContains(anonymous_response, 'id="project-form"')

        regular_user = User.objects.create_user(
            username="regular_user",
            password="SafePassword123!",
        )
        self.client.force_login(regular_user)
        regular_response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(regular_response, 'popovertarget="add-project-modal"')
        self.assertNotContains(regular_response, 'id="project-form"')

        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        owner_response = self.client.get(reverse("main:show_projects"))
        self.assertContains(owner_response, 'popovertarget="add-project-modal"')
        self.assertContains(owner_response, 'id="project-form"')

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

    def test_project_ajax_search_filters_by_title(self):
        response = self.client.get(
            reverse("main:get_projects_json"), {"title": "score"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["fields"]["title"] for item in response.json()],
            [self.project.title],
        )
        self.assertEqual(
            self.client.get(
                reverse("main:get_projects_json"), {"title": "unknown"}
            ).json(),
            [],
        )

    def test_create_project_ajax_requires_post_and_superuser(self):
        ajax_url = reverse("main:create_project_ajax")
        self.assertEqual(self.client.get(ajax_url).status_code, 405)
        self.assertEqual(self.client.post(ajax_url).status_code, 403)

        regular_user = User.objects.create_user(
            username="regular_user", password="SafePassword123!"
        )
        self.client.force_login(regular_user)
        self.assertEqual(self.client.post(ajax_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    def test_create_project_ajax_strips_html_from_project_fields(self):
        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "<b>New</b> Project",
            "category": "Web",
            "description": "Built with <em>Django</em>.",
            "tech_stack": "<i>Python</i>, Django",
            "year": 2026,
        })

        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(pk=response.json()["pk"])
        self.assertEqual(project.title, "New Project")
        self.assertEqual(project.description, "Built with Django.")
        self.assertEqual(project.tech_stack, "Python, Django")

    def test_create_project_ajax_rejects_html_only_title(self):
        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        self.client.force_login(superuser)
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": '<img src="x" onerror="alert(1)">',
            "category": "Web",
            "description": "Description",
            "tech_stack": "Django",
            "year": 2026,
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertEqual(Project.objects.count(), 1)

    def test_create_project_ajax_requires_csrf_token(self):
        superuser = User.objects.create_superuser(
            username="portfolio_owner",
            password="SafePassword123!",
            email="owner@example.com",
        )
        client = Client(enforce_csrf_checks=True)
        client.force_login(superuser)
        ajax_url = reverse("main:create_project_ajax")
        project_data = {
            "title": "CSRF Project",
            "category": "Web",
            "description": "Description",
            "tech_stack": "Django",
            "year": 2026,
        }

        self.assertEqual(client.post(ajax_url, project_data).status_code, 403)
        client.get(reverse("main:show_projects"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(
            client.post(ajax_url, project_data, HTTP_X_CSRFTOKEN=token).status_code,
            201,
        )
        self.assertTrue(Project.objects.filter(title="CSRF Project").exists())

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

        api_response = self.client.get(reverse("main:get_projects_json"))
        project_data = next(
            item
            for item in api_response.json()
            if item["pk"] == str(self.project.pk)
        )
        self.assertEqual(project_data["fields"]["star_count"], 1)
        self.assertTrue(project_data["fields"]["is_starred"])
        self.assertEqual(project_data["fields"]["starred_by_names"], "star_user")

        self.client.logout()
        anonymous_project = self.client.get(reverse("main:get_projects_json")).json()[0]
        self.assertFalse(anonymous_project["fields"]["is_starred"])


class TugasFourTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experience = Experience.objects.create(
            order=1,
            title="Teaching Assistant",
            company="Fasilkom UI",
            period="2026",
            category="Teaching",
            description="Helping students learn Django.",
            tags="Django, Teaching",
        )
        cls.project = Project.objects.create(
            title="Portfolio Project",
            category="Web",
            description="A portfolio project.",
            tech_stack="Django",
            year=2026,
        )
        cls.regular = User.objects.create_user(
            username="regular",
            email="private@example.test",
            password="SafePassword123!",
        )
        cls.editor = User.objects.create_user(
            username="editor",
            password="SafePassword123!",
        )
        cls.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.test",
            password="SafePassword123!",
        )
        cls.editor.groups.add(Group.objects.get(name="Editor"))

    def experience_data(self, title):
        return {
            "title": title,
            "company": "Fasilkom UI",
            "period": "2026",
            "category": "Teaching",
            "description": "Helping students learn Django.",
            "tags": "Django, Teaching",
        }

    def test_editor_group_grants_change_only(self):
        self.assertEqual(
            set(Group.objects.get(name="Editor").permissions.values_list(
                "codename", flat=True
            )),
            {"change_experience"},
        )
        self.assertTrue(self.editor.has_perm("main.change_experience"))
        self.assertFalse(self.editor.has_perm("main.add_experience"))
        self.assertFalse(self.editor.has_perm("main.delete_experience"))
        self.assertFalse(self.regular.has_perm("main.change_experience"))

    def test_public_pages_and_api_are_readable(self):
        for url in (
            reverse("main:show_main"),
            reverse("main:show_experience"),
            reverse("main:show_projects"),
            reverse("main:get_experience_json"),
            reverse("main:get_projects_json"),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_anonymous_management_actions_redirect_to_login(self):
        urls = (
            reverse("main:create_experience"),
            reverse("main:update_experience", args=[self.experience.pk]),
            reverse("main:delete_experience", args=[self.experience.pk]),
        )
        for url in urls:
            for method in ("get", "post"):
                with self.subTest(url=url, method=method):
                    if method == "get":
                        response = self.client.get(url)
                    else:
                        response = self.client.post(
                            url, self.experience_data("Unauthorized")
                        )
                    self.assertRedirects(
                        response, f'{reverse("main:login")}?next={url}'
                    )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")
        self.assertEqual(Experience.objects.count(), 1)

    def test_regular_user_gets_403_for_all_management_actions(self):
        self.client.force_login(self.regular)
        urls = (
            reverse("main:create_experience"),
            reverse("main:update_experience", args=[self.experience.pk]),
            reverse("main:delete_experience", args=[self.experience.pk]),
        )
        for url in urls:
            for method in ("get", "post"):
                with self.subTest(url=url, method=method):
                    if method == "get":
                        response = self.client.get(url)
                    else:
                        response = self.client.post(
                            url, self.experience_data("Unauthorized")
                        )
                    self.assertEqual(response.status_code, 403)
                    self.assertTemplateUsed(response, "403.html")
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_login(self.editor)
        create_url = reverse("main:create_experience")
        update_url = reverse("main:update_experience", args=[self.experience.pk])
        delete_url = reverse("main:delete_experience", args=[self.experience.pk])

        self.assertEqual(self.client.get(update_url).status_code, 200)
        self.assertRedirects(
            self.client.post(update_url, self.experience_data("Edited by Editor")),
            reverse("main:show_experience"),
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited by Editor")

        for url in (create_url, delete_url):
            for method in ("get", "post"):
                with self.subTest(url=url, method=method):
                    if method == "get":
                        response = self.client.get(url)
                    else:
                        response = self.client.post(
                            url, self.experience_data("Not Allowed")
                        )
                    self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_login(self.owner)
        create_url = reverse("main:create_experience")
        update_url = reverse("main:update_experience", args=[self.experience.pk])
        delete_url = reverse("main:delete_experience", args=[self.experience.pk])

        self.assertEqual(self.client.get(create_url).status_code, 200)
        self.assertEqual(self.client.get(update_url).status_code, 200)
        self.assertRedirects(
            self.client.post(create_url, self.experience_data("New Experience")),
            reverse("main:show_experience"),
        )
        self.assertTrue(Experience.objects.filter(title="New Experience").exists())
        self.assertRedirects(
            self.client.post(update_url, self.experience_data("Edited by Owner")),
            reverse("main:show_experience"),
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited by Owner")
        self.assertRedirects(self.client.get(delete_url), reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assertRedirects(
            self.client.post(delete_url), reverse("main:show_experience")
        )
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_create_experience_ajax_enforces_role_method_and_validation(self):
        url = reverse("main:create_experience_ajax")
        self.assertEqual(self.client.get(url).status_code, 405)
        for user in (None, self.regular, self.editor):
            with self.subTest(user=user.username if user else "anonymous"):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                response = self.client.post(url, self.experience_data("Denied"))
                self.assertEqual(response.status_code, 403)
                self.assertIn("message", response.json())
        self.assertEqual(Experience.objects.count(), 1)

        self.client.force_login(self.owner)
        invalid = self.client.post(
            url, self.experience_data('<img src="x" onerror="alert(1)">')
        )
        self.assertEqual(invalid.status_code, 400)
        self.assertIn("title", invalid.json()["errors"])
        self.assertEqual(Experience.objects.count(), 1)

        valid = self.client.post(url, self.experience_data("<b>New Experience</b>"))
        self.assertEqual(valid.status_code, 201)
        created = Experience.objects.get(pk=valid.json()["pk"])
        self.assertEqual(created.title, "New Experience")
        self.assertEqual(created.order, 2)
        self.assertEqual(Experience.objects.count(), 2)

    def test_create_experience_ajax_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        url = reverse("main:create_experience_ajax")
        data = self.experience_data("Created with CSRF")

        self.assertEqual(client.post(url, data).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        client.get(reverse("main:show_experience"))
        token = client.cookies["csrftoken"].value
        response = client.post(url, {**data, "csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(title="Created with CSRF").exists())

    def test_renderer_controls_match_each_role(self):
        for user, can_create, can_edit, can_delete in (
            (None, False, False, False),
            (self.regular, False, False, False),
            (self.editor, False, True, False),
            (self.owner, True, True, True),
        ):
            with self.subTest(user=user.username if user else "anonymous"):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                content = self.client.get(
                    reverse("main:show_experience")
                ).content.decode()
                self.assertEqual('id="experience-form"' in content, can_create)
                self.assertEqual(
                    'popovertarget="add-experience-modal"' in content,
                    can_create,
                )
                self.assertIn(
                    f'const CAN_EDIT = "{str(can_edit).lower()}"', content
                )
                self.assertIn(
                    f'const IS_SUPERUSER = "{str(can_delete).lower()}"', content
                )

    def test_editor_cannot_manage_projects_but_can_star_them(self):
        self.client.force_login(self.editor)
        create_url = reverse("main:create_project")
        delete_url = reverse("main:delete_project", args=[self.project.pk])
        for url in (create_url, delete_url):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)
                self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

        star_url = reverse("main:toggle_star", args=[self.project.pk])
        self.assertRedirects(
            self.client.post(star_url), reverse("main:show_projects")
        )
        self.assertTrue(self.project.starred_by.filter(pk=self.editor.pk).exists())

    def test_experience_star_requires_login_and_post(self):
        star_url = reverse("main:toggle_experience_star", args=[self.experience.pk])
        list_url = reverse("main:show_experience")

        self.assertRedirects(self.client.post(star_url), reverse("main:login"))
        anonymous_page = self.client.get(list_url)
        self.assertContains(anonymous_page, 'const IS_AUTHENTICATED = "false"')
        self.assertEqual(self.experience.starred_by.count(), 0)

        for count, user in enumerate((self.regular, self.editor, self.owner), 1):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.get(star_url).status_code, 405)
                self.assertRedirects(self.client.post(star_url), list_url)
                self.assertEqual(self.experience.starred_by.count(), count)
                self.assertEqual(user.starred_experiences.count(), 1)

        self.client.force_login(self.regular)
        starred_data = self.client.get(
            reverse("main:get_experience_json")
        ).json()[0]["fields"]
        self.assertTrue(starred_data["is_starred"])
        self.assertEqual(starred_data["star_count"], 3)
        self.assertRedirects(self.client.post(star_url), list_url)
        self.assertEqual(self.experience.starred_by.count(), 2)
        unstarred_data = self.client.get(
            reverse("main:get_experience_json")
        ).json()[0]["fields"]
        self.assertFalse(unstarred_data["is_starred"])
        self.assertEqual(unstarred_data["star_count"], 2)
        self.assertRedirects(self.client.post(star_url), list_url)
        self.assertEqual(self.experience.starred_by.count(), 3)
        self.assertEqual(
            self.experience.starred_by.filter(pk=self.regular.pk).count(), 1
        )

    def test_experience_mutations_require_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.regular)
        star_url = reverse("main:toggle_experience_star", args=[self.experience.pk])
        self.assertEqual(client.post(star_url).status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)

        client.get(reverse("main:show_experience"))
        token = client.cookies["csrftoken"].value
        response = client.post(star_url, {"csrfmiddlewaretoken": token})
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertEqual(self.experience.starred_by.count(), 1)

        client.force_login(self.owner)
        for url in (
            reverse("main:create_experience"),
            reverse("main:update_experience", args=[self.experience.pk]),
            reverse("main:delete_experience", args=[self.experience.pk]),
        ):
            with self.subTest(url=url):
                self.assertEqual(
                    client.post(url, self.experience_data("Without CSRF")).status_code,
                    403,
                )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")
        self.assertEqual(Experience.objects.count(), 1)

    def test_experience_json_is_public_and_exposes_star_state_without_usernames(self):
        self.experience.starred_by.add(self.regular)
        Experience.objects.create(
            order=2,
            title="Alpha Teaching",
            company="Fasilkom UI",
            period="2025",
            category="Teaching",
            description="Another teaching role.",
            tags="Teaching",
        )
        Experience.objects.create(
            order=3,
            title="Internship Role",
            company="Company",
            period="2024",
            category="Internship",
            description="An internship.",
            tags="Python",
        )
        api_url = reverse("main:get_experience_json")
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        item = next(
            item for item in response.json()
            if item["pk"] == str(self.experience.pk)
        )
        self.assertEqual(item["model"], "main.experience")
        self.assertEqual(item["fields"]["title"], self.experience.title)
        self.assertEqual(item["fields"]["star_count"], 1)
        self.assertFalse(item["fields"]["is_starred"])
        self.assertNotIn("starred_by", item["fields"])
        self.assertNotIn("regular", response.content.decode())
        self.assertNotIn("private@example.test", response.content.decode())
        self.assertNotIn("password", response.content.decode())

        self.client.force_login(self.regular)
        starred_item = next(
            item for item in self.client.get(api_url).json()
            if item["pk"] == str(self.experience.pk)
        )
        self.assertTrue(starred_item["fields"]["is_starred"])

        self.client.force_login(self.editor)
        editor_response = self.client.get(api_url)
        unstarred_item = next(
            item for item in editor_response.json()
            if item["pk"] == str(self.experience.pk)
        )
        self.assertFalse(unstarred_item["fields"]["is_starred"])
        self.assertNotIn("regular", editor_response.content.decode())

        self.client.logout()
        self.assertNotContains(
            self.client.get(reverse("main:show_experience")), "Dibintangi oleh"
        )

        filtered = self.client.get(
            api_url, {"category": "Teaching", "sort": "a-z"}
        ).json()
        self.assertEqual(
            [item["fields"]["title"] for item in filtered],
            ["Alpha Teaching", "Teaching Assistant"],
        )

    def test_experience_json_searches_title_and_company_with_filter_and_sort(self):
        mentor = Experience.objects.create(
            order=2,
            title="Lab Mentor",
            company="Fasilkom UI",
            period="2025",
            category="Teaching",
            description="Mentoring students.",
            tags="Teaching",
        )
        Experience.objects.create(
            order=3,
            title="Internship Role",
            company="Fasilkom UI",
            period="2024",
            category="Internship",
            description="An internship.",
            tags="Python",
        )
        mentor.starred_by.add(self.regular, self.editor)
        self.experience.starred_by.add(self.regular)
        api_url = reverse("main:get_experience_json")

        by_title = self.client.get(api_url, {"search": "mentor"}).json()
        self.assertEqual(
            [item["fields"]["title"] for item in by_title], ["Lab Mentor"]
        )

        by_company = self.client.get(api_url, {"search": "FASILKOM"}).json()
        self.assertEqual(
            [item["fields"]["title"] for item in by_company],
            ["Teaching Assistant", "Lab Mentor", "Internship Role"],
        )

        combined = self.client.get(api_url, {
            "search": "  fasilkom  ",
            "category": "Teaching",
            "sort": "most-starred",
        }).json()
        self.assertEqual(
            [item["fields"]["title"] for item in combined],
            ["Lab Mentor", "Teaching Assistant"],
        )
        self.assertEqual(self.client.get(api_url, {"search": "unknown"}).json(), [])

    def test_experience_most_starred_sort_preserves_filter_and_tie_order(self):
        popular = Experience.objects.create(
            order=2,
            title="Popular Teaching",
            company="Fasilkom UI",
            period="2025",
            category="Teaching",
            description="Popular teaching role.",
            tags="Teaching",
        )
        tied = Experience.objects.create(
            order=3,
            title="Internship Role",
            company="Company",
            period="2024",
            category="Internship",
            description="An internship.",
            tags="Python",
        )
        Experience.objects.create(
            order=4,
            title="Unstarred Teaching",
            company="Fasilkom UI",
            period="2023",
            category="Teaching",
            description="Another teaching role.",
            tags="Teaching",
        )
        self.experience.starred_by.add(self.regular)
        popular.starred_by.add(self.regular, self.editor)
        tied.starred_by.add(self.owner)

        params = {"sort": "most-starred"}
        expected = [
            "Popular Teaching",
            "Teaching Assistant",
            "Internship Role",
            "Unstarred Teaching",
        ]
        api_url = reverse("main:get_experience_json")
        api_items = self.client.get(api_url, params).json()
        self.assertEqual(
            [item["fields"]["title"] for item in api_items], expected
        )
        self.assertEqual(
            [item["fields"]["star_count"] for item in api_items], [2, 1, 1, 0]
        )
        self.assertTrue(
            all("starred_by" not in item["fields"] for item in api_items)
        )

        page = self.client.get(reverse("main:show_experience"), params)
        self.assertNotContains(page, "Popular Teaching")
        self.assertContains(page, "Sort: Most Starred")

        self.client.force_login(self.regular)
        logged_in_page = self.client.get(
            reverse("main:show_experience"), params
        )
        self.assertContains(logged_in_page, 'const IS_AUTHENTICATED = "true"')
        self.assertNotContains(logged_in_page, "Dibintangi oleh")
        logged_in_items = self.client.get(api_url, params).json()
        self.assertTrue(logged_in_items[0]["fields"]["is_starred"])
        self.assertEqual(logged_in_items[0]["fields"]["star_count"], 2)

        filtered = self.client.get(
            api_url, {"category": "Teaching", "sort": "most-starred"}
        ).json()
        self.assertEqual(
            [item["fields"]["title"] for item in filtered],
            ["Popular Teaching", "Teaching Assistant", "Unstarred Teaching"],
        )

    def test_login_next_allows_internal_path_but_rejects_external_url(self):
        login_url = reverse("main:login")
        list_url = reverse("main:show_experience")
        safe_page = self.client.get(f"{login_url}?next={list_url}")
        self.assertContains(safe_page, f'name="next" value="{list_url}"')
        self.assertRedirects(
            self.client.post(login_url, {
                "username": "regular",
                "password": "SafePassword123!",
                "next": list_url,
            }),
            list_url,
        )
        self.client.logout()

        invalid_login = self.client.post(login_url, {
            "username": "regular",
            "password": "wrong-password",
            "next": list_url,
        })
        self.assertEqual(invalid_login.status_code, 200)
        self.assertContains(invalid_login, f'name="next" value="{list_url}"')

        for destination in ("https://evil.example/", "//evil.example/"):
            with self.subTest(destination=destination):
                page = self.client.get(login_url, {"next": destination})
                self.assertNotContains(page, 'name="next"')
                self.assertRedirects(
                    self.client.post(login_url, {
                        "username": "regular",
                        "password": "SafePassword123!",
                        "next": destination,
                    }),
                    reverse("main:show_main"),
                )
                self.client.logout()
