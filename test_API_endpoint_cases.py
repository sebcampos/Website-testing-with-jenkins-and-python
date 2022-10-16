import requests
from Webpages import utils

UN = 'Sensi'
PWD = '1a7428Sensi420'
client = requests.session()


def setup_module(module):
    global api_logger
    api_logger = utils.set_up_logger("api_logger")


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    client.close()


def authenticate_session():
    login_url = f'https://thesensisociety.com/services/apiv1/authenticate?username={UN}&password={PWD}'
    r = client.get(login_url, headers={"Referer": "foo"}, verify=False)
    return r


def test_retrieve_api_token():
    r = authenticate_session()
    assert r.status_code == 200


def test_post():
    r = authenticate_session()
    print(r.headers)
    req = client.post("https://thesensisociety.com/services/apiv1/qrcode_endpoint/",
                      json={"test": 1},
                      headers={"Referer": "https://thesensisociety.com", "X-CSRFToken": r.cookies["csrftoken"]})
    api_logger.info(f"{req.content}")
    assert req.status_code == 200


def test_qrcode_endpoint():
    x = requests.post("https://thesensisociety.com/services/apiv1/qrcode_endpoint/", json={"test": 1}, verify=False)
    with open("x.html", "wb") as f:
        f.write(x.content)
    assert x.status_code == 200
