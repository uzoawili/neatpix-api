from django.conf.urls import url
from views import IndexView, DashboardView,\
                  LogoutView


urlpatterns = [

    url(r'^$',
        IndexView.as_view(),
        name='index'),

    url(r'^dashboard/$',
        DashboardView.as_view(),
        name='dashboard'),

    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),

]
