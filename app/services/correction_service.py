"""This file contains the correctors services responsible for the correction of the exams by the AI."""

import connectors.openai_connector as openai_connector
from schemas.items import QuestionDoc, ImageDoc
from schemas.prompts_schemas import CorrectionPrompt

"""
This file is under construction. In order to get a function that corrects the questions,
I need to get access for firebase url storage, and then then function should: 
1. receive as argument a question document, and an image document.
2. form the prompt to send to openai.
3. parse the response from openai.
4. save the response on the database.
"""

def correct_question(question: QuestionDoc, image: ImageDoc):
    """Constructs the prompts and sends it to the openai api."""
    prompt = CorrectionPrompt(
        question_text=question.question_text,
        question_answer=question.question_answer
    )

    params = {
        "system_message": prompt.system_prompt,
        "json_mode": True
    }

    response = openai_connector.send_online_image_to_openai(prompt.template, image.url, **params)
    return response
