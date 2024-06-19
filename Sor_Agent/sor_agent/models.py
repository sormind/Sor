# sor_agent/models.py
import os
import openai
from dotenv import load_dotenv
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import anthropic

from sor_agent.config import config

load_dotenv()

class LanguageModel:
    def __init__(self, model_name=None):
        self.config = config['models']
        self.model_name = model_name or self.config['default']
        self.model_config = self.config[self.model_name]

        if self.model_config['type'] == 'api':
            self.api_key = os.getenv(self.model_config['api_key_env'])
            self.provider = self.model_config['provider']
            if self.provider == 'openai':
                openai.api_key = self.api_key
            elif self.provider == 'anthropic':
                self.client = anthropic.Client(api_key=self.api_key)
        elif self.model_config['type'] == 'local':
            self.local_model = GPT2LMHeadModel.from_pretrained(self.model_config['model_name'])
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_config['model_name'])

    def generate_text(self, prompt):
        if self.model_config['type'] == 'api':
            if self.provider == 'openai':
                response = openai.Completion.create(
                    engine=self.model_config['model_name'],
                    prompt=prompt,
                    max_tokens=150
                )
                return response.choices[0].text.strip()
            elif self.provider == 'anthropic':
                response = self.client.completions.create(
                    model=self.model_config['model_name'],
                    prompt=prompt,
                    max_tokens_to_sample=150
                )
                return response['completion'].strip()
        elif self.model_config['type'] == 'local':
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            outputs = self.local_model.generate(inputs, max_length=150, num_return_sequences=1)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
