from django.test.utils import override_settings

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import BitbucketOAuth2Provider


@override_settings(SOCIALACCOUNT_QUERY_EMAIL=True, SOCIALACCOUNT_STORE_TOKENS=True)
class BitbucketOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = BitbucketOAuth2Provider.id

    response_data = """
        {
            "created_on": "2011-12-20T16:34:07.132459+00:00",
            "display_name": "tutorials account",
            "links": {
                "avatar": {
                    "href":
                    "https://bitbucket-assetroot.s3.amazonaws.com/c/photos/2013/Nov/25/tutorials-avatar-1563784409-6_avatar.png"
                },
                "followers": {
                    "href":
                    "https://api.bitbucket.org/2.0/users/tutorials/followers"
                },
                "following": {
                    "href":
                    "https://api.bitbucket.org/2.0/users/tutorials/following"
                },
                "html": {
                    "href": "https://bitbucket.org/tutorials"
                },
                "repositories": {
                    "href":
                    "https://api.bitbucket.org/2.0/repositories/tutorials"
                },
                "self": {
                    "href": "https://api.bitbucket.org/2.0/users/tutorials"
                }
            },
            "location": "Santa Monica, CA",
            "type": "user",
            "username": "tutorials",
            "uuid": "{c788b2da-b7a2-404c-9e26-d3f077557007}",
            "website": "https://tutorials.bitbucket.org/"
        }
    """  # noqa

    email_response_data = """
        {
            "page": 1,
            "pagelen": 10,
            "size": 1,
            "values": [
                {
                    "email": "tutorials@bitbucket.org",
                    "is_confirmed": true,
                    "is_primary": true,
                    "links": {
                        "self": {
                            "href":
                            "https://api.bitbucket.org/2.0/user/emails/tutorials@bitbucket.org"
                        }
                    },
                    "type": "email"
                },
                {
                    "email": "tutorials+secondary@bitbucket.org",
                    "is_confirmed": true,
                    "is_primary": true,
                    "links": {
                        "self": {
                            "href":
                            "https://api.bitbucket.org/2.0/user/emails/tutorials+secondary@bitbucket.org"
                        }
                    },
                    "type": "email"
                }
            ]
        }
    """  # noqa

    def get_mocked_response(self):
        return [
            MockedResponse(200, self.response_data),
            MockedResponse(200, self.email_response_data),
            MockedResponse(200, self.response_data),
            MockedResponse(200, self.email_response_data),
        ]

    def test_provider_account(self):
        self.login(self.get_mocked_response())
        socialaccount = SocialAccount.objects.get(uid="tutorials")
        self.assertEqual(socialaccount.user.username, "tutorials")
        self.assertEqual(socialaccount.user.email, "tutorials@bitbucket.org")
        account = socialaccount.get_provider_account()
        self.assertEqual(account.to_str(), "tutorials account")
        self.assertEqual(account.get_profile_url(), "https://bitbucket.org/tutorials")
        self.assertEqual(
            account.get_avatar_url(),
            "https://bitbucket-assetroot.s3.amazonaws.com/c/photos/2013/Nov/25/tutorials-avatar-1563784409-6_avatar.png",  # noqa
        )
