from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser

from exercise.models import Exercise, ExerciseTracker


class ExerciseListView(ListView):
    model = Exercise
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ExerciseDetailView(DetailView):
    model = Exercise

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ExerciseTrackerListView(ListView):
    model = ExerciseTracker
    # queryset = ExerciseTracker.objects.all()

    def get_queryset(self):
        # self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        # return Book.objects.filter(publisher=self.publisher)
        self.user = self.request.user if self.request.user.is_authenticated else None
        if self.user:
            return ExerciseTracker.objects.filter(user=self.user)
        return ExerciseTracker.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ExerciseTrackerDetailView(DetailView):
    model = ExerciseTracker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ExerciseTrackerCreateView(CreateView):
    model = ExerciseTracker
    # fields = ['name']

class ExerciseTrackerUpdateView(UpdateView):
    model = ExerciseTracker
    # fields = ['name']

class ExerciseTrackerDeleteView(DeleteView):
    model = ExerciseTracker
    success_url = reverse_lazy('exercisetracker-list')