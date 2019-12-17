
check:
	pylint3 --errors-only --output-format=parseable hackforum/*.py hackforum/tests/*.py
	


run_dev:
	ls hackforum/*.py hackforum/views/*.tpl | entr -dr python3 hackforum/main.py
