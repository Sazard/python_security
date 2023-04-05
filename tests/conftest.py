import pytest

def pytest_addoption(parser):
    parser.addoption('--ip', default='192.168.56.1', help='Host IP address')
    parser.addoption('--netmask', default='24', help='Subnet mask')
    parser.addoption('--single-ip', help='Single IP address to scan')
    parser.addoption('--output-format', choices=['json', 'csv', 'html'], default='html', help='Output format')
    parser.addoption('--analyse', help='Analyse network traffic')

@pytest.fixture(scope='session')
def ip(request):
    return request.config.getoption('--ip')

@pytest.fixture(scope='session')
def netmask(request):
    return request.config.getoption('--netmask')

@pytest.fixture(scope='session')
def single_ip(request):
    return request.config.getoption('--single-ip')

@pytest.fixture(scope='session')
def output_format(request):
    return request.config.getoption('--output-format')

@pytest.fixture(scope='session')
def analyse(request):
    return request.config.getoption('--analyse')