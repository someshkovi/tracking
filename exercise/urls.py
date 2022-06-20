from django.urls import path

from exercise.views import ExerciseListView, ExerciseDetailView, ExerciseTrackerListView, ExerciseTrackerDetailView


app_name = 'exercise'
urlpatterns = [
    path('exercise/', ExerciseListView.as_view(), name='exercise-list'),
    path('exercise/<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('', ExerciseTrackerListView.as_view(), name='exercisetracker-list'),
    path('<int:pk>/', ExerciseTrackerDetailView.as_view(), name='exercisetracker-detail'),
]