from django.conf.urls import url
from views import IndexView, FacebookAuthView,\
                  DashboardView, LogoutView,\
                  PhotosListView


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

    url(r'^dashboard/photos/$',
        PhotosListView.as_view(),
        name='photo_list'),

    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),

]
