import click
from loguru import logger

from adder.adder import add_all

from .config import cfg


def process(*numbers: int) -> int:
    """performs the requested calculation"""
    return add_all(*numbers)


@click.command()
@click.option("--number-a", required=True, type=int)
@click.option("--number-b", default=cfg.default_number_b, type=int)
def command_line(number_a: int, number_b: int) -> None:
    """adds two numbers together"""
    logger.debug("number a = {}", number_a)
    logger.debug("number b = {}", number_b)
    click.echo(process(number_a, number_b))
