from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

import sys
import os
import logging

from PIL import Image

from screenshot import ScreenShotter

@csrf_exempt
def screenshot(request):

    logging.info('Screenshot request received')

    if request.method == 'POST' and 'file' in request.FILES:
        try:
            logging.info('Screenshot request being processed')

            file = request.FILES['file']

            screenWidth = int(request.POST.get('screenWidth')) if request.POST.get('screenWidth') else None
            screenHeight = int(request.POST.get('screenHeight')) if request.POST.get('screenHeight') else None
            minWidth = int(request.POST.get('minWidth')) if request.POST.get('minWidth') else None
            minHeight = int(request.POST.get('minHeight')) if request.POST.get('minHeight') else None
            quality = int(request.POST.get('quality')) if request.POST.get('quality') else None
            format = str(request.POST.get('format')) if request.POST.get('format') else None
            html = file.read()

            screenshot = ScreenShotter(screenWidth = screenWidth, screenHeight = screenHeight, minWidth = minWidth, minHeight = minHeight, format = format, quality = quality)
            rendering = screenshot.screenshotHTML(html = html)

            logging.info('Screenshot request successfully processed')

            return HttpResponse(rendering['content'], content_type=rendering['content_type'])

        except ValueError:
            logging.error('Invalid arguments passed with request, returned 400')

            return HttpResponse('Invalid arguments passed with request', status = 400)

        except Exception, e:
            logging.error(e.args[0] + " " + type(e).__class__.__name__ + " " + 'returned 400')

            return HttpResponse(e.args[0] + " " + type(e).__class__.__name__, status = 400)

    else:
        logging.error('Invalid or unsupported request, returned 400')

        return HttpResponse('Invalid or unsupported request', status = 400)
