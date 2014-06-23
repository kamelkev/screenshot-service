# ss

Screenshot Service - simplistic http based web service powered by Python and WebKit

## Purpose

This is a work in progress, right now this service will accept a submitted html file
and return back a rendering of said html through webkit. Moving forward the seemingly
straightforward step of rendering a remote url will also be added.

Right now the target platform is Linux. There is a chance that this can work elsewhere,
but at least xvfb is tightly bound to Linux, and the font rendering is known to be less
than ideal elsewhere as well.

## Setup

You'll Django already up and running, and obviously WebKit (4.8.x should be fine)

Django and WebKit don't play together so great when multiprocessing is enabled, so you'll
want to make sure you're running in single threaded mode. That's pretty simple to do with
mpm_prefork and I'm sure there are other ways to guarantee this as well.

In addition to Django the following libraries dependencies need to be installed:
- xvfb
- fontconfig
- python-imaging
- python-pip
- python-sip
- python-qt4

Once you have the above handled you'll want to pull in Richard Penman's "webscraping" library:

```
$ pip install webscraping
```

You will probably will want the ttf microsoft fonts for your flavor of UNIX, otherwise any
generated renderings aren't going to look so hot.

Finally you'll need to fire up a virtual framebuffer using xvfb. The application expects
said buffer on :1, so:

```
$ /usr/bin/Xvfb :1 -screen 0 1024x768x24 -extension RANDR -ac +extension GLX +render -noreset

```

## Usage

For a quick test with the command line, type:

```
$ curl --form file=@index.html http://hostname:port/screenshot > index.jpg
```

Several arguments are currently supported:

Return back an image limited by viewport

```
curl --form file=@index.html --form width=200 --form height=200 http://hostname:port/screenshot > index.jpg
```

More to come...

## TODO

* Add support for retrieving a remote URL
