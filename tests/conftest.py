from .func.utils import drivers


def pytest_addoption(parser):
    parser.addoption("--browser", action="append", default=[],
                     help="List of webbrowsers to test (firefox, chrome)")


def pytest_generate_tests(metafunc):
    if 'webdriver' in metafunc.fixturenames:
        browsers = metafunc.config.getoption('browser')
        if not browsers:
            browsers = ['firefox', 'chrome']
        browsers = sorted(set(browsers))
        webdrivers = [drivers.get_driver(browser) for browser in browsers]
        metafunc.parametrize('webdriver', webdrivers)


def pytest_exception_interact(node, call, report):
    # import pdb; pdb.set_trace()
    if report.failed:
        # Retrieve test's browser logs through the webdriver
        s = '\n'.join(
            [line for line in node.funcargs['webdriver'].get_log('browser')]
        )
        if len(s) > 0:
            print('=== LOGS ===')
            print(s)


def pytest_sessionfinish(session, exitstatus):
    # Ensure all drivers are exited before we exit py.test
    drivers.release()
