from cicoclient import cli

def test_inventory(inventory_mock, app_mock, mocker):
    test_lister = cli.Inventory(app_mock, [])

    parsed_args = mocker.Mock()
    parsed_args.columns = ('host_id', 'hostname', 'ip_address')
    parsed_args.formatter = 'table'
    parsed_args.sort_columns = []
    parsed_args.print_empty = False
    parsed_args.max_width = 80

    test_lister.run(parsed_args)

def test_node_get(inventory_mock, app_mock, requests_mock, mocker):
    requests_mock.get('http://api.example.com/Node/get', json={'hosts':['n1.hufty'], 'ssid': 'deadtest'})

    test_lister = cli.NodeGet(app_mock, [])

    parsed_args = mocker.Mock()
    parsed_args.columns = ('host_id', 'hostname', 'ip_address')
    parsed_args.formatter = 'table'
    parsed_args.sort_columns = []
    parsed_args.print_empty = False
    parsed_args.max_width = 80

    test_lister.run(parsed_args)

def test_node_done(inventory_mock, app_mock, requests_mock, mocker):
    requests_mock.get('http://api.example.com/Node/done')

    test_lister = cli.NodeDone(app_mock, [])

    parsed_args = mocker.Mock()
    parsed_args.columns = ('host_id', 'hostname', 'ip_address')
    parsed_args.formatter = 'table'
    parsed_args.sort_columns = []
    parsed_args.print_empty = False
    parsed_args.max_width = 80

    test_lister.run(parsed_args)
