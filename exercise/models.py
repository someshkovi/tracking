from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings
import datetime

from django.urls import reverse, reverse_lazy

body_part_choices = (
    ('Abs', 'Abs'),
    ('Back', 'Back'),
    ('Biceps', 'Biceps'),
    ('Cardio', 'Cardio'),
    ('Chest', 'Chest'),
    ('Legs', 'Legs'),
    ('Shoulders', 'Shoulders'),
    ('Triceps', 'Triceps'),
    ('Other', 'Other')
)


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    primary_body_part = models.CharField(max_length=20, choices=body_part_choices)
    other_body_parts = models.CharField(max_length=200, null=True, blank=True)
    view_link = models.URLField(max_length=500, null=True, blank=True)
    suggestions = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['primary_body_part', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.pk:
            return reverse("exercise:exercise-detail", kwargs={"pk": self.pk})
        return reverse_lazy('exercise:exercise-list')


class ExerciseTracker(models.Model):
    date = models.DateField(default=datetime.date.today)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(help_text='Enter count per rep, or keep rep 1 and total count',
                                             null=True, blank=True)
    repetitions = models.PositiveSmallIntegerField(default=1)
    weight = models.DecimalField(max_digits=4,
                                 decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))],
                                 null=True,
                                 blank=True)
    # duration = models.DecimalField(max_digits=4,
    #                                decimal_places=2,
    #                                validators=[MinValueValidator(Decimal('0.01'))],
    #                                null=True,
    #                                blank=True)
    duration = models.DurationField(help_text='Duration in hh:mm:ss', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_stamp', 'exercise', 'user']

    def __str__(self):
        return f'{self.exercise}, {self.date}, {self.user}'

    def get_absolute_url(self):
        if self.pk:
            return reverse("exercise:exercisetracker-detail", kwargs={"pk": self.pk})
        return reverse_lazy('exercise:exercisetracker-list')
