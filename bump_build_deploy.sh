#!/bin/bash
# Jump to this directory so we can execute relative scripts
pushd "$(dirname "$0")"

# Use argument for bumpversion
if ! (bumpversion $1) &> /dev/null; then
    # handle error
    echo "Git working directory is not clean."
    popd
    exit 1
fi

# Build the distributions
python setup.py sdist bdist_wheel

# Upload tp PyPi
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Remove the builds locally
rm -r build/
rm -r dist/
rm -r PVGeo.egg-info/

popd
