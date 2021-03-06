from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
app_name= "ml_core"
urlpatterns = [
    path('create/', views.CreateProcess.as_view(), name='create-process'),
    path('<int:pk>/', views.DetailProcess.as_view(), name='process'),
    path('<int:pk>/update/', views.UpdateProcess.as_view(), name='update-process'),
    path('<int:pk>/delete/', views.DeleteProcess.as_view(), name='delete-process'),
    path('my-process/', views.ListProcesses.as_view(), name='list-process'),
    path('csv-list/', views.ListCSV.as_view(), name='list-csv'),
    path('csv/create/', views.CreateCSV.as_view(), name='create-csv'),
    path('csv/delete/<int:pk>', views.DeleteCSV.as_view(), name='delete-csv'),
    #path('execute/<str:model>/<str:machine>/<str:csv>/<str:target>/<int:test>', views.RPCRecieverTest.as_view(), name='execute'),
    path('execute/<int:pk>', views.RPCRecieverTest.as_view(), name='execute'),
    path('instance/create/', views.CreateInstance.as_view(), name='create-instance'),
    path('instance/delete/<int:pk>', views.DeleteInstance.as_view(), name='delete-instance'),
    path('instances/', views.ListInstances.as_view(), name='list-instance'),
    path('instance/update/<int:pk>', views.UpdateInstance.as_view(), name='update-instance'),
    path('model/create/', views.CreateModel.as_view(), name='create-model'),
    path('model/update/<int:pk>', views.UpdateModel.as_view(), name='update-model'),
    path('model/delete/<int:pk>', views.DeleteModel.as_view(), name='delete-model'),
    path('models/', views.ListModels.as_view(), name='list-model'),
]
