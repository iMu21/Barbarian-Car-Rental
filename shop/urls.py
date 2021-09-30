from django.urls import path
from . import views

urlpatterns = [
     path("",views.home,name="ShopeHome"),
     path("home",views.home,name="ShopeHome"),
     path("about",views.about,name="AboutUs"),
     path("contact",views.contact,name="ContactUs"),
     path("search",views.search,name="Search"),
     path("productview",views.productView,name="ProductView"),
     path("checkout",views.checkout,name="Checkout"),
     path("supercategory",views.supercategory,name='Supercategory'),
     path("addcart",views.addcart,name='Add Cart'),
     path("productView",views.productView,name='Product View'),
     path("error",views.error,name='Error'),
     path("category",views.category,name='category'),
     path("confirmBuying",views.confirmBuying,name='confirmBuying')
]
