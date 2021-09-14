rm -rf dist
python setup.py sdist
twine upload --repository testpypi dist/* || exit 
twine upload dist/*
