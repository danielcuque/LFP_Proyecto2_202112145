class GenerateHTML:
    def __init__(self) -> None:
        pass


    def header_html(self) -> str:
        header: str = ''''
        <html>
            <head>
            <link href="prueba.css" rel="stylesheet" type="text/css" />
            </head>
        '''

    def body_html(self) -> str:
        body: str = f'''
        <body>
        {self._generate_body()}
        </body>
        '''

    def _generate_body(self) -> str:
        pass