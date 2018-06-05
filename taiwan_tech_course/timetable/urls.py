from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.timetable, name='timetable'),
    url(r'api/search', views.search_api, name='timetable_search_api'),
    url(r'api/add', views.add_api, name='timetable_add_api'),
    url(r'api/del', views.del_api, name='timetable_del_api'),
    url(r'api/get', views.get_course_api, name='timetable_get_api'),
]