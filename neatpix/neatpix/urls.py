"""
neatpix URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [

    # admin routes:
    url(r'^admin/',
        include(admin.site.urls)),

    # webapp routes:
    url(r'^',
        include('webapp.urls',
                namespace='webapp')),

]
