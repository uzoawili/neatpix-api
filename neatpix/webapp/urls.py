from django.conf.urls import url
from views import IndexView, FacebookAuthView,\
                  DashboardView, LogoutView,\
                  PhotosListView, PhotoUploadView,\
                  PhotoServiceView, PhotoUpdateDeleteView


urlpatterns = [

    url(r'^$',
        IndexView.as_view(),
        name='index'),

    url(r'^auth/facebook/$',
        FacebookAuthView.as_view(),
        name='facebook_auth'),

    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),

    url(r'^dashboard/$',
        DashboardView.as_view(),
        name='dashboard'),

    url(r'^dashboard/photos/$',
        PhotosListView.as_view(),
        name='photos'),

    url(r'^dashboard/photos/upload/$',
        PhotoUploadView.as_view(),
        name='photo_upload'),

    url(r'^dashboard/photos/(?P<public_id>[\w]+)/$',
        PhotoUpdateDeleteView.as_view(),
        name='photo_update_delete'),

    url(r'^media/photos/(?P<username>[\w\-]+)/' +
        r'((?P<effects>[\w\,]+)/)?(?P<filename>[\w\-\.]+)$',
        PhotoServiceView.as_view(),
        name='photo_service'),

]
