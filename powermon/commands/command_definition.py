from powermon.protocols import ResponseType
from powermon.dto.command_definition_dto import CommandDefinitionDTO
from powermon.commands.response import Response
from powermon.commands.response_definition import ResponseDefinition

class CommandDefinition:
    def __init__(self, code, description, help_text: str, response_type : ResponseType, 
                 response_definitions, test_responses: list, regex: str, command_definition_type: str):
        if response_definitions is None or len(response_definitions) == 0:
            raise ValueError(f"response definitions cannot be None for command_code: {code}")
        if test_responses is None or len(test_responses) == 0:
            raise ValueError(f"test_responses cannot be None for command_code: {code}")
        self.code = code
        self.description = description
        self.help_text = help_text
        self.response_type : ResponseType = response_type
        self.response_definitions : list[ResponseDefinition] = response_definitions
        self.test_responses : list[bytes] = test_responses
        self.regex : str | None = regex
        self.command_definition_type : str = command_definition_type
        
    def to_DTO(self) -> CommandDefinitionDTO:
        return CommandDefinitionDTO(
            command_code=self.code,
            description=self.description,
            help_text=self.help_text,
            response_type=str(self.response_type),
            #responses=self.response_definitions, #TODO: make DTOs for the response definitions
            #test_responses=self.test_responses,
            regex=self.regex
        )
        
    def get_type(self) -> str:
        return self.command_definition_type
        
    def get_response_count(self) -> int:
        if(self.response_definitions is None):
            return 0
        else:
            return len(self.response_definitions)
        
        
    @classmethod
    def from_config(cls, protocol_dictionary : dict, command_definition_type) -> "CommandDefinition":
        code = protocol_dictionary.get("name")
        description = protocol_dictionary.get("description")
        help_text = protocol_dictionary.get("help_text")
        response_type = protocol_dictionary.get("response_type")
        response_definitions : list[ResponseDefinition] = ResponseDefinition.multiple_from_config(protocol_dictionary.get("response"))
        test_responses = protocol_dictionary.get("test_responses")
        regex = protocol_dictionary.get("regex", None)
        return cls(code=code, description=description, help_text=help_text, response_type=response_type, 
                   response_definitions=response_definitions, test_responses=test_responses, regex=regex, command_definition_type=command_definition_type)