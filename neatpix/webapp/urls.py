from django.conf.urls import url
from views import IndexView, DashboardView


urlpatterns = [

    url(r'^$',
        IndexView.as_view(),
        name='index'),

    url(r'^(?P<slug>[\w-]+)/dashboard/$',
        DashboardView.as_view(),
        name='dashboard'),

]
