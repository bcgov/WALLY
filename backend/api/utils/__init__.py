import os
import uuid

""" general utility functions """


def normalize_quantity(qty, qty_unit: str):
    """ takes a qty and a unit (as a string) and returns the quantity in m3/year
        accepts:
        m3/sec
        m3/day
        m3/year
        Returns None if QUANTITY_UNITS doesn't match one of the options.
    """

    qty_unit = qty_unit.strip()

    if qty_unit == 'm3/year':
        return qty
    elif qty_unit == 'm3/day':
        return qty * 365
    elif qty_unit == 'm3/sec':
        return qty * 60 * 60 * 24 * 365
    else:
        # could not interpret QUANTITY_UNIT value
        return None



def get_file_ext(file_path: str) -> str:
    file_name, file_extension = os.path.splitext(file_path)
    return file_extension


def get_file_name(file_path: str) -> str:
    file_name, file_extension = os.path.splitext(file_path)
    return file_name


def generate_file_name(file_name: str) -> str:
    file_ext = get_file_ext(file_name)
    return f'{str(uuid.uuid4())}{file_ext}'
