import urllib, json

try:
    # test if it's Python 3
    from urllib.request import Request, urlopen
except:
    from urllib2 import Request, urlopen


VERIFY_SERVER="www.google.com"

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

    def __repr__(self):
        return "Recaptcha response: %s %s"%(
            self.is_valid, self.error_code)

    def __str__(self):
        return self.__repr__()

def displayhtml (site_key, language=''):
    """Gets the HTML to display for reCAPTCHA

    site_key -- The site key
    language -- The language code for the widget.
    """

    return """<script src="https://www.google.com/recaptcha/api.js?hl=%(LanguageCode)s" async defer></script>
      <div class="g-recaptcha" data-sitekey="%(SiteKey)s"></div>
""" % {
        'LanguageCode': language,
        'SiteKey' : site_key,
        }

def submit (recaptcha_response_field,
            secret_key,
            remoteip,
            verify_server=VERIFY_SERVER):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_response_field -- The value of recaptcha_response_field from the form
    secret_key -- your reCAPTCHA secret key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and len (recaptcha_response_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode ({
            'secret': encode_if_necessary(secret_key),
            'remoteip' :  encode_if_necessary(remoteip),
            'response' :  encode_if_necessary(recaptcha_response_field),
            })

    request = Request (
        url = "https://%s/recaptcha/api/siteverify" % verify_server,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    httpresp = urlopen (request)

    return_values = json.loads(httpresp.read())
    httpresp.close()

    return_code = return_values['success']

    if return_code:
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values['error-codes'])
