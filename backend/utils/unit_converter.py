from decimal import Decimal
from typing import Tuple

CONVERSION_MAP = {
    ("grama", "kg"): Decimal('1000'),
    ("grama", "grama"): Decimal('1'),
    ("mililitro", "litro"): Decimal('1000'),
    ("mililitro", "mililitro"): Decimal('1'),
    ("unidade", "unidade"): Decimal('1'),
    ("unidade", "pacote"): Decimal('1'),
    ("unidade", "duzia"): Decimal('12'),
    ("kg", "kg"): Decimal('1'),
    ("litro", "litro"): Decimal('1'),
}


def get_conversion_factor(measure_unity: str, price_unit: str) -> Decimal:
    """
    Retorna o fator de conversão entre a unidade de medida do estoque
    e a unidade de preço

    Args:
        measure_unity: Unidade de medida do estoque (ex: 'grama', 'mililitro')
        price_unit: Unidade do preço (ex: 'kg', 'litro')

    Returns:
        Fator de conversão como Decimal
    """
    key = (measure_unity.lower(), price_unit.lower())
    factor = CONVERSION_MAP.get(key)

    if factor is None:
        return Decimal('1')

    return factor


def calculate_item_total_value(amount: Decimal, price: Decimal, measure_unity: str, price_unit: str) -> Decimal:
    """
    Calcula o valor total de um item considerando conversão de unidades

    Args:
        amount: Quantidade em estoque
        price: Preço por unidade de price_unit
        measure_unity: Unidade de medida do estoque
        price_unit: Unidade do preço

    Returns:
        Valor total como Decimal
    """
    factor = get_conversion_factor(measure_unity, price_unit)
    return (amount / factor) * price


def calculate_unit_price(price: Decimal, price_unit: str, target_unit: str) -> Decimal:
    """
    Converte o preço de uma unidade para outra

    Args:
        price: Preço na unidade original
        price_unit: Unidade original do preço
        target_unit: Unidade desejada

    Returns:
        Preço convertido como Decimal
    """
    factor = get_conversion_factor(target_unit, price_unit)
    return price / factor