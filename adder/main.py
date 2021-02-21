import click
from loguru import logger

from adder.adder import add_all

from .config import cfg


@click.command()
@click.option("--number-a", required=True, type=int)
@click.option("--number-b", default=cfg.default_number_b, type=int)
def main(number_a, number_b):
    """sample adder"""
    logger.debug("number a = {}", number_a)
    logger.debug("number b = {}", number_b)
    click.echo(add_all(number_a, number_b))
