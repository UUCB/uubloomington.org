from wagtail.embeds.finders.base import EmbedFinder
import re


class VimeoChatEmbedFinder(EmbedFinder):
    def __init__(self, **options):
        pass

    def accept(self, url):
        """
        Returns True if this finder knows how to fetch an embed for the URL.

        This should not have any side effects (no requests to external servers)
        """
        if re.search("^https://vimeo.com/event.*/chat/interaction/.*$", url):
            return True
        else:
            return False

    def find_embed(self, url, max_width=None):
        """
        Takes a URL and max width and returns a dictionary of information about the
        content to be used for embedding it on the site.

        This is the part that may make requests to external APIs.
        """
        try:
            options = url.split('||')[1]
        except IndexError:
            options = None

        css_class = "hidden"

        if options is not None:
            if "show" in options:
                css_class = ""
        # TODO: Document ||show option here
        return {
            'title': "Vimeo Chat",
            'author_name': "UU Church of Bloomington",
            'provider_name': "Vimeo Chat",
            'type': "rich",
            'thumbnail_url': "URL to thumbnail image",
            'width': 360,
            'height': 640,
            'html': f'<a href="javascript:void(0)" _="on click toggle .hidden on <#vimeo-chat/> then halt">Show/Hide Livestream Chat</a><iframe class="{css_class}" id="vimeo-chat" src="{url.split("||")[0]}" width="400" height="600" frameborder="0" class="vimeo-chat"></iframe>',
        }