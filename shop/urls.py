from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home_alt'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('api/search-suggest/', views.SearchSuggestView.as_view(), name='search_suggest'),
    path('api/validate-coupon/', views.CouponValidateView.as_view(), name='validate_coupon'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/review/', views.ReviewCreateView.as_view(), name='review_create'),
    path('supercategory/<int:pk>/', views.SuperCategoryDetailView.as_view(), name='supercategory_detail'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('rent/<int:pk>/', views.RentCarView.as_view(), name='rent_car'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm_order'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('booking/<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking_cancel'),
    path('favorite/<int:pk>/toggle/', views.FavoriteToggleView.as_view(), name='favorite_toggle'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    path('error/', views.ErrorView.as_view(), name='error'),
]
