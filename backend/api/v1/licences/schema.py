"""
API data models for Water Rights Licence analysis.
These are external facing data models/schemas that users see.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema


class LicenceApplicationApproval(BaseModel):
    """ schema for displaying licences, applications, and water use approvals in one table """

    distance: float
    type: str
    usage: Optional[str]
    status: Optional[str]
    qty_m3yr: Optional[float]

    # application fields. They will be blank if not applicable.
    APPLICATION_JOB_NUMBER: Optional[str]
    APPLICATION_STATUS: Optional[str]

    # approval fields
    WATER_APPROVAL_ID: Optional[str]
    WATER_APPROVAL_STATUS: Optional[str]
    APPROVAL_FILE_NUMBER: Optional[str]
    WORKS_DESCRIPTION: Optional[str]

    # common fields
    LICENCE_NUMBER: Optional[str]
    LICENCE_STATUS: Optional[str]
    POD_NUMBER: Optional[str]
    POD_SUBTYPE: Optional[str]
    PURPOSE_USE: Optional[str]
    SOURCE_NAME: Optional[str]
    QUANTITY: Optional[float]
    QUANTITY_UNITS: Optional[str]
    QTY_DIVERSION_MAX_RATE: Optional[float]
    QTY_UNITS_DIVERSION_MAX_RATE: Optional[str]
    QUANTITY_FLAG: Optional[str]
    QUANTITY_FLAG_DESCRIPTION: Optional[str]


class WaterRightsLicence(BaseModel):
    """
    Water rights licences for analysing licences with a defined distance/buffer area.
    Includes fields for applications, if using Water Rights Applications as a data source (in
    addition to Water Rights Licences)
    """

    distance: float

    # application fields. They will be blank if not applicable.
    APPLICATION_JOB_NUMBER: Optional[str]
    APPLICATION_STATUS: Optional[str]

    # common fields
    LICENCE_NUMBER: Optional[str]
    LICENCE_STATUS: Optional[str]
    POD_NUMBER: Optional[str]
    POD_SUBTYPE: Optional[str]
    PURPOSE_USE: Optional[str]
    SOURCE_NAME: Optional[str]
    QUANTITY: Optional[float]
    QUANTITY_UNITS: Optional[str]
    QTY_DIVERSION_MAX_RATE: Optional[float]
    QTY_UNITS_DIVERSION_MAX_RATE: Optional[str]
    QUANTITY_FLAG: Optional[str]
    QUANTITY_FLAG_DESCRIPTION: Optional[str]

    class Config:
        orm_mode = True
