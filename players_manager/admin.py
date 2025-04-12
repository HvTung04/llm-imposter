from models.groq_model import GroqModel
from dotenv import load_dotenv
from prompts.admin import admin_ask, admin_rank
import ast
import os

load_dotenv()


class Admin:
    def __init__(
        self,
        model_name=os.getenv("ADMIN_MODEL"),
        ask_system_prompt=admin_ask,
        rank_system_prompt=admin_rank,
    ):
        self.ask_model = GroqModel(
            model_name=model_name,
            system_prompt=ask_system_prompt,
            temperature=1.5,
            max_tokens=128,
            top_p=0.5,
            stream=False,
            stop=None,
        )

        self.rank_model = GroqModel(
            model_name=model_name,
            system_prompt=rank_system_prompt,
            temperature=0.5,
            max_tokens=128,
            top_p=0.5,
            stream=False,
            stop=None,
        )

    def ask(self):
        """
        Create a question for the current turn

        Returns:
            str: The generated question.
        """
        question = self.ask_model.memory_chat(prompt="Hãy trả lại một câu hỏi duy nhất, đừng nói gì khác, đảm bảo mỗi câu hỏi chỉ được hỏi một lần.")
        return question

    def rank(self, question, answers, retry=5):
        """
        Rank the answers provided by players.

        Args:
            question (str): The question to rank the answers for.
            answers (list): List of answers provided by players.

        Returns:
            list: Probability scores for each answer.
        """
        prompt = f"Câu hỏi: {question}\n\n"
        for i, answer in enumerate(answers):
            prompt += f"Đáp án {i + 1}: {answer}\n"
        scores = self.rank_model.generate_plain_text(prompt)

        for i in range(retry):
            try:
                scores = ast.literal_eval(scores)
                break
            except Exception as e:
                print(f"Error parsing scores: {e}")
                scores = self.rank_model.generate_plain_text(prompt)
                print(f"Retrying... {i + 1}/{retry}")
        return scores
