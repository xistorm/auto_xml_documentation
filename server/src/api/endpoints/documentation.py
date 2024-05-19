from fastapi import APIRouter

from src.models.api import RequestBody
from src.core.services.static_analyzer_service import StaticAnalyzerService

router = APIRouter()


@router.post('/create')
async def create(request_body: RequestBody):
    code_text = request_body.code_text
    documented_code_text = StaticAnalyzerService.add_xml_documentation(code_text)

    return documented_code_text
