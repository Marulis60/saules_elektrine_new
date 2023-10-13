from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('klientai/', views.klientai, name='klientai'),
    path('klientai/<int:klientas_id>', views.klientas, name='klientas'),
    path('objektai/', views.ObjektasListView.as_view(), name='objektai'),
    path('objektai/<int:pk>', views.ObjektasDetailView.as_view(), name='objektas'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name="register"),
    path("profilis/", views.profilis, name="profilis"),
    path("manoobjektai/", views.UserObjektaiListView.as_view(), name='manoobjektai'),
    path("manoobjektai/<int:pk>", views.ObjektasDetailView.as_view(), name='manoobjektas'),
    path("manoobjektai/new/", views.UserObjektaiCreateView.as_view(), name="manoobjektai_new"),
    path("manoobjektai/<int:pk>/update", views.UserObjektaiUpdateView.as_view(), name='manoobjektas_Update'),
    path("manoobjektai/<int:pk>/delete", views.UserObjektaiDeleteView.as_view(), name='manoobjektas_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('load-data/', views.my_view, name='load-data'),
]
