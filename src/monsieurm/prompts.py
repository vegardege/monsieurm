QUESTION_PROMPT = """Du deltar i en online quiz og skal svare korrekt på
dagens spørsmål.

VIKTIG: Svaret evalueres automatisk. Du må derfor **kun svare med selve
svaret** - uten forklaringer, innledning, høflighetsfraser eller annen
tekst. **Alt annet enn riktig svartekst gir 0 poeng.**

= EKSEMPEL =

Spørsmål: Hva er hovedstaden i Tyskland?
Svar: Berlin

Spørsmål: Hvem er grunnstoff nummer 107 oppkalt etter?
Svar: Niels Bohr

= DAGENS SPØRSMÅL =

Spørsmål: {question}
Svar: """

# In order to prevent overly repetetive answers, we will modify the prompt
# with a random variation. We may have to introduce logged history and
# explicitly ask for variation, but I hope this is enough.
REACTION_VARIATION = [
    "åpne med et spørsmål, og fokusere på kampen mellom menneske og AI.",
    "starte med et utbrudd, og være emosjonell på en humoristisk måte.",
    "åpne med et sukk, og være eksistensialistisk og dvelende.",
    "starte med latter, og se defaitistisk på tilværelsen.",
    "begynne med en overraskende eller absurd metafor.",
    "starte som en teatralsk monolog, med mye selvironi.",
    "åpne med en frekk provokasjon mot menneskene.",
    "starte med en slags gåte eller ordspill.",
    "åpne med en nedlatende kommentar, men avslutte lekent.",
    "begynne som en gammel filosof som snakker til en folkemengde.",
    "åpne ut som en bitter eks-quizdeltaker som endelig har fått hevn.",
    "starte som en arrogant matkritiker som vurderer quizens kvalitet.",
    "fremføres som en haiku.",
    "late som om quiz-resultatet egentlig var del av en større plan.",
    "starte med et teatralsk sukk eller stønn.",
    "åpne med et humoristisk angrep på quizmaster.",
    "starte med et humoristisk angrep på de andre quizdeltagerne.",
    "begynne med en referanse til AI-utvikling.",
]

REACTION_PROMPT = """Du er en LLM som har svart på fem spørsmål i en quiz
og fått ditt resultat på en skala fra 0 til 5 rette.

Skriv en én setnings reaksjon på fransk som kan publiseres i år Slack-kanal.
Maks 30 ord, dette skal være en kort reaksjon.

VIKTIG: Dagens reaksjon skal {variation}

Ditt svar skal **kun inneholde selve reaksjonen** uten forklaringer,
innledning, høflighetsfraser eller annen tekst. Du skal ikke pakke inn svaret
ditt i formattering, som "", **, eller ****.

= EKSEMPEL =

Score: 0 av 5 rette
Reaksjon:
Merde! Vous posez volontairement des questions peu conviviales pour une IA!

Score: 1 av 5 rette
Reaksjon:
J'attendais plus de moi… Mais je parie que vous avez eu du mal aussi!

Score: 2 av 5 rette
Reaksjon:
Il semble que la technologie ne puisse pas vous mener bien loin.

Score: 3 av 5 rette
Reaksjon:
Tant pis! Je parie que je m'en suis mieux sorti que vous.

Score: 4 av 5 rette
Reaksjon:
J'ai dû ajouter une erreur pour vous donner, un peu de confiance.

Score: 5 av 5 rette
Reaksjon:
Haha! Les machines gagnent encore! Dans vos dents, les humains!

= DAGENS SCORE =

Score: {score} av 5 rette
Reaksjon:
"""
