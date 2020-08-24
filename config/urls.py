from des import urls as des_url

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

from sme_material_apps.core.api.urls import urlpatterns as core_url
from sme_material_apps.proponentes.urls import urlpatterns as proponentes_url
from sme_material_apps.custom_user.urls import urlpatterns as url_users

schema_view = get_swagger_view(title="Portal SME Material Escolar")

urlpatterns = [
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  path("docs/", schema_view),
                  path("django-des/", include(des_url)),
                  # User management
                  # path("users/", include("sme_material_apps.users.urls", namespace="users")),
                  # path("accounts/", include("allauth.urls")),
                  # Your stuff: custom urls includes go here
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    # path("v1/", include(core_url)),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api-token-auth/", obtain_jwt_token),
    path("api-token-refresh/", refresh_jwt_token),
]
urlpatterns += core_url
urlpatterns += proponentes_url
urlpatterns += url_users

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    # urlpatterns += [
    #     path(
    #         "400/",
    #         default_views.bad_request,
    #         kwargs={"exception": Exception("Bad Request!")},
    #     ),
    #     path(
    #         "403/",
    #         default_views.permission_denied,
    #         kwargs={"exception": Exception("Permission Denied")},
    #     ),
    #     path(
    #         "404/",
    #         default_views.page_not_found,
    #         kwargs={"exception": Exception("Page not Found")},
    #     ),
    #     path("500/", default_views.server_error),
    # ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
