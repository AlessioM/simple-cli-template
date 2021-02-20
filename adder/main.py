import click
from loguru import logger


@click.command()
@click.option("--number-a", required=True, type=int)
@click.option("--number-b", required=True, type=int)
def main(number_a, number_b):
    """sample adder"""
    logger.debug("number a = {}", number_a)
    logger.debug("number b = {}", number_b)
    print(number_a + number_b)
