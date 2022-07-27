from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('search', views.search, name='search'),
    path('search_cartegory', views.search_cartegory, name='search_cartegory'),
    path('show_map', views.show_map, name='show_map'),
    path('Distance', views.Distance, name='Distance'),

    path('register', views.register, name='register'),
    path('loging', views.loging, name='Kuingia'),
    path('mteja wetu', views.add_product, name='mteja wetu'),
    path('add_product', views.add_product, name='add_product'),


    path('Kuhusu Sisi', views.about_us, name='Kuhusu Sisi'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
]
