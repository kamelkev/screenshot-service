from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

import sys
import os
import logging
from PIL import Image

from screenshot import ScreenShotter

logger = logging.getLogger('default')

@csrf_exempt
def screenshot(request):

    if request.method == 'POST':

        if 'file' in request.FILES:
            file = request.FILES['file']
            html = file.read()

            try:
                if (('width' in request.POST and request.POST['width']) or ('height' in request.POST and request.POST['height'])):
                    screenshot = ScreenShotter(screenWidth = int(request.POST['width']), screenHeight = int(request.POST['height']))
                    rendering = screenshot.screenshotHTML(html = html)
                elif (('minwidth' in request.POST and request.POST['minwidth']) or ('minheight' in request.POST and request.POST['minheight'])):
                    screenshot = ScreenShotter(screenWidth = request.POST['minwidth'], screenHeight = request.POST['minheight'])
                    rendering = screenshot.screenshotHTML(html = html)
                else:
                    screenshot = ScreenShotter()
                    rendering = screenshot.screenshotHTML(html = html)

                return HttpResponse(rendering, content_type="image/jpeg")

            except Exception, e:
                return HttpResponse(e.args[0] + " " + type(e).__class__.__name__)

        else:
            return HttpResponse('You submitted an empty form.')

    else:
        return HttpResponse('Invalid or unsupported request.')
