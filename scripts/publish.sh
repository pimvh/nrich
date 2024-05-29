set -eo pipefail
# Make sure poetry's venv uses the configured python executable.
echo 'running poetry...'
poetry -v env use --no-interaction python3
poetry -v install --no-interaction

echo 'publishing package using poetry...'
poetry -v publish --build -u '__token__' -p $PIPY_API_TOKEN;
