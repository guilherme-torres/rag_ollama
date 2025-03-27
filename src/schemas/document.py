from typing import TypedDict, Dict

class Document(TypedDict):
    assunto: str
    numero_processo: str
    data: str
    attachment: Dict
    sistema: str
    numero_documento: str
    subassunto: str
    mimetype: str
    nucleo: str