"""This file contains the correctors services responsible for the correction of the exams by the AI."""

import connectors.openai_connector as openai_connector
from schemas.items import QuestionDoc, ImageDoc

"""
This file is under construction. In order to get a function that corrects the questions,
I need to get access for firebase url storage, and then then function should: 
1. receive as argument a question document, and an image document.
2. form the prompt to send to openai.
3. parse the response from openai.
4. save the response on the database.
"""