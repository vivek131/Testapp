from django.urls import path
from .views import *
#saare views import krlo

urlpatterns=[
    #path('login/',login),
    path('new-question/',newQuestion),
    path('save-question/',saveQuestion),
    path('view-questions/',viewQuestions),
    path('edit-question/',editQuestion),
    path('edit-save-question/',editSaveQuestion),
    path('delete-question/',deleteQuestion),
    path('signup/',signup),
    path('save-user/',saveUser),
    path('logout/',logout),
    path('login-validation/',loginValidation),
    path('home/',home),
    path('start-test/',startTest),
    path('test-result/',testResult),
    path('view-users/',viewusers),
    path('delete-user/',deleteUser),
]