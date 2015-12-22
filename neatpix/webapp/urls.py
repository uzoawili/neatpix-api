from django.conf.urls import url
from views import IndexView, FacebookAuthView,\
                  DashboardView, LogoutView


urlpatterns = [

    url(r'^$',
        IndexView.as_view(),
        name='index'),

    url(r'^auth/facebook/$',
        FacebookAuthView.as_view(),
        name='facebook_auth'),

    url(r'^dashboard/$',
        DashboardView.as_view(),
        name='dashboard'),

    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),

]
