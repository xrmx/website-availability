import json
import logging
from time import sleep

from kafka import KafkaProducer

from wava.checker.exceptions import CheckerNetworkError

logger = logging.getLogger()


def loop(config, check, cleanup):
    """Main loop of the program that will execute the checker

    It takes three parameters:
    - the config, parsed by the cli
    - a check function, to do the actual availability checking
    - a cleanup function, to do the cleanup at exit

    The loop is agnostic of the actual checker implementation."""

    producer = KafkaProducer(
        bootstrap_servers=config["kafka_brokers"],
        security_protocol="SSL",
        ssl_cafile=config["kafka_ssl_cafile"],
        ssl_certfile=config["kafka_ssl_certfile"],
        ssl_keyfile=config["kafka_ssl_keyfile"],
    )
    interval = config["interval"]
    try:
        # TODO: catch signals
        while True:
            try:
                response = check(config)
            except CheckerNetworkError as e:
                logger.error(
                    "Network error: {}".format(str(e.checker_original_exception))
                )
            else:
                # FIXME: verbosity should handle default logger value
                if config["verbosity"]:
                    logger.info("response: {}".format(str(response)))

                serialized = json.dumps(response)
                producer.send(config["kafka_topic"], serialized.encode("utf-8"))
                producer.flush()

            sleep(interval)
    except KeyboardInterrupt:
        cleanup(config, producer)
