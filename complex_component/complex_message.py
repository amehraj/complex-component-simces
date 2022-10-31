# -*- coding: utf-8 -*-
# Copyright 2021 Tampere University and VTT Technical Research Centre of Finland
# This software was developed as a part of the ProCemPlus project: https://www.senecc.fi/projects/procemplus
# This source code is licensed under the MIT license. See LICENSE in the repository root directory.
# Author(s): Ville Heikkilä <ville.heikkila@tuni.fi>

"""
Module containing the message class for simple message type.
"""

from __future__ import annotations
from typing import Any, Dict, Optional

from tools.exceptions.messages import MessageError, MessageValueError
from tools.messages import AbstractResultMessage


class ComplexMessage(AbstractResultMessage):
    """Description for the SimpleMessage class"""
    CLASS_MESSAGE_TYPE = "Complex"
    MESSAGE_TYPE_CHECK = True

    COMPLEX_VALUE_ATTRIBUTE = "ComplexValue"
    COMPLEX_VALUE_PROPERTY = "complex_value"
    COMPLEX_STRING_ATTRIBUTE = "ComplexString"
    COMPLEX_STRING_PROPERTY = "complex_string"

    # all attributes specific that are added to the AbstractResult should be introduced here
    MESSAGE_ATTRIBUTES = {
        COMPLEX_VALUE_ATTRIBUTE: COMPLEX_VALUE_PROPERTY
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

    # for each attributes added by this message type provide a property function to get the value of the attribute
    # the name of the properties must correspond to the names given in MESSAGE_ATTRIBUTES
    # template for one property:
    @property
    def complex_value(self) -> float:
        """TODO: Description what the simple value is."""
        return self.__complex_value
    @property
    def complex_string(self) -> float:
        """TODO: Description what the simple value is."""
        return self.__complex_string

    # for each attributes added by this message type provide a property setter function to set the value of
    # the attribute the name of the properties must correspond to the names given in MESSAGE_ATTRIBUTES
    # template for one property setter:
    @complex_value.setter
    def complex_value(self, complex_value: float):
        if self._check_complex_value(complex_value):
            self.__complex_value = complex_value
        else:
            raise MessageValueError(f"Invalid value for ComplexValue: {complex_value}")

    @complex_string.setter
    def complex_string(self, complex_string: float):
        if self._check_complex_string(complex_string):
            self.__complex_string = complex_string
        else:
            raise MessageValueError(f"Invalid value for ComplexValue: {complex_string}")

    # provide a new implementation for the "test of message equality" function
    def __eq__(self, other: Any) -> bool:
        return (
            super().__eq__(other) and
            isinstance(other, ComplexMessage) and
            self.complex_value == other.complex_value and 
            self.complex_string == other.complex_string
        )

    # Provide a class method for each attribute added by this message type to check if the value is acceptable
    # These should return True only when the given parameter corresponds to an acceptable value for the attribute
    @classmethod
    def _check_complex_value(cls, complex_value: float) -> bool:
        return isinstance(complex_value, float)

    @classmethod
    def _check_complex_string(cls, complex_string: str) -> bool:
        return isinstance(complex_string, str)
    # Provide a new implementation for the class method from_json method
    # Only the return type should be changed here
    @classmethod
    def from_json(cls, json_message: Dict[str, Any]) -> Optional[ComplexMessage]:
        """TODO: description for the from_json method"""
        try:
            message_object = cls(**json_message)
            return message_object
        except (TypeError, ValueError, MessageError):
            return None


ComplexMessage.register_to_factory()