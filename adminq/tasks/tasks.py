from celery.task import task
from subprocess import call, check_call, CalledProcessError
import logging

logging.basicConfig(level=logging.INFO)


def _call_systemctl(action):
    if action in ['start', 'stop', 'restart']:
        #try:
        call(["sudo", "/usr/bin/systemctl", action, "oulib-celery-workerq"])
        #except CalledProcessError as err:
        #    logging.error(err)
        #    return({"ERROR": err})
        #return("SUCCESS")
    else:
        return({"ERROR": "Unsupported action"})


@task()
def startworker():
    _call_systemctl("start")


@task()
def stopworker():
    _call_systemctl("stop")


@task()
def restartworker():
    _call_systemctl("restart")
