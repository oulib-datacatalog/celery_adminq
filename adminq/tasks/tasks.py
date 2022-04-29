from celery import Celery
from subprocess import check_call, CalledProcessError
import logging

logging.basicConfig(level=logging.INFO)

try:
    import celeryconfig
except ImportError:
    logging.error('Failed to import celeryconfig - exiting!')
    exit()

app = Celery()
app.config_from_object(celeryconfig)


def _call_systemctl(action, service):
    if action not in ["start", "stop", "restart"]:
        return {"ERROR": "Unsupported action: %s" % action} 
    if service not in ["oulib-celery-workerq", "oulib-celery-workerq-installer"]:
        return {"ERROR": "Unkown service: %s" % service} 
    try:
        check_call(["sudo", "/usr/bin/systemctl", action, service])
    except CalledProcessError as err:
        logging.error(err)
        return {"ERROR": err} 
    return {"status": "SUCCESS"}


@app.task()
def startworker(reinstall=False):
    if reinstall:
        _call_systemctl("start", "oulib-celery-workerq-installer")
    _call_systemctl("start", "oulib-celery-workerq")


@app.task()
def stopworker():
    _call_systemctl("stop", "oulib-celery-workerq")


@app.task()
def restartworker(reinstall=False):
    if reinstall:
        _call_systemctl("start", "oulib-celery-workerq-installer")
    _call_systemctl("restart", "oulib-celery-workerq")

