from urllib import request
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Users.utils.email_utils import EmailUtils


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
    
class SendVerificationEmail:
    @staticmethod
    def send_verification_email(request_site, user):
        context = CommonUtils(request=request_site).create_context(user=user)
        html_content = f'<a type="button" style="color: #0a3370;padding: 7px 15px; color: #fff; background: #0a3370; border-radius: 20px;text-decoration: none;display: inline-block;" href="{context.get("protocol")}://{context.get("domain")}/user-auth/email-verification/{context.get("uid")}/{context.get("token")}/">Verification Link</a>'
        EmailUtils().send_email(to_emails=user.email, subject='Verification Mail', html_content=html_content)

    @staticmethod
    def send_reset_password_email(request_site, user):
        context = CommonUtils(request=request_site).create_context(user=user)
        html_content = f'<a type="button" style="color: #0a3370;padding: 7px 15px; color: #fff; background: #0a3370; border-radius: 20px;text-decoration: none;display: inline-block;" href="{context.get("protocol")}://{context.get("domain")}/user-auth/reset-password/{context.get("uid")}/{context.get("token")}/">Password Reset Link</a>'
        EmailUtils().send_email(to_emails=user.email, subject='Password Reset Mail', html_content=html_content)