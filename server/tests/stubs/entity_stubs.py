from src.models.entities import VariableEntity, FunctionEntity, ClassEntity
from .code_stubs import variable_text, function_text, class_text


variable_entity = VariableEntity(variable_text)
function_entity = FunctionEntity(function_text)
class_entity = ClassEntity(class_text)
