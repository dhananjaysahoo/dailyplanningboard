from django.urls import path
from . import views

app_name = "dailyplanningboard"

urlpatterns = [
       path('',views.analytics,name="landingpageanalytics"),
       path('analytics',views.analytics,name="analytics"),
       path('login',views.login_view,name='login'),
       path('logout',views.logout_view,name='logout'),
       path('index',views.index,name="index"),
       path('<int:id>/edittask',views.edittask,name='edittask'),
       path('addtask',views.addtask,name="addtask"),
       path('custom',views.custom,name="custom"),
       path('<int:id>/customedit',views.customedit,name="customedit"),
       path('deletetask',views.deletetask,name="deletetask"),


]