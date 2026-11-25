.PHONY: rundev runmock runprod venv envrun

rundev:
	bash rundev.sh

runmock:
	bash runmock.sh

runprod:
	tmux new -s gunicorn "bash runprod.sh"

venv:
	test -x ../apivenv/bin/python || python3 -m venv ../apivenv

envrun: venv
	tmux new-session -d -s lookmix-api -n rundev
	tmux send-keys -t lookmix-api:rundev 'make rundev' C-m
	tmux new-window -d -t lookmix-api -n runmock
	tmux send-keys -t lookmix-api:runmock 'make runmock' C-m
	tmux attach-session -t lookmix-api