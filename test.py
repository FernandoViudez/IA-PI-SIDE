from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import JaccardSimilarity
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.languages import SPA

#Descomentar estas lineas sólo la primera vez que se ejecute el algoritmo para instalar los componentes que falten.
#Luego se pueden volver a comentar

#import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')

#Creo una instancia de la clase ChatBot
chatbot = ChatBot(
    'Xpikuos',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite5',
    statement_comparison_function = LevenshteinDistance(SPA),
    logic_adapters=[ 
        #'chatterbot.logic.MathematicalEvaluation', #Este es un logic_adapter que responde preguntas sobre matemáticas en inglés
        #'chatterbot.logic.TimeLogicAdapter', #Este es un logic_adapter que responde preguntas sobre la hora actual en inglés  
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        }
        #{
        #    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
        #    'threshold': 0.51,
        #    'default_response': 'Disculpa, no te he entendido bien. ¿Puedes ser más específico?.'
        #},
        #{
        #    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        #    'input_text': 'Eso es todo',
        #    'output_text': 'Perfecto. Hasta la próxima'
        #},
    ],
    
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
)

DEFAULT_SESSION_ID = 1

trainer = ListTrainer(chatbot)
trainer.train('chatterbot.corpus.spanish')
trainer.train("./PreguntasYRespuestas.yml")

disparate=Statement('se te ha ido la pinza')
entradaDelUsuario = ""
entradaDelUsuarioAnterior = ""

while entradaDelUsuario!="adios":

    entradaDelUsuario = input()
    
    response = chatbot.generate_response(entradaDelUsuario, DEFAULT_SESSION_ID)
    
    if levenshtein_distance.compare(entradaDelUsuario, disparate) > 0.51:
        print('¿Qué debería haber dicho?')
        entradaDelUsuarioCorreccion = input()
        trainer.train([entradaDelUsuarioAnterior, entradaDelUsuarioCorreccion])
        print("He aprendiendo que cuando digas {} debo responder {}".format(entradaDelUsuarioAnterior, entradaDelUsuarioCorreccion))
    
    entradaDelUsuarioAnterior = entradaDelUsuario

    print("\n%s\n\n" % response)