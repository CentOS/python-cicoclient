from cicoclient import client, wrapper

import pytest

_FAKE_INVENTORY = [
  [
    1,
    "n1.hufty",
    "172.19.3.1",
    "hufty",
    351,
    "Disabled",
    "83fba182",
    None,
    None,
    "7",
    "x86_64",
    1,
    2000,
    None
  ]
]

@pytest.fixture
def cico():
    return client.CicoClient(endpoint='http://api.example.com')

@pytest.fixture
def cicowrapper():
    return wrapper.CicoWrapper(endpoint='http://api.example.com/', api_key='dummy_key')

@pytest.fixture
def inventory_mock(requests_mock):
    return requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)
