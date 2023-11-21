from typing import List, Optional

from pydantic import BaseModel
from utils.prompts import BINARY_CORRECTION_PROMPT, BYNARY_CORRECTION_SYSTEM_PROMPT


class CorrectionPrompt(BaseModel):
    """Constructor for the correction prompt."""

    system_prompt:str = BYNARY_CORRECTION_SYSTEM_PROMPT
    question_text: str
    question_answer: str
    template: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.format_string()

    def format_string(self):
        self.template = BINARY_CORRECTION_PROMPT.format(
            question_text=self.question_text,
            question_answer=self.question_answer
        )
