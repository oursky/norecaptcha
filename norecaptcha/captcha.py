from json import loads
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen


VERIFY_SERVER = "www.google.com"


class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

    def __repr__(self):
        return "Recaptcha response: %s %s" % (self.is_valid, self.error_code)

    def __str__(self):
        return self.__repr__()


def displayhtml(
    site_key, language="", theme="light", fallback=False, d_type="image", size="normal"
):
    """
    Gets the HTML to display for reCAPTCHA

    site_key -- The site key
    language -- The language code for the widget.
    theme -- The color theme of the widget. `light` or `dark`
    fallback -- Old version recaptcha.
    d_type -- The type of CAPTCHA to serve. `image` or `audio`
    size -- The size of the dispalyed CAPTCHA, 'normal' or 'compact'

    For more detail, refer to:
      - https://developers.google.com/recaptcha/docs/display
    """

    return """
<script
  src="https://www.google.com/recaptcha/api.js?hl=%(LanguageCode)s&fallback=%(Fallback)s&"
  async="async" defer="defer"></script>
<div class="g-recaptcha"
    data-sitekey="%(SiteKey)s"
    data-theme="%(Theme)s"
    data-type="%(Type)s"
    data-size="%(Size)s">
</div>
<noscript>
  <div  style="width: 302px; height: 480px;">
    <div style="width: 302px; height: 422px; position: relative;">
      <div style="width: 302px; height: 422px; position: relative;">
        <iframe
          src="https://www.google.com/recaptcha/api/fallback?k=%(SiteKey)s&hl=%(LanguageCode)s"
          frameborder="0" scrolling="no"
          style="width: 302px; height:422px; border-style: none;">
        </iframe>
      </div>
      <div
        style="border-style: none; bottom: 12px; left: 25px;
               margin: 0px; padding: 0px; right: 25px;
               background: #f9f9f9; border: 1px solid #c1c1c1;
               border-radius: 3px; height: 60px; width: 300px;">
            <textarea
              id="g-recaptcha-response" name="g-recaptcha-response"
              class="g-recaptcha-response"
              style="width: 250px; height: 40px; border: 1px solid #c1c1c1;
                     margin: 10px 25px; padding: 0px; resize: none;"
              value=""></textarea>
      </div>
    </div>
  </div>
</noscript>
""" % {
        "LanguageCode": language,
        "SiteKey": site_key,
        "Theme": theme,
        "Type": d_type,
        "Size": size,
        "Fallback": fallback,
    }


def submit(recaptcha_response_field, secret_key, remoteip, verify_server=VERIFY_SERVER):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_response_field -- The value from the form
    secret_key -- your reCAPTCHA secret key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and len(recaptcha_response_field)):
        return RecaptchaResponse(is_valid=False, error_code="incorrect-captcha-sol")

    params = urlencode(
        {
            "secret": secret_key,
            "remoteip": remoteip,
            "response": recaptcha_response_field,
        }
    ).encode()

    request = Request(
        url="https://%s/recaptcha/api/siteverify" % verify_server,
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "noReCAPTCHA Python",
        },
    )

    httpresp = urlopen(request)

    return_values = loads(httpresp.read())
    httpresp.close()

    return_code = return_values["success"]
    error_codes = return_values.get("error-codes", [])

    if return_code:
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False, error_code=error_codes)
