# Installing private dependancies from GITHUB using provided GITHUB_TOKEN
$CONDA_ENV_BIN_PATH"/pip" install --upgrade pip
$CONDA_ENV_BIN_PATH"/pip" install --upgrade setuptools
$CONDA_ENV_BIN_PATH"/pip" install --upgrade wheel

# University Scheduler
$CONDA_ENV_BIN_PATH"/pip" install git+https://${GITHUB_ID}:${GITHUB_TOKEN}@github.com/lcharleux/automatic_university_scheduler.git
