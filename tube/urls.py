from django.urls import path
from . import views


app_name = "tube"
urlpatterns =[
    path('', views.index, name="index"),

    # TIPS:<型:変数名>とすることでビューに変数を与えることができる

    #path('delete/<int:pk>', views.delete, name="delete"),
    #path('update/<int:pk>', views.update, name="update"),
    path('delete/<uuid:pk>', views.delete, name="delete"),
    path('update/<uuid:pk>', views.update, name="update"),
]
