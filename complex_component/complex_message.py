"""
Module containing the message class for complex message type.
"""

from __future__ import annotations
from typing import Any, Dict, Optional

from tools.exceptions.messages import MessageError, MessageValueError
from tools.messages import AbstractResultMessage

class ComplexMessage(AbstractResultMessage):
    CLASS_MESSAGE_TYPE = "Complex"
    MESSAGE_TYPE_CHECK = True

    COMPLEX_VALUE_ATTRIBUTE = "ComplexValue"
    COMPLEX_VALUE_PROPERTY = "complex_value"

    MESSAGE_ATTRIBUTES = {
        COMPLEX_VALUE_ATTRIBUTE : COMPLEX_VALUE_PROPERTY
    }
    # list all attributes that are optional here (use the JSON attribute names)
    OPTIONAL_ATTRIBUTES = []

    # all attributes that are using the Quantity block format should be listed here
    QUANTITY_BLOCK_ATTRIBUTES = {}

    # all attributes that are using the Quantity array block format should be listed here
    QUANTITY_ARRAY_BLOCK_ATTRIBUTES = {}

    # all attributes that are using the Time series block format should be listed here
    TIMESERIES_BLOCK_ATTRIBUTES = []

    # always include these definitions to update the full list of attributes to these class variables
    # no need to modify anything here
    MESSAGE_ATTRIBUTES_FULL = {
        **AbstractResultMessage.MESSAGE_ATTRIBUTES_FULL,
        **MESSAGE_ATTRIBUTES
    }
    OPTIONAL_ATTRIBUTES_FULL = AbstractResultMessage.OPTIONAL_ATTRIBUTES_FULL + OPTIONAL_ATTRIBUTES
    QUANTITY_BLOCK_ATTRIBUTES_FULL = {
        **AbstractResultMessage.QUANTITY_BLOCK_ATTRIBUTES_FULL,
        **QUANTITY_BLOCK_ATTRIBUTES
    }
    QUANTITY_ARRAY_BLOCK_ATTRIBUTES_FULL = {
        **AbstractResultMessage.QUANTITY_ARRAY_BLOCK_ATTRIBUTES_FULL,
        **QUANTITY_ARRAY_BLOCK_ATTRIBUTES
    }
    TIMESERIES_BLOCK_ATTRIBUTES_FULL = (
        AbstractResultMessage.TIMESERIES_BLOCK_ATTRIBUTES_FULL +
        TIMESERIES_BLOCK_ATTRIBUTES
    )

    @property
    def complex_value(self) -> float:
        return self.complex_value


    @complex_value.setter
    def complex_value(self, complex_value: float):
        if self._check_complex_value(complex_value):
            self.__complex_value = complex_value
        else:
            raise MessageValueError(f"Invalid value for ComplexValue: {complex_value}")

    def __eq__(self, other: Any) -> bool:
        return (
            super().__eq__(other) and
            isinstance(other, ComplexMessage) and
            self.complex_value == other.complex_value
        )

    @classmethod
    def _check_complex_value(cls, complex_value: float) -> bool:
        return isinstance(complex_value, float)


    @classmethod
    def from_json(cls, json_message: Dict[str, Any]) -> Optional[ComplexMessage]:
        try:
            message_object = cls(**json_message)
            return message_object
        except (TypeError, ValueError, MessageError):
            return None


ComplexMessage.register_to_factory()