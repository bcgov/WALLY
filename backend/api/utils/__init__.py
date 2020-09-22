""" conversions for water data """


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
