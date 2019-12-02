coverage run --rcfile=.coverage_config test/test_unit.py && coverage run --rcfile=.coverage_config -a test/test_server.py
coverage html && coverage report
