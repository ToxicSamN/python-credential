# api/render.py

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class CredStoreBrowsableAPIRenderer(BrowsableAPIRenderer):
    template = 'api/query_results.html'

    def get_default_renderer(self, view):
        return JSONRenderer()