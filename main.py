# from view.app import App

from typing import List

from controller.lexer import Lexer
from controller.parser import Parser


def main():
    source: str = '''
                    <!-- Controles
            Contenedor contlogin;
            Boton btnlogin;
            Etiqueta lblusuario;
            Controles -->

            <!--propiedades
            contlogin.setAncho(190); 
            contlogin1.setAlto(150);
            btn1.setColorFondo(47,79,79); 

            //#$inicio de contFondo 
            contFondo.setAncho(800);
            contFondo.setAlto(100); 
            contFondo.setColorFondo(64,64,64);
            //#$fin de contFondo

            //#$inicio de cmdIngresar 
            cmdIngresar.setTexto("Ingresar"); 
            contlogin.add(cmdIngresar);
            //#$fin de cmdIngresar

            //#$inicio de pswClave 
            pswClave.setTexto("");
            //#$fin de pswClave 

            //#$inicio de etiqueta passw
            passw.setAncho(53); 
            passw.setAlto(13 ); 
            passw.setColorLetra(128,128,128);
            passw.setTexto("Password");
            //#$fin de passw

            //#$inicio de Nombre
            Nombre.setAncho(44); 
            Nombre.setAlto(13);
            Nombre.setColorLetra(128,128,128); 
            Nombre.setTexto("Nombre");
            //#$fin de Nombre

            //#$inicio de JTextField0 
            JTextField0.setTexto("");
            //#$fin de JTextField0

            //#$inicio de contlogo2 
            contlogo2.setAncho(150); 
            contlogo2.setAlto( 50);
            contlogo2.setColorFondo(0,128,128); 
            //#$fin de contlogo2

            //#$inicio de ContLogo1 
            ContLogo1.setAncho(50);
            ContLogo1.setAlto( 50); 
            ContLogo1.setColorFondo(64,64,64);
            //#$fin de ContLogo1

            //#$inicio de ContBody 
            ContBody.setAncho(800);
            ContBody.setAlto(300); 
            ContBody.setColorFondo(64,224,208);
            //#$fin de ContBody
            propiedades -->

            <!--Colocacion
            /*
            Posicionamiento de los controles
            */

            contFondo.setPosicion(25,330); 
            this.add(contFondo);
            contlogin.setPosicion(586,110); 
            ContBody.add(contlogin);
            passw.setPosicion(11,54); 
            contlogin.add(passw); 
            cmdIngresar.setPosicion(40,100);
            pswClave.setPosicion(67,48); 
            contlogin.add(pswClave);

            Nombre.setPosicion(8,21);
            contlogin.add(Nombre);
            JTextField0.setPosicion(65,20); 
            contlogin.add(JTextField0);
            contlogo2.setPosicion(88,25); 
            ContBody.add(contlogo2);
            ContLogo1.setPosicion(36,25); 
            ContBody.add(ContLogo1);
            ContBody.setPosicion(23,21); 
            this.add(ContBody);
            Colocacion -->
                    '''

    lexer: Lexer = Lexer(source)
    lexer.fill_table_of_tokens()

    parser: Parser = Parser(lexer.get_valid_tokens())
    parser.parse_programm()

    for error in parser.errors:
        print(error)


if __name__ == "__main__":
    main()
