import re

from django.db.models.base import ModelBase


def camel_case_to_snake_case(camel_case: str) -> str:
    """Recebe uma string em CamelCase e retorna em snake_case

    Args:
        camel_case (str): strint em CamelCase

    Returns:
        str: string transformada para snake_case
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()


class NoPrefixOnTableName(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name != "MyModel":

            class MetaB:
                db_table = camel_case_to_snake_case(name)

            attrs["Meta"] = MetaB

        return super().__new__(cls, name, bases, attrs, **kwargs)
