# from django.conf.urls import url
from django.urls import path

from Home import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    
    path('ArtCreate', views.ArtCreateView.as_view(), name="ArtCreate"),
    path('ArtDetail/<pk>', views.ArtDetailView.as_view(), name="ArtDetail"),
    path('ArtDetail/<pk>/ArtEdit', views.ArtUpdateView.as_view(), name="ArtEdit"),
    path('ArtDetail/<pk>/ArtDelete', views.ArtDeleteView.as_view(), name="ArtDelete"),
    path('ArtList', views.art_list, name="ArtList"),
    path('ArtsSearch', views.art_search_title, name="ArtsSearch"),
    path('ArtDetail/<pk>/ArtListAutor', views.art_list_author, name="ArtListAutor"),
    path('MyArts', views.my_arts, name="MyArts"),
    path('AuthorsList', views.authors_list, name="AuthorsList"),

]

urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)