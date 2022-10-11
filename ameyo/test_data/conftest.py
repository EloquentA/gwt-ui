__author__ = "Developed by EA"

import os
import pytest


def pytest_addoption(parser):
    """
    Adds custom command line options for running the pytest harness
    All options will be stored in pytest config
    :param parser:
    :return:
    """
    parser.addoption("--processes", action="store", type=int, default=10, help="Number of Processes")
    parser.addoption("--agents", action="store", type=int, default=50, help="Number of Agents")
    parser.addoption("--leads", action="store", type=int, default=10, help="Number of (leads)")
    parser.addoption("--customers", action="store", type=int, default=10, help="Number of Customers (leads)")
    parser.addoption("--calls", action="store", type=int, default=1, help="Number of Calls")
    parser.addoption("--cxn", action="store", default='customer_success_60_DefaultVR', help="Call Context Name")


def pytest_sessionstart(session):
    """
    Runs at the Start of execution
    :param session:
    :return:
    """
    os.environ.update({'CALL_COUNTS': str(session.config.option.calls)})


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    """
    Here we skip the test-cases at the very beginning !!
    :param config:
    :param items:
    :return:
    """
    allowedcxn = ["customer_success_60_DefaultVR", "customer_success_1800_DefaultVR"]
    markersToSkip = [
        "CALL_TRANSFER_TO_CAMPAIGN", "CALL_TRANSFER_TO_PHONE", "CALL_TRANSFER_TO_USER", "CALL_TRANSFER_TO_QUEUE"
    ]
    for item in items:
        for markerToSkip in markersToSkip:
            if config.option.cxn not in allowedcxn and item.get_closest_marker(markerToSkip):
                item.add_marker(pytest.mark.skip('Skipped Test Case without Customer Success :)'))


def pytest_generate_tests(metafunc):
    """
    Modify Test-Cases
    :param metafunc:
    :return:
    """
    # Iterate over Class Markers
    for _marker in metafunc.cls.pytestmark:
        pass

    # Iterate over Function Markers
    for _marker in metafunc.definition.own_markers:
        if _marker.name in ['CREATE_PROCESS']:
            metafunc.parametrize("pn", [f"PROCESS_{i:04}" for i in range(1, metafunc.config.option.processes + 1)])
            break
