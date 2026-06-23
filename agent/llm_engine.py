from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LLMEngine:
    def __init__(self):
        model_name = "microsoft/phi-2"  # you can change later

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32
        )

        self.model.eval()

    def generate(self, prompt: str, max_new_tokens: int = 120) -> str:
        """
        Unified text generation method for the agent.
        """

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.6,
                top_p=0.9,
                do_sample=True,
            )

        decoded = self.tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )

        # Return only generated part (cleaner)
        return decoded[len(prompt):].strip()
