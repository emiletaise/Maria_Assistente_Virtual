import unittest 
import maria
import json

maria = maria.Maria()

CHAMANDO_MARIA = r"C:\Users\emile.DESKTOP-0DI12O3\Desktop\Maria_Assistente_Virtual - Copia\comandos.json"


class TestNomeAssistente(unittest.TestCase):

    with open(CHAMANDO_MARIA, "r", encoding='utf8') as comandos_file:
        teste = json.load(comandos_file)
        for comando in teste['questions']:
            try:
                if comando:
                        question = maria.get_token(maria, comando)
                        isValid = maria.command_validation(maria, question)

                        if isValid:
                            maria.command_exec(maria, question)
                        else:
                            print("Não entendi!")

            except KeyboardInterrupt:
                print('Bye')
                maria.keepListening = False   
       
           
if __name__ == "__main__":
    carregador = unittest.TestLoader()
    testes = unittest.TestSuite()

    testes.addTest(carregador.loadTestsFromTestCase(TestNomeAssistente))
    executor = unittest.TextTestRunner()
    executor.run(testes)