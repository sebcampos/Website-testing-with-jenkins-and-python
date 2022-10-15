import requests

admin_url= 'https://thesensisociety.com/services/automation/admin/'
admin_post_url= 'https://thesensisociety.com/services/automation/admin/login/?next=/admin/'

UN='Sensi'
PWD='1a7428Sensi420'
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
    client.close()

def post_test():
    client.post("https://thesensisociety.com/services/apiv1/qrcode_endpoint/", data={"TEST_POST"}, headers=headers)


