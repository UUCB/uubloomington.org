from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.template.loader import render_to_string
from wagtail.embeds.finders.base import EmbedFinder

import urllib.parse


class AudioEmbedFinder(EmbedFinder):

    supported_schemes = ["http", "https"]

    def __init__(self, **options):
        pass

    def accept(self, url):
        # Fix scheme if not present
        url = f"//{url}" if "//" not in url else url

        # Parse URL
        parsed_url = urllib.parse.urlparse(url, scheme="https")

        # Validate URL
        validate = URLValidator()
        try:
            validate(parsed_url.geturl())
        except ValidationError:
            return False

        # Allow only supported schemes
        if parsed_url.scheme not in self.supported_schemes:
            return False

        # Support ogg files for now (need ogg in URL)
        return ".ogg" in parsed_url.path

    def _get_html(self, ctx):
        return render_to_string("wagtailaudioembed/audio.html", ctx)

    def find_embed(self, url, max_width=None):
        """
        Takes a URL and max width and returns a dictionary of information about the
        content to be used for embedding it on the site.

        This is the part that may make requests to external APIs.
        """
        # TODO: Perform the request

        ctx = {"title": "", "url": url}

        return {
            "title": ctx["title"],
            "author_name": "Author name",
            "provider_name": "Local",
            "type": "rich",
            "width": 0,  # useless, but mandatory
            "height": 0,  # useless, but mandatory
            "html": self._get_html(ctx),
        }
