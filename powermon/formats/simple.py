import logging
from powermon.formats.abstractformat import AbstractFormat
from powermon.dto.formatDTO import FormatDTO
from powermon.commands.result import Result

log = logging.getLogger("simple")


class SimpleFormat(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "simple"
        self.extra_info = formatConfig.get("extra_info", False)
   
    def set_command_description(self, command_description):
        pass

    def format(self, result: Result) -> list:

        _result = []

        # check for error in result
        #if result.error:
        #    data = {}
        #    data["Error"] = [f"Command: {result.command_code} incurred an error or errors during execution or processing", ""]
        #    data["Error Count"] = [len(result.error_messages), ""]
        #    for i, message in enumerate(result.error_messages):
        #        data[f"Error #{i}"] = [message, ""]


        if len(result.get_responses()) == 0:
            return _result

        display_data = self.format_and_filter_data(result)

        # build data to display
        for key in display_data:
            value = display_data[key][0]
            unit = display_data[key][1]
            if len(display_data[key]) > 2 and display_data[key][2] and self.extra_info:
                extra = display_data[key][2]
                _result.append(f"{key}={value}{unit} {extra}")
            else:
                _result.append(f"{key}={value}{unit}")
        return _result

    @classmethod
    def from_DTO(cls, dto: FormatDTO):
        return cls(formatConfig={})