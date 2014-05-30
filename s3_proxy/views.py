import urlparse
import requests

from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import redirect

from .utils import get_headers


EXCLUDED_HEADERS = set([
  # Hop-by-hop headers
  # ------------------
  # Certain response headers should NOT be just tunneled through.  These
  # are they.  For more info, see:
  # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
  'connection', 'keep-alive', 'proxy-authenticate',
  'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
  'upgrade',

  # Although content-encoding is not listed among the hop-by-hop headers,
  # it can cause trouble as well.  Just let the server set the value as
  # it should be.
  'content-encoding',

  # Since the remote server may or may not have sent the content in the
  # same encoding as Django will, let Django worry about what the length
  # should be.
  'content-length',
])


class S3ProxyView(object):
  """
  Forward as close to an exact copy of the request as possible along to the
  given url.  Respond with as close to an exact copy of the resulting
  response as possible.

  If there are any additional arguments you wish to send to requests, put
  them in the args dictionary.
  """
  def __init__(self, bucket, region='us-west-1', protocol='http'):
    self.url = '{}://{}.s3-website-{}.amazonaws.com'.format(
      protocol,
      bucket,
      region
    )

  def as_view(self, index='index.html'):
    index_url = urlparse.urljoin(self.url, index)

    def _view(request, url, args=None):
      if url:
        # we only need to create a proxy response if the endpoint requested is
        # not the index document. just return a redirect to the asset, as browsers
        # will follow redirects for Javascript + CSS files
        return redirect(
          urlparse.urljoin(self.url, url)
        )

      args = (args or {}).copy()
      headers = get_headers(request.META)
      params = request.GET.copy()

      args['headers'] = args.get('headers', {})
      args['data'] = args.get('data', request.body)
      args['params'] = args.get('params', QueryDict('', mutable=True))

      # Overwrite any headers and params from the incoming request with explicitly
      # specified values for the requests library.
      headers.update(args['headers'])
      params.update(args['params'])

      # If there's a content-length header from Django, it's probably in all-caps
      # and requests might not notice it, so just remove it.
      for key in headers.keys():
        if key.lower() == 'content-length':
          del headers[key]

      args['headers'] = headers
      args['params'] = params

      response = requests.request(
        request.method,
        urlparse.urljoin(self.url, index_url),
        **args
      )

      proxy_response = HttpResponse(
        response.content,
        status=response.status_code
      )

      for key, value in response.headers.iteritems():
        if key.lower() in EXCLUDED_HEADERS:
          continue
        proxy_response[key] = value

      return proxy_response

    return _view
