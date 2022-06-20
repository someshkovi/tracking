from django.contrib import admin

# Register your models here.
from exercise.models import Exercise, ExerciseTracker


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_body_part']
    list_filter = ['primary_body_part']


class FilterUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(FilterUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user == request.user


@admin.register(ExerciseTracker)
class ExerciseTrackerAdmin(FilterUserAdmin):
    list_editable = ['count', 'repetitions', 'weight', 'duration']
    list_display = ['date', 'exercise', 'count', 'repetitions', 'weight', 'duration']
    list_filter = ['date', 'exercise']
    exclude = ['user', ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        obj.save()

    def queryset(self, request):
        """
        Filtering the objects dispalyed in the change_list
        to only display those for current signed in user
        """

        qs = super(ExerciseTrackerAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.site_header = 'Tracker'
admin.site.site_title = 'Tracker'
