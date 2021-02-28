import logging
from time import sleep

from wava.checker.exceptions import CheckerNetworkError

logger = logging.getLogger()


def loop(config, check, cleanup):
    """Main loop of the program that will execute the checker"""

    interval = config["interval"]
    try:
        # TODO: catch signals
        while True:
            try:
                response = check(config)
            except CheckerNetworkError as e:
                logger.error("Network error:".format(str(e.checker_original_exception)))
            else:
                if config["verbosity"]:
                    logger.info("response: {}".format(str(response)))
            sleep(interval)
    except KeyboardInterrupt:
        cleanup(config)
