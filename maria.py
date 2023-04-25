import speech_recognition as sr
from nltk import word_tokenize, corpus
import json 

class Maria:

    # Define o contrutor da classe.
    # Inicia variavel booleana para indicar a assistente ouvindo o usuario para novas entradas.
    # Define a assistente em Portugues
    # Define variavel para que contem conjunto de palafras vazias
    def __init__(self):
        self.keepListening = True
        self.LANGUAGE = 'portuguese'
        self.stopwords = set(corpus.stopwords.words(self.LANGUAGE))

    #   Arquivo de configuração para lê o conteudo do json
    #   Incia variaveis para nome da assistente e perguntas
        with open('config.json', "r", encoding='utf8') as config_file:
            config = json.load(config_file)

            self.assistant_name = config["name"]
            self.questions = config["questions"]

            config_file.close()
            
    # Metodo Main 
    # Verifica a variavel comand é valida enquanto o keepListening é verdadeiro 
    # Chama o metodo comand_validation para validar a entrada do usuario
    def main(self):
        # print(self.questions)
        while self.keepListening:
            try:
                command = self.get_speech()
                
                if command:
                    question = self.get_token(self,command)
                    isValid = self.command_validation(self, question)

                    if isValid:

                        self.command_exec(self, question)
                    else:
                        print("Não entendi o que você falou!")
            except KeyboardInterrupt:
                print('Bye')
                self.keepListening = False
    
    # Metodo get_speech responsável pela entrada de voz do usuario
    # Acessa o microfone do dispositivo para captura
    # Solicita que o usuario diga algo em até 5 segundos
    # Utiliza reconhecimento de fala do google
    @staticmethod
    def get_speech():
        command = None
        recognizer = sr.Recognizer()
            
        with sr.Microphone() as audio_src:
            recognizer.adjust_for_ambient_noise(audio_src)
            
            print('Diga alguma coisa... ')
            speech = recognizer.listen(audio_src, timeout=5,)
            
            try:
                command = recognizer.recognize_google(speech, language='pt-BR')
                
                print('Comando: ', command)
            except sr.UnknownValueError:
                print('Alguma coisa deu errado')
        
        return command

    # Remove as palavras vazias 
    @staticmethod
    def remove_stopwords(self, tokens):
        filtered_tokens = []

        for token in tokens:
            if token not in self.stopwords:
                filtered_tokens.append(token)

        return filtered_tokens
    
    # Transforma a entrada em tokens e remove as palavras vazias
    # Cria a lista de tokens, verifica se a primeira palavra é da assistente e identica a intenção do usuario na ultima palavra dita. 
    @staticmethod
    def get_token(self, command):
        question = None
        
        tokens = word_tokenize(command, self.LANGUAGE)
        if tokens:
            tokens = self.remove_stopwords(self,tokens)
            
        print("token >>> " + str(tokens))
                
        if len(tokens) >= 2:
            for name in self.assistant_name:
                if name == tokens[0].lower():
                    question = tokens[len(tokens) - 1].lower() 
        return question

    # Valida se a pergunta do usuario está no json
    @staticmethod
    def command_validation(self, question):        
        isValid = False
        
        if question:
            for registered_question in self.questions:
                if question == registered_question["question"].lower():
                    isValid = True
                    break
        
        return isValid
    
    # Retorna a resposta da pergunta
    @staticmethod
    def get_response(self, question):
        try:
            for registered_question in self.questions:
                if question == registered_question["question"].lower():
                    print(registered_question["response"])
        except:
            print('Alguma coisa deu errado')
    
    # Executa recebendo a pergunta do usuario, caso for pare, finaliza a execução. 
    @staticmethod
    def command_exec(self, question):
        # print(question)
        if question == 'pare':
            print('Fim da execução')
        
            self.keepListening = False
        else:
            self.get_response(self, question)
        
maria = Maria()

if __name__ == "__main__":
    maria.main()