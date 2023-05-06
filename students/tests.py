from django.test import TestCase, TransactionTestCase
from .models import Group, Students
from django.urls import reverse


class StudentModelTests(TestCase):
    def setUp(self):
        math_group = Group.objects.create(name="math", birth_year=1388)
        Students.objects.create(name="ali", age=15, group=math_group, score=5)
        Students.objects.create(name='reza', age=17, group=math_group, score=10)
        Students.objects.create(name='mohammad', age=16, group=math_group, score=7)

    def test_group_age(self):
        math_group = Group.objects.get(name="math")
        self.assertEqual(math_group.get_group_age(1402), 14)

    def test_student_age_gap(self):
        ali = Students.objects.get(name="ali")
        mohammad = Students.objects.get(name="mohammad")
        self.assertEqual(ali.get_age_gap(1402), 1)
        self.assertEqual(mohammad.get_age_gap(1402), 2)

    def test_student_rank(self):
        ali = Students.objects.get(name="ali")
        reza = Students.objects.get(name="reza")
        mohammad = Students.objects.get(name="mohammad")
        self.assertEqual(mohammad.get_rank_in_group(), 2)
        self.assertEqual(ali.get_rank_in_group(), 3)
        self.assertEqual(reza.get_rank_in_group(), 1)


class IndexViewTest(TestCase):
    def test_empty_index(self):
        response = self.client.get(reverse("students:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no groups yet!")

    def test_groups_in_index(self):
        math_group = Group.objects.create(name="math", birth_year=1388)
        science_group = Group.objects.create(name="science", birth_year=1388)
        response = self.client.get(reverse("students:index"))
        self.assertQuerysetEqual(list(response.context["groups"]),
                                 ["{'id': 1, 'name': 'math', 'birth_year': 1388}",
                                  "{'id': 2, 'name': 'science', 'birth_year': 1388}"]
                                 )


class AddRemoveViewTest(TestCase):
    def test_add_duplicated_group(self):
        Group.objects.create(name="math", birth_year=1388)
        url = reverse("students:add_group")
        data = {"name": "math", "birth": 1388}
        response = self.client.post(url, data)
        self.assertContains(response, "There is another group with this name.")

    def test_delete_not_exist_student(self):
        response = self.client.get(reverse("students:delete", args=(1,)))
        self.assertEqual(response.context['exception'], "Student does not exist")
        self.assertEqual(response.status_code, 404)

