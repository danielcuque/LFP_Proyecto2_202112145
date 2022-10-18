from unittest import TestCase

class ParserTest(TestCase):
    def test_parse(self):
        source: str = '''
        <-- Controles
        Boton btn1;
        Controles -->
        '''