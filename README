# wava

wava is a website availability checker. It's mostly a toy implementation :)

## Architecture

wava use Kafka for communicating and PostgreSQL to store its results.

wava consists of two programs: wavacheck and wavawrite. wavacheck checks the availability of an URL
via HTTP at a fixed interval, wavawrite writes the output to the PostgreSQL database.

## Installation

wava is written in Python 3.

wava is not publishead on Pypi, you should install it from a checkout of this repository with the following command:

```
pip install -e .
```

Better install it on a local virtual environment

## Configuration

Only authentications with certificates is supported for Kafka.

See wavacheck and wavawrite help for details.

## Development

### Local configuration

[pre-commit](https://pre-commit.com/) is used to check changes before a commit. Once you have installed it you can setup it with:

```
pre-commit install
```

### Running tests

Tests are written in pytest. You can run tests with:

```
python setup.py test
```

Some tests require a PostgreSQL instance already running, you can find `postgres/docker-compose.yml` handy.

You can skip these PostgreSQL integration tests with `pytest -m "not postgres"`. Please note you can use pytest after setting up requirements with the `python setup.py test` command.


## Fun facts

Developing this program [one pull request](https://github.com/kvesteri/validators/pull/186) was contributed to one of wava dependencies.
