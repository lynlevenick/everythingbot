import json
import logging
import re
import subscriber
import traceback
import urllib

# TODO: Should we support a generic 'website response' class? This is becoming a pattern

url_res = [
    "gfycat\\.com/([A-Za-z]+)"
]

def format_size(n):
    if n > 2 ** 20:
        return "%.2f MB" % (n / (2 ** 20))
    elif n > 2 ** 10:
        return "%.2f KB" % (n / (2 ** 10))
    else:
        return "%.2f B" % n

class Gfycatinfo(subscriber.Subscriber):
    def __init__(self, config):
        self.cache = {}
        self.ignored_users = config["ignored_users"]

    def on_add(self, publisher):
        self.publisher = publisher

    def message(self, kind, *args):
        if kind == 'pubmsg':
            nick = args[1].source.nick
            text = args[1].arguments[0]

            if not nick in self.ignored_users:
                for url_re in url_res:
                    for match in re.finditer(url_re, text):
                        gfycat_id = match.group(1)
                        title = None
                        size = None

                        logging.info("Gfycat ID=%s found in text" % gfycat_id)

                        if gfycat_id in self.cache:
                            logging.info("Already in cache")
                            title = self.cache[gfycat_id][0]
                            size = self.cache[gfycat_id][1]
                        else:
                            logging.info("Not in cache; Hitting gfycat.com")

                            try:
                                resp = urllib.urlopen("http://gfycat.com/cajax/get/%s" % gfycat_id)
                                data = json.load(resp)
                                title = unicode(data["gfyItem"]["title"] or data["gfyItem"]["uploadGifName"] or "Untitled")
                                size = format_size(min(data["gfyItem"]["gifSize"] or float("inf"), data["gfyItem"]["mp4Size"] or float("inf"), data["gfyItem"]["webmSize"] or float("int")))
                                self.cache[gfycat_id] = (title, size)
                            except Exception as e:
                                # TODO: Python 2/3 compat here
                                logging.info("Failed: %s: %s" % (e, traceback.format_exc()))
                                self.publisher.parent.say("Linked Gfycat not found.")

                        if title and size:
                            self.publisher.parent.say(u"Linked Gfycat: \"%s\", %s" % (title, size))
