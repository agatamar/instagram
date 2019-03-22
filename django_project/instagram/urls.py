from django.conf.urls import url
from django.urls import path

from django.views import generic
from instagram import views

app_name = 'instagram'
urlpatterns = [
    # path('', generic.TemplateView.as_view(template_name='twitter/index.html'),
    #      name='index'),
    path('', views.MainView.as_view(),
         name='index'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('compose/',views.ComposeView.as_view(),name='compose'),
    # path('user/<int:pk>/', views.AuthorDetailView.as_view(),name='author-detail'),
    # path('tweet/<int:pk>/', views.TweetDetailView.as_view(),name='tweet-detail'),
    # path('add_message/',views.AddMessageView.as_view(),name='add_message'),
    # path('message/<int:pk>/',views.MessageDetailView.as_view(),name='message'),
    # path('messages/',views.MessageListView.as_view(),name='messages'),
    path('upload_photo/',views.UploadPhotoView.as_view(template_name='instagram/upload_photo.html'),name='upload'),
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(),name='photo-details'),
    url(r'^photo/(?P<photo_id>\d+)/preference/(?P<preference_type>\d+)/$', views.PostPreferenceView.as_view(), name='postpreference'),


]