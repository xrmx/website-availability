def parse_common_kafka_args(parser):
    """This is an helper to share kafka configuration between different tools

    Takes an argparse.ArgumentParser"""

    # Kafka configuration from:
    # https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
    parser.add_argument(
        "--kafka-broker",
        help="Kafka broker host:port pair",
        nargs="+",
        default="kafka-wava-d538bd8-riccardo-ae5f.aivencloud.com:27652",
    )
    parser.add_argument("--kafka-topic", help="Kafka topic", default="test")
    parser.add_argument(
        "--kafka-ssl-cafile", help="Kafka CA certificate", default="ca.pem"
    )
    parser.add_argument(
        "--kafka-ssl-certfile", help="Kafka access certificate", default="service.cert"
    )
    parser.add_argument(
        "--kafka-ssl-keyfile", help="Kafka access key", default="service.key"
    )
