import os
import sys
import cStringIO

from webscraping import webkit
from PyQt4.QtCore import Qt, QSize,QBuffer,QIODevice,QUrl
from PyQt4.QtGui import QImage,QPainter,QApplication
from PyQt4.QtWebKit import QWebView,QWebSettings

class ScreenShotter(webkit.WebkitBrowser):

    def __init__(self, gui=True, user_agent=None, proxy=None, load_images=True, forbidden_extensions=None, timeout=15, delay=0, enable_plugins=True, display=":1", screenWidth=0, screenHeight=0):
        os.environ["DISPLAY"] = display

        self.app = QApplication(sys.argv) # must instantiate first

        QWebView.__init__(self)

        manager = webkit.NetworkAccessManager(proxy, forbidden_extensions, "", cache_size=100, cache_dir='/tmp/webkit_cache')

        self.base_url = None # don't use this feature

        manager.finished.connect(self.finished)

        webpage = webkit.WebPage(user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:22.0) Gecko/20100101 Firefox/22.0')

        webpage.setNetworkAccessManager(manager)

        self.setPage(webpage)

        self.timeout = timeout
        self.delay = delay

        # enable flash plugin etc.
        self.settings().setAttribute(QWebSettings.PluginsEnabled, enable_plugins)
        self.settings().setAttribute(QWebSettings.JavaEnabled, enable_plugins)
        self.settings().setAttribute(QWebSettings.AutoLoadImages, load_images)
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)

        if gui: self.show() 

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def screenshot(self):
        frame = self.page().mainFrame()
        size = frame.contentsSize()

        if (self.screenWidth or self.screenHeight):
           size.setWidth(self.screenWidth)
           size.setHeight(self.screenHeight)

        self.page().setViewportSize(size)
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()

        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        image.save(buffer, "JPG")

        return buffer.data()

    def screenshotHTML(self,html):
        self.get(html = html, url='file://')

        return self.screenshot()

if __name__ == '__main__':
    print ""
