"""
Module containing a template for a simulation platform component,
"""

import asyncio
from typing import Any, cast, Set, Union

from tools.components import AbstractSimulationComponent
from tools.exceptions.messages import MessageError
from tools.messages import BaseMessage
from tools.tools import FullLogger, load_environmental_variables

from complex_component.complex_message import ComplexMessage

LOGGER = FullLogger(__name__)

COMPLEX_VALUE = "COMPLEX_VALUE"
COMPLEX_STRING = "COMPLEX_STRING"

#Ask Ville
SIMPLE_TOPIC = "SIMPLE_TOPIC" 

TIMEOUT = 1.0


class ComplexComponent(AbstractSimulationComponent):

    def __init__(
            self,
            complex_value: float,
            complex_string: str,
            input_components: Set[str],
            output_delay: float):

        super().__init__()

        self._complex_value = complex_value
        self._complex_string = complex_string
        self._current_number_sum = 0.0
        self._current_input_components = set()

        environment = load_environmental_variables(
            (SIMPLE_TOPIC, str, "SimpleTopic")
        )
        self._simple_topic_base = cast(str, environment[SIMPLE_TOPIC])
        self._simple_topic_output = ".".join([self._simple_topic_base, self.component_name])

        self._other_topics = [
            ".".join([self._simple_topic_base, other_component_name])
            for other_component_name in self._input_components
        ]


    def clear_epoch_variables(self) -> None:
        """Clears all the variables that are used to store information about the received input within the
           current epoch. This method is called automatically after receiving an epoch message for a new epoch.

           NOTE: this method should be overwritten in any child class that uses epoch specific variables
        """
        self._current_number_sum = 0.0
        self._current_input_components = set()

    async def process_epoch(self) -> bool:
        """
        Process the epoch and do all the required calculations.
        Assumes that all the required information for processing the epoch is available.

        Returns False, if processing the current epoch was not yet possible.
        Otherwise, returns True, which indicates that the epoch processing was fully completed.
        This also indicated that the component is ready to send a Status Ready message to the Simulation Manager.

        NOTE: this method should be overwritten in any child class.
        TODO: add proper description specific for this component.
        """

        # set the number value used in the output message
        if self._current_input_components:
            if self._complex_string == "Correct":
                self._current_number_sum = round(self._current_number_sum * self._complex_value, 3)
        else:
            self._current_number_sum = round(self._complex_value * self._latest_epoch / 1000, 3)

        # send the output message
        await asyncio.sleep(self._output_delay)
        await self._send_complex_message()

        # return True to indicate that the component is finished with the current epoch
        return True

    async def all_messages_received_for_epoch(self) -> bool:
        return self._input_components == self._current_input_components

    async def general_message_handler(self, message_object: Union[BaseMessage, Any],
                                      message_routing_key: str) -> None:
        """
        Handles the incoming messages. message_routing_key is the topic for the message.
        Assumes that the messages are not of type SimulationStateMessage or EpochMessage.

        NOTE: this method should be overwritten in any child class that
        listens to messages other than SimState or Epoch messages.
        TODO: add proper description specific for this component.
        """
        if isinstance(message_object, ComplexMessage):
            # added extra cast to allow Pylance to recognize that message_object is an instance of SimpleMessage
            message_object = cast(ComplexMessage, message_object)
            # ignore simple messages from components that have not been registered as input components
            if message_object.source_process_id not in self._input_components:
                LOGGER.debug(f"Ignoring ComplexMessage from {message_object.source_process_id}")

            # only take into account the first simple message from each component
            elif message_object.source_process_id in self._current_input_components:
                LOGGER.info(f"Ignoring new ComplexMessage from {message_object.source_process_id}")

            else:
                self._current_input_components.add(message_object.source_process_id)
                self._current_number_sum = round(self._current_number_sum * message_object.complex_value, 3)
                LOGGER.debug(f"Received ComplexMessage from {message_object.source_process_id}")

                self._triggering_message_ids.append(message_object.message_id)
                if not await self.start_epoch():
                    LOGGER.debug(f"Waiting for other input messages before processing epoch {self._latest_epoch}")

        else:
            LOGGER.debug("Received unknown message from {message_routing_key}: {message_object}")

    async def _send_complex_message(self):
        """
        Sends a SimpleMessage using the self._current_number_sum as the value for attribute SimpleValue.
        """
        #Ask Ville
        try:
            complex_message = self._message_generator.get_message(
                ComplexMessage,
                EpochNumber=self._latest_epoch,
                TriggeringMessageIds=self._triggering_message_ids,
                ComplexValue=self._current_number_sum
            )
            #Ask Ville
            await self._rabbitmq_client.send_message(
                topic_name=self._simple_topic_output,
                message_bytes=complex_message.bytes()
            )

        except (ValueError, TypeError, MessageError) as message_error:
            # When there is an exception while creating the message, it is in most cases a serious error.
            LOGGER.error(f"{type(message_error).__name__}: {message_error}")
            await self.send_error_message("Internal error when creating simple message.")

def create_component() -> ComplexComponent:
    """
    Creates and returns a SimpleComponent based on the environment variables.

    TODO: add proper description specific for this component.
    """

    # Read the parameters for the component from the environment variables.
    environment_variables = load_environmental_variables(
        (COMPLEX_VALUE, float, 1.0),   # the value to be added for SimpleValue attribute
        (COMPLEX_STRING, str, ""),
        (INPUT_COMPONENTS, str, ""),  # the comma-separated list of component names that provide input
        (OUTPUT_DELAY, float, 0.0)    # delay in seconds before sending the result message for the epoch
    )

    # The cast function here is only used to help Python linters like pyright to recognize the proper type.
    # They are not necessary and can be omitted.
    complex_value = cast(float, environment_variables[COMPLEX_VALUE])
    # put the input components to a set, only consider component with non-empty names
    input_components = {
        input_component
        for input_component in cast(str, environment_variables[INPUT_COMPONENTS]).split(",")
        if input_component
    }
    output_delay = cast(float, environment_variables[OUTPUT_DELAY])

    # Create and return a new SimpleComponent object using the values from the environment variables
    return ComplexComponent(
        complex_value=complex_value,
        complex_string = complex_string,
        input_components=input_components,
        output_delay=output_delay
    )
async def start_component():
    """
    Creates and starts a SimpleComponent component.
    """
    complex_component = create_component()

    # The component will only start listening to the message bus once the start() method has been called.
    await complex_component.start()

    # Wait in the loop until the component has stopped itself.
    while not complex_component.is_stopped:
        await asyncio.sleep(TIMEOUT)


if __name__ == "__main__":
    asyncio.run(start_component())