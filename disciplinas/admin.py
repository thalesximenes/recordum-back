from django.contrib import admin
from .models import Disciplinas, Aulas, EixosTematicos, MapasTextos, Temas

admin.site.register(Aulas)
admin.site.register(Disciplinas)
admin.site.register(EixosTematicos)
admin.site.register(MapasTextos)
admin.site.register(Temas)