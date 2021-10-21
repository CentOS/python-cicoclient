from cicoclient import wrapper

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
def cicowrapper():
    return wrapper.CicoWrapper(endpoint='http://api.example.com/', api_key='dummy_key')

def test_full_inventory(cicowrapper, requests_mock):
    requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)
    assert cicowrapper.full_inventory
    assert 'n1.hufty' in cicowrapper.full_inventory
    assert cicowrapper.full_inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_self_inventory(cicowrapper, requests_mock):
    requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)
    assert cicowrapper.self_inventory
    assert 'n1.hufty' in cicowrapper.self_inventory
    assert cicowrapper.self_inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_inventory(cicowrapper, requests_mock):
    requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)
    inventory = cicowrapper.inventory()
    assert inventory
    assert 'n1.hufty' in inventory
    assert inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_inventory_with_ssid(cicowrapper, requests_mock):
    requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)
    inventory = cicowrapper.inventory(ssid='83fba182')
    assert inventory
    assert 'n1.hufty' in inventory
    assert inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_inventory_with_nonexisting_ssid(cicowrapper, requests_mock):
    requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)
    inventory = cicowrapper.inventory(ssid='deaddead')
    assert inventory == {}
