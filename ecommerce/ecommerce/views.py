"""Project-level views.

The service worker must be served from the site root so that its scope is "/"
(a worker served from /static/ can only control /static/*), which is why it is
routed here instead of being left to the static files handler.
"""
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def service_worker(request):
    sw_path = Path(settings.BASE_DIR) / "static" / "service-worker.js"
    if not sw_path.exists():
        raise Http404("service-worker.js not found")
    response = FileResponse(open(sw_path, "rb"), content_type="application/javascript")
    # Allow the worker to control the whole origin.
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"
    return response
