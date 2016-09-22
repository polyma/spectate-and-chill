"""spectate_and_chill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from cassiopeia import riotapi, baseriotapi
from cassiopeia.type.api import APIError


# Initialize cassiopeia settings
def auto_retry(api_call_method):
    """ A decorator to automatically retry 500s (Service Unavailable) and skip 400s (Bad Request) or 404s (Not Found). """
    def call_wrapper(*args, **kwargs):
        try:
            return api_call_method(*args, **kwargs)
        except APIError as error:
            # Try Again Once
            if error.error_code in [500]:
                try:
                    return api_call_method(*args, **kwargs)
                except APIError as another_error:
                    if another_error.error_code in [500, 400, 404]:
                        return None
                    else:
                        raise another_error

            # Skip
            elif error.error_code in [400, 404]:
                return None

            # Fatal
            else:
                raise error
    return call_wrapper


riotapi.set_load_policy("lazy")
riotapi.set_rate_limit((25000, 10))
riotapi.set_data_store(None)
riotapi.set_api_key("RGAPI-e4491f0b-b99a-49c4-b817-5f9b00267da1")
baseriotapi.get_current_game = auto_retry(baseriotapi.get_current_game)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('chillhome.urls')),
]
