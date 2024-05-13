from django.urls import path, re_path
from . import views
app_name = 'myapp'
urlpatterns = [
    path("", views.login, name='login'),
    path("404", views.build, name='build'),
    path("result", views.result, name='result'),
    path("doctor", views.doctor, name='doctor'),
    path("visual", views.visual, name='visual'),
    re_path(r'^profile/$', views.profile, name='profile'),
    path("prediction", views.PredictionCreate.as_view(), name='prediction'),
    path("data", views.DataCreate.as_view(), name='data'),
    path("body/<int:pindex>", views.body, name='body'),
    path("data/<int:data_id>", views.detail, name='detail'),
    path("community", views.community, name='community'),
]