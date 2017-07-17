from django.conf.urls import url
from werobot.contrib.django import make_view
from robot import robot
from django.contrib.auth import views as auth_views
import views

app_name = 'wechat'
urlpatterns = [
    url(r'^robot/', make_view(robot), name='robot_url'),
    url(r'^refreshfans/', views.refreshfans, name='refreshfans'),
    url(r'^refreshgroup/', views.refreshgroup, name='refreshgroup'),
    url(r'^send_text_message/', views.send_text_message, name='send_text_message'),
]
