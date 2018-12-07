from django.conf.urls import url
from django.urls import include, path
from basic_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'basic_app'
urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('post/createpost/', views.AddPostView.as_view(), name='createpost'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail_post'),
    path('user/<int:pk>/', views.UserAnnouncesList.as_view(), name='author_view'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)