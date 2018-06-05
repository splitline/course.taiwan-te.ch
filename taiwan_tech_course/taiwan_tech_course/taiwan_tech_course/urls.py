from django.conf.urls import url, include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'timetable/', include('timetable.urls')),
    url(r'^accounts/', include('allauth.urls')),
]
