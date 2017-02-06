#!/bin/bash
 
NAME="musicassist"
APPDIR=/opt/web/prod/assist.frequencies.audio
SOCKFILE=/opt/web/prod/assist.frequencies.audio/sock/gunicorn.sock
USER=www
GROUP=www
NUM_WORKERS=2
WSGI_MODULE=wsgi
VIRTUAL_ENV_PATH=/opt/web/prod/assist.frequencies.audio/venv/bin/
 
echo "Starting ${NAME}"
 
# Activate the virtual environment
cd ${APPDIR}
source ${VIRTUAL_ENV_PATH}activate
export PYTHONPATH=${APPDIR}:${PYTHONPATH}
 
# Create the run directory if it doesn't exist
RUNDIR=$(dirname ${SOCKFILE})
test -d ${RUNDIR} || mkdir -p ${RUNDIR}
 
exec ${VIRTUAL_ENV_PATH}gunicorn ${WSGI_MODULE}:app \
--name ${NAME} \
--workers ${NUM_WORKERS} \
--user=${USER} --group=${GROUP} \
--log-level=info \
--bind=unix:${SOCKFILE}
