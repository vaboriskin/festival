from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель
    path('accounts/', include('accounts.urls')),  # URL-ы для регистрации и входа
    path('', include('main.urls')),  # Главная страница
    path('vote/', include('vote.urls')),
    path('Table/', include('Table.urls')),
    path('translation/', include('translation.urls')),

] + i18n_patterns(
    path('set_language/', set_language, name='set_language'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    path('vote/', include('vote.urls')),
    path('Table/', include('Table.urls')),
    path('translation/', include('translation.urls')),
    # Add this line
)
