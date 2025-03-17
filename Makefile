build:
	@echo "No build required for Python"

run-server:
	python3 server.py

run-client:
	python3 client.py

clean:
	rm -f server_logs.txt
	rm -rf __pycache__
