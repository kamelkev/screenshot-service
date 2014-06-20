# ss

Screenshot Service - simplistic http based web service powered by Python and WebKit

## Purpose

This is a work in progress, right now this service will accept a submitted html file
and return back a rendering of said html through webkit. Moving forward the seemingly
straightforward step of rendering a remote url will also be added.

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

Additionally you probably will want the ttf microsoft fonts for your flavor of UNIX, otherwise
any generated renderings aren't going to look so hot.

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

* Add support for specifying returned image type and quality level (for jpg)
* Add support for retrieving a remote URL
