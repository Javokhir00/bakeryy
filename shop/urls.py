from django.urls import path
from .views import Index, product_detail, comment_add, all_product_list, get_cart_products, add_to_cart, remove_from_cart, get_user_cart, clear_cart, toggle_like, get_user_likes

app_name = 'shop'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<slug:category_slug>/', Index.as_view(), name='products_by_category'),
    path('products/', all_product_list, name = 'products_list'),
    path('detail/<int:product_id>/', product_detail, name='product_detail'),
    path('comment_add/<int:product_id>/', comment_add, name='comment_add'),
    path('api/cart-products/', get_cart_products, name='get_cart_products'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('api/user-cart/', get_user_cart, name='get_user_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('toggle-like/<int:product_id>/', toggle_like, name='toggle_like'),
    path('api/user-likes/', get_user_likes, name='get_user_likes'),
]