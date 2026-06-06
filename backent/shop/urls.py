from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CategoryViewSet, ProductViewSet, home_page, 
    favorites_page, add_product_page, delivery_page, 
    profile_page, product_detail_page, toggle_favorite_api
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    # 1. Саҳифаи асосӣ
    path('', views.home_page, name='home'),
    
    # 2. Саҳифаи мукаммали маҳсулот
    path('product/<int:product_id>/', views.product_detail_page, name='product_detail'),
        
    # 3. Интихобшуда (Favorites)
    path('favorites/', views.favorites_page, name='favorites'),
    
    # 4. Фурӯшанда (Иловаи маҳсулот)
    path('add-product/', views.add_product_page, name='add_product'),
    
    # 5. Расонидан (Доставка)
    path('delivery/', views.delivery_page, name='delivery'),

    path('delete-product-api/<int:product_id>/', views.delete_product_api, name='delete_product_api'),
    
    # 6. Профил
    path('profile/', views.profile_page, name='profile'),
    
    # API барои роутер (Бэкэнд)
    path('api/', include(router.urls)),
    
    # API барои тугмаи дилак тавассути JavaScript
    path('favorite/toggle/<int:product_id>/', views.toggle_favorite_api, name='toggle_favorite_api'),
]