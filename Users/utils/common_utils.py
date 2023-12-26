from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class CommonUtils:
    def __init__(self, request, use_https=False):
        # todo: Need to be changed for the production website
        self.request = request
        self.use_https = use_https

    def create_context(self, user):
        token_generator = default_token_generator
        site_name, domain = self.get_domain_and_site_name()
        context = {
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.email)),
                    'token': token_generator.make_token(user),
                    'protocol': 'https' if self.use_https else 'http',
                }
        return context

    def get_domain_and_site_name(self, domain_override=None):
        if not domain_override:
            current_site = get_current_site(self.request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        return site_name, domain