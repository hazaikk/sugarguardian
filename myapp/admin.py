from django.contrib import admin

from myapp.models import Prediction, Body


# Register your models here.
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('gender', 'year', 'tall', 'weight', 'family', 'press', 'test', 'release', 'thick')

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


class BodyAdmin(admin.ModelAdmin):
    list_display = ('bmi', 'heart', 'ssy', 'szy', 'bl', 'bg', 'bone', 'muscle')

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Prediction,PredictionAdmin)
admin.site.register(Body,BodyAdmin)
admin.site.site_header = ('糖尿病检测后台')
admin.site.site_title = ('糖尿病检测后台')