import requests
from Webpages import utils

admin_url = 'https://thesensisociety.com/services/automation/admin/'
admin_post_url = 'https://thesensisociety.com/services/automation/admin/login/?next=/admin/'

UN = 'Sensi'
PWD = '1a7428Sensi420'
client = requests.session()

# Retrieve the CSRF token first
client.get(admin_url, verify=False)  # sets the cookie
csrftoken = client.cookies['csrftoken']
login_data = dict(username=UN, password=PWD, csrfmiddlewaretoken=csrftoken)
r = client.post(admin_post_url, data=login_data, headers={"Referer": "foo"}, verify=False)
headers = {"Referer": "foo", "X-csrftoken": csrftoken}


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    global api_logger
    api_logger = utils.set_up_logger("api_logger")
    client.close()


def test_post():
    req = client.post("https://thesensisociety.com/services/apiv1/qrcode_endpoint/", data={"TEST_POST": 1}, headers=headers)
    api_logger.info(f"{req.content}")
    assert r.status_code == 200

