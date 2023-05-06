from django.db import models
from django.contrib import admin


class Group(models.Model):
    name = models.CharField(max_length=200)
    birth_year = models.PositiveIntegerField(default=1380)

    def __str__(self):
        return self.name

    def get_group_age(self, current_year):
        return current_year - self.birth_year


class Students(models.Model):
    name = models.CharField(max_length=200, default='')
    age = models.PositiveSmallIntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_age_gap(self, current_year):
        return self.age - self.group.get_group_age(current_year)

    @admin.display(
        ordering="score",
        description="rank in group"
    )
    def get_rank_in_group(self):
        ordered_students = self.group.students_set.order_by('-score')
        for i in range(len(ordered_students)):
            if ordered_students[i].score == self.score:
                return i + 1

