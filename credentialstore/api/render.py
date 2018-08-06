# api/render.py

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class CredStoreBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    Inherited customized BrowsableAPIRenderer used for users that
    use a browser to query the API. This will point to a customized
    template to maintain site formatting from the base.html template.
    Also set the default rendere to be JSONRenderer().
    """
    template = 'api/query_results.html'

    def get_default_renderer(self, view):
        return JSONRenderer()
