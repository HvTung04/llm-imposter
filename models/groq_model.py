from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class GroqModel:
    def __init__(
        self,
        model_name,
        client=client,
        system_prompt=None,
        response_format=None,
        temperature=0.5,
        max_tokens=512,
        top_p=0.5,
        stream=False,
        stop=None,
    ):
        """
        Initialize the GroqModel with the given parameters.

        Args:
            client: The Groq client to use for the model.
            model_name: The name of the model to use.
            system_prompt: The system prompt to use.
            temperature: The temperature to use.
            max_tokens: The maximum number of tokens to generate.
            top_p: The nucleus sampling threshold.
            stream: Whether to stream the response.
            stop: The stop sequence to use.
        """
        self.client = client
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.response_format = response_format
        self.top_p = top_p
        self.stream = stream
        self.stop = stop
        self.memory = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ] if self.system_prompt else []

    def generate_plain_text(self, prompt):
        if self.system_prompt:
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        else:
            messages = [
                {"role": "user", "content": prompt},
            ]

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format=self.response_format,
            top_p=self.top_p,
            stream=self.stream,
            stop=self.stop,
        )

        output = chat_completion.choices[0].message.content
        return output
    
    def memory_chat(self, prompt=None):
        """
        Chat with your restored memory
        """
        if prompt:
            self.memory.append({"role": "user", "content": prompt})
        chat_completion = self.client.chat.completions.create(
            messages=self.memory,
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format=self.response_format,
            top_p=self.top_p,
            stream=self.stream,
            stop=self.stop,
        ).choices[0].message
        self.memory.append(chat_completion)
        return chat_completion.content
    
    def reset_memory(self):
        """
        Reset the memory of the model.
        """
        self.memory = []

    def tools_chat(self, messages, tools):
        response = (
            self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=self.stream,
                tools=tools,
                tool_choice="auto",
            )
            .choices[0]
            .message
        )
        return response, response.tool_calls