#Generate a dialoge of TinyTroupe agents influenced by querying OpenAI
import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *

# Function to query OpenAI's GPT-4o
def get_gpt_response(prompt):
    completions = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a conversational assistant helping two AI personas interact."},
                  {"role": "user", "content": prompt}]
    )
    return completions.choices[0].message.content

# Create TinyPerson - Enrique
persona = TinyPerson("Enrique")
persona.define("age", 35)
persona.define("nationality", "Mexican")
persona.define("occupation", "Baker, Mechanic, Accountant")
persona.define("routine", "Every morning, you wake up, stretch, have coffee, and check your emails.")
persona.define("personality", {"traits": [
    "You don't mind explaining things and have a lot of patience.",
    "You enjoy explaining solutions to problems with numbers.",
    "You are friendly and a good active listener.",
    "You are a great collaborator with people"
]})

# Create TinyPerson - Trisha
personb = TinyPerson("Trisha")
personb.define("age", 24)
personb.define("nationality", "Swedish")
personb.define("occupation", "Model, Chemist, Gymnast")
personb.define("routine", "Every morning, you wake up, stretch, and have coffee.")
personb.define("personality", {"traits": [
    "You love to read to be caught up in the lastest science news.",
    "You love cooking healthy food.",
    "You are an excellent planner",
    "You enjoy comedy and have a great sense of humor."
]})

# Create the world
environment = TinyWorld("Corner Cafe", [persona, personb])
environment.make_everyone_accessible()

# AI-driven conversation
prompt = "Leslie and Ashley are discussing the best places to network with other people."
ai_response = get_gpt_response(prompt)

persona.listen(ai_response)
response_b = get_gpt_response(f"Trisha, respond to Enrique: {ai_response}")
personb.listen(response_b)

# Run the interaction
environment.run(4)
