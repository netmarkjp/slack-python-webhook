# -*- coding: utf-8 -*-


# 3rd party library
try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
    import urllib.request as urlrequest
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode
    import urllib2 as urlrequest
import json
import time


class Slack():

    def __init__(self, url="", retry_max_count=3, retry_after_default=1):
        self.url = url
        self.opener = urlrequest.build_opener(urlrequest.HTTPHandler())
        self.retry_max_count = retry_max_count
        self.retry_after_default = retry_after_default  # in second

    def notify(self, **kwargs):
        """
        Send message to slack API
        """
        return self.send(kwargs)

    def send(self, payload, retry_times=0):
        """
        Send payload to slack API
        """
        payload_json = json.dumps(payload)
        data = urlencode({"payload": payload_json})
        req = urlrequest.Request(self.url)
        response = self.opener.open(req, data.encode('utf-8'))
        print(dir(response))
        if response.code == 200:
            if retry_times >= self.retry_max_count:
                raise Exception("retry over")
            retry_after = self.retry_after_default
            for header in response.headers:
                if header[0] == "Retry-After":
                    retry_after = int(header[1])
            time.sleep(retry_after)
            return self.send(payload, retry_times=retry_times+1)

        return response.read().decode('utf-8')
