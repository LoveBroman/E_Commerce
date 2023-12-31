from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("listing/<id>", views.listing, name="listing"),
    path("listing/<id>/makebid", views.makebid, name="makebid"),
    path("listing/<id>/makecomment", views.make_comment, name="makecomment")
]
