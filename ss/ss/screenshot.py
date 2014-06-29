import os
import sys
import cStringIO
import mimetypes
import logging

from webscraping import webkit
from PyQt4.QtCore import Qt, QSize,QBuffer,QIODevice,QUrl
from PyQt4.QtGui import QImage,QPainter,QApplication
from PyQt4.QtWebKit import QWebView,QWebSettings

class ScreenShotter(webkit.WebkitBrowser):

    def __init__(self, gui=True, user_agent=None, proxy=None, load_images=True, forbidden_extensions=None, timeout=15, delay=0,
                 enable_plugins=True, display=":1", screenWidth=None, screenHeight=None, minWidth=None, minHeight=None, format=None,
                 quality=None):

        logging.debug('Attempting to create Screenshot instance')

        os.environ["DISPLAY"] = display

        self.app = QApplication(sys.argv) # must instantiate first

        QWebView.__init__(self)

        manager = webkit.NetworkAccessManager(proxy, forbidden_extensions, "", cache_size=100, cache_dir='/tmp/webkit_cache')

        self.base_url = None # don't use this feature

        manager.finished.connect(self.finished)

        webpage = webkit.WebPage(user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:22.0) Gecko/20100101 Firefox/22.0')

        webpage.setNetworkAccessManager(manager)

        self.setPage(webpage)

        # enable flash plugin etc.
        self.settings().setAttribute(QWebSettings.PluginsEnabled, enable_plugins)
        self.settings().setAttribute(QWebSettings.JavaEnabled, enable_plugins)
        self.settings().setAttribute(QWebSettings.AutoLoadImages, load_images)
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)

        if gui: self.show() 

        self.timeout = timeout
        self.delay = delay

        self.format = format if format == 'jpg' or format == 'png' else 'jpg' 
        self.quality = quality if 0 <= quality <= 100 else 90 

        self.content_type, self.encoding = mimetypes.guess_type('filename.' + self.format)

        self.screenWidth = screenWidth or 1024
        self.screenHeight = screenHeight or 768

        self.minWidth = minWidth
        self.minHeight = minHeight

        logging.debug('Screenshot instance successfully created')

    def screenshot(self):
        logging.debug('screenshot() invoked')

        frame = self.page().mainFrame()
        size = frame.contentsSize()

        if (self.screenWidth):
           size.setWidth(self.screenWidth)

        if (self.screenHeight):
           size.setHeight(self.screenHeight)

        if (self.minWidth and self.minWidth > self.screenWidth):
           size.setWidth(self.minWidth)

        if (self.minHeight and self.minHeight > self.screenHeight):
           size.setHeight(self.minHeight)

        self.page().setViewportSize(size)
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()

        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        image.save(buffer, self.format, self.quality)

        logging.debug('screenshot() returned image of type ' + self.content_type + ' of length ' + str(buffer.data().length()))
        
        return { 'content': buffer.data(), 'content_type': self.content_type }

    def screenshotHTML(self,html):
        logging.debug('screenshotHTML() invoked')

        self.get(html = html, url='file://')

        if (self.is_binary(html)):
            raise ValueError('Expected text file for argument, received binary file')

        screenshot = self.screenshot()

        logging.debug('screenshotHTML() successfully returned')

        return screenshot

    def is_binary(self, data):
        textchars = ''.join(map(chr, [7,8,9,10,12,13,27] + range(0x20, 0x100)))
        is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

        return is_binary_string(data)
