import requests


def test_req_101_listpets(base_url):
    url = base_url + "/pets"
    resp = requests.request("GET", url)
    assert resp.status_code == 200

def test_req_101_getpet(base_url):
    url = base_url + "/pets/{petId}"
    resp = requests.request("GET", url)
    assert resp.status_code == 200
