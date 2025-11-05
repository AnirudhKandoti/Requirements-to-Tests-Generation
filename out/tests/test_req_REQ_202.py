import requests


def test_req_202_createpet(base_url):
    url = base_url + "/pets"
    resp = requests.request("POST", url)
    assert resp.status_code == 200
