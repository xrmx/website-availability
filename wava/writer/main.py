import json
import logging

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from wava.writer.exceptions import WriterError

logger = logging.getLogger()


def loop(config, write, cleanup):
    """Main loop of the program that will write checker output to database"""

    # kafka tips from: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
    consumer = KafkaConsumer(
        config["kafka_topic"],
        bootstrap_servers=config["kafka_brokers"],
        security_protocol="SSL",
        group_id=config["kafka_group_id"],
        ssl_cafile=config["kafka_ssl_cafile"],
        ssl_certfile=config["kafka_ssl_certfile"],
        ssl_keyfile=config["kafka_ssl_keyfile"],
    )
    try:
        # TODO: catch signals
        while True:
            try:
                records = consumer.poll(config["kafka_poll_timeout"])
            except KafkaError as e:
                logger.error(
                    "Network error: {}".format(str(e.writer_original_exception))
                )
            else:
                for record in records:
                    logger.debug("record: {}".format(str(record.value)))
                    try:
                        payload = json.loads(record.value.decode("utf-8"))
                        write(config, payload)
                    except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                        logger.error("dropped invalid record: {}".format(record.value))
                        continue
                    except WriterError as e:
                        logger.error("write failure: {}".format(str(e.original_value)))

                consumer.commit()
    except KeyboardInterrupt:
        cleanup(config, consumer)