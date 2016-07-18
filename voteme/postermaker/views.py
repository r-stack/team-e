# -*- coding:utf-8 -*-


from django.conf import settings
from django.views.generic import TemplateView
from postermaker.models import User
from requests_oauthlib import OAuth1Session


class PosterView(TemplateView):
    template_name = "postermaker/poster.html"

    _CONSUMER_KEY = settings.SOCIAL_AUTH_TWITTER_KEY
    _CONSUMER_SECRET = settings.SOCIAL_AUTH_TWITTER_SECRET
    _REQUEST_TOKEN_URL = settings.TWITTER_REQUEST_TOKEN_URL
    _AUTHORIZATION_URL = settings.TWITTER_AUTHORIZATION_URL

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def authorization_request(self):
        oauth_client = OAuth1Session(self._CONSUMER_KEY,
                                     client_secret=self._CONSUMER_SECRET)
        try:
            resp = oauth_client.fetch_request_token(self._REQUEST_TOKEN_URL)
            oauth = User(
                        oauth_token=resp.get('oauth_token'),
                        oauth_token_secret=resp.get('oauth_token_secret'))
            oauth.save()
        except ValueError as err:
            print(err)
            return

        return oauth_client.authorization_url(self._AUTHORIZATION_URL)
