from cicoclient import exceptions

import pytest

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

def test_node_get_no_body(cicowrapper, requests_mock, inventory_mock):
    requests_mock.get('http://api.example.com/Node/get?key=dummy_key&arch=x86_64')
    with pytest.raises(exceptions.NoInventory) as excinfo:
        cicowrapper.node_get(arch='x86_64', retry_interval=1)
    assert str(excinfo.value) == "The requested operation failed as no inventory is available."

def test_node_get_error(cicowrapper, requests_mock, inventory_mock):
    requests_mock.get('http://api.example.com/Node/get?key=dummy_key&arch=x86_64', json="Failed to allocate nodes")
    with pytest.raises(ValueError) as excinfo:
        cicowrapper.node_get(arch='x86_64')
    assert str(excinfo.value) == "Failed to allocate nodes"

def test_node_done(cicowrapper, requests_mock, inventory_mock):
    requests_mock.get('http://api.example.com/Node/done?key=dummy_key&ssid=deadtest')
    cicowrapper.node_done(ssid='deadtest')

def test_node_done_without_ssid(cicowrapper, requests_mock, inventory_mock):
    requests_mock.get('http://api.example.com/Node/done?key=dummy_key')
    with pytest.raises(exceptions.SsidRequired) as excinfo:
        cicowrapper.node_done()
    assert str(excinfo.value) == "The requested operation requires a SSID."
