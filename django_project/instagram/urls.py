from django.conf.urls import url
from django.urls import path

from django.views import generic
from instagram import views

app_name = 'instagram'
urlpatterns = [

    path('', views.MainView.as_view(),
         name='index'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('upload_photo/',views.UploadPhotoView.as_view(template_name='instagram/upload_photo.html'),name='upload'),
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(),name='photo-details'),
    url(r'^photo/(?P<photo_id>\d+)/preference/(?P<preference_type>\d+)/$', views.PostPreferenceView.as_view(), name='postpreference'),


]