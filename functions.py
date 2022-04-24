import json
import logging
import sys


def get(product, environment=None):
    path = "./creds.json"
    infile = open(path, "r").read()
    credsjson = json.loads(infile)
    if not environment:
        return credsjson[product]
    else:
        for i in credsjson[product]:
            if i['environment'] == environment:
                return i
            else:
                pass



#Prep Logging
DEBUG = False
if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(LOG_LEVEL)
formatter = logging.Formatter("| %(filename)s:%(lineno)s | %(levelname)-6s | %(funcName)-13s| %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info("Logging init...")


def httpcheckandreturn(res):
    if res.status_code != 200:
        if res.status_code == 403:
            logger.error(res.json()['message'])
            return
        else:
            logger.info("controller login failed with http " + str(res.status_code))
            logger.info(res.json())
    else:
        logger.info("Authentication successful")
#        print(json.dumps(json.loads(res.text), indent=2))
        return res.json()

