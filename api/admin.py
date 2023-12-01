from django.contrib import admin
from api.models import Answer, Question, FAQ, Category

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(FAQ)
