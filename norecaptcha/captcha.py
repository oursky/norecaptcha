# -*- coding: utf-8 -*-
import urllib

try:
    import json
except ImportError:
    import simplejson as json

try:
    # test if it's Python 3
    from urllib.request import Request, urlopen
except:
    from urllib2 import Request, urlopen


VERIFY_SERVER = "www.google.com"


class RecaptchaResponse(object):

    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

    def __repr__(self):
        return "Recaptcha response: %s %s" % (
            self.is_valid, self.error_code)

    def __str__(self):
        return self.__repr__()


def displayhtml(site_key,
                language='',
                theme='light',
                fallback=False,
                d_type='image'):
    """
    Gets the HTML to display for reCAPTCHA

    site_key -- The site key
    language -- The language code for the widget.
    theme -- The color theme of the widget. `light` or `dark`
    fallback -- Old version recaptcha.
    d_type -- The type of CAPTCHA to serve. `image` or `audio`

    For more detail, refer to:
      - https://developers.google.com/recaptcha/docs/display
    """

    return """
<script
  src="https://www.google.com/recaptcha/api.js?hl\=%(LanguageCode)s"
  async="async" defer="defer"></script>
<div class="g-recaptcha"
  data-sitekey="%(SiteKey)s" data-theme="%(Theme)s" data-type="%(Type)s"></div>
<noscript>
  <div style="width: 302px; height: 352px;">
    <div style="width: 302px; height: 352px; position: relative;">
      <div style="width: 302px; height: 352px; position: absolute;">
        <iframe
          src="https://www.google.com/recaptcha/api/fallback?k=%(SiteKey)s&hl=%(LanguageCode)s"
          frameborder="0" scrolling="no"
          style="width: 302px; height:352px; border-style: none;">
        </iframe>
      </div>
      <div
        style="width: 250px; height: 80px; position: absolute;
               border-style: none; margin: 0px; padding: 0px;
               bottom: 21px; left: 25px;  right: 25px;">
            <textarea
              id="g-recaptcha-response" name="g-recaptcha-response"
              class="g-recaptcha-response"
              style="width: 250px; height: 80px; border: 1px solid #c1c1c1;
                     margin: 0px; padding: 0px; resize: none;"
              value=""></textarea>
      </div>
    </div>
  </div>
</noscript>
""" % {
        'LanguageCode': language,
        'SiteKey': site_key,
        'Theme': theme,
        'Type': d_type,
        'Fallback': fallback,
    }


def submit(recaptcha_response_field,
           secret_key,
           remoteip,
           verify_server=VERIFY_SERVER):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_response_field -- The value from the form
    secret_key -- your reCAPTCHA secret key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and len(recaptcha_response_field)):
        return RecaptchaResponse(
            is_valid=False,
            error_code='incorrect-captcha-sol'
        )

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
        'secret': encode_if_necessary(secret_key),
        'remoteip': encode_if_necessary(remoteip),
        'response': encode_if_necessary(recaptcha_response_field),
    })

    request = Request(
        url="https://%s/recaptcha/api/siteverify" % verify_server,
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "noReCAPTCHA Python"
        }
    )

    httpresp = urlopen(request)

    return_values = json.loads(httpresp.read())
    httpresp.close()

    return_code = return_values['success']
    error_codes = return_values.get('error-codes', [])

    if return_code:
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(
            is_valid=False,
            error_code=error_codes
        )
