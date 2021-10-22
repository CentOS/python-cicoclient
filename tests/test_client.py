from cicoclient import client

def test_get(requests_mock):
    expected_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'python-cicoclient',
    }
    cico = client.CicoClient(endpoint='http://api.example.com')
    requests_mock.get('http://api.example.com/', request_headers=expected_headers, json={'status': 'OK'})
    resp, body = cico.get('/')
    assert body == {'status': 'OK'}
