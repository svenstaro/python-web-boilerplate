default:
	pyvenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt --upgrade

clean:
	rm -rf venv
