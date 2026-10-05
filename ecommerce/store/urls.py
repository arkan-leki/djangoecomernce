from django.urls import path
from . import views

urlpatterns = [
    path('', views.store , name='store'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:product_slug>', views.product_info , name='product-info'),
    path('collection/<slug:collection_slug>', views.collection_detail, name='collection-detail'),
    path('search/<slug:category_slug>', views.list_category , name='list-category'),
]
