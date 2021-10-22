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

@pytest.fixture
def inventory_mock(requests_mock):
    return requests_mock.get('http://api.example.com/Inventory', json=_FAKE_INVENTORY)

def test_full_inventory(cicowrapper, inventory_mock):
    assert cicowrapper.full_inventory
    assert 'n1.hufty' in cicowrapper.full_inventory
    assert cicowrapper.full_inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_self_inventory(cicowrapper, inventory_mock):
    assert cicowrapper.self_inventory
    assert 'n1.hufty' in cicowrapper.self_inventory
    assert cicowrapper.self_inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_inventory(cicowrapper, inventory_mock):
    inventory = cicowrapper.inventory()
    assert inventory
    assert 'n1.hufty' in inventory
    assert inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_inventory_with_ssid(cicowrapper, inventory_mock):
    inventory = cicowrapper.inventory(ssid='83fba182')
    assert inventory
    assert 'n1.hufty' in inventory
    assert inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_inventory_with_nonexisting_ssid(cicowrapper, inventory_mock):
    inventory = cicowrapper.inventory(ssid='deaddead')
    assert inventory == {}

def test_node_get(cicowrapper, requests_mock, inventory_mock):
    requests_mock.get('http://api.example.com/Node/get?key=dummy_key&arch=x86_64', json={'hosts':['n1.hufty'], 'ssid': 'deadtest'})
    inventory, ssid = cicowrapper.node_get(arch='x86_64')
    assert ssid == 'deadtest'
    assert inventory
    assert 'n1.hufty' in inventory
    assert inventory['n1.hufty']['ip_address'] == "172.19.3.1"

def test_node_done(cicowrapper, requests_mock, inventory_mock):
    requests_mock.get('http://api.example.com/Node/done?key=dummy_key&ssid=deadtest')
    cicowrapper.node_done(ssid='deadtest')
