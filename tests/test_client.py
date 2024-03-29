def test_get(requests_mock, cico):
    expected_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'python-cicoclient',
    }
    requests_mock.get('http://api.example.com/', request_headers=expected_headers, json={'status': 'OK'})
    resp, body = cico.get('/')
    assert body == {'status': 'OK'}

def test_get_string_body(requests_mock, cico):
    requests_mock.get('http://api.example.com/', json="Failed to allocate nodes")
    resp, body = cico.get('/')
    assert body == "Failed to allocate nodes"

def test_get_bad_body(requests_mock, cico):
    requests_mock.get('http://api.example.com/', text="Invalid JSON")
    resp, body = cico.get('/')
    assert body is None
