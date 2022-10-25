from typing import Dict


def lookup_justify(literal: str) -> str:
    literal = literal.lower()
    types_justify: Dict[str, str] = {
        'centro': 'center',
        'derecha': 'right',
        'izquierda': 'left',
    }
    return types_justify.get(literal, 'center')