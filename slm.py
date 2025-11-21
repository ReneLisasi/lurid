from transformers import pipeline

import re
import json
from transformers import StoppingCriteria, StoppingCriteriaList
import torch

#MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
MODEL_NAME = "HuggingFaceTB/SmolLM2-1.7B"

#load slm
def init_model():
    generator = pipeline(
        task='text-generation',
        model=MODEL_NAME, 
        tokenizer=MODEL_NAME,
        dtype="auto",
        #device_map="auto",
        trust_remote_code=True,
        device = 0
    )
    print(torch.version.cuda)

    return generator

def read_file(filepath):
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            content=f.read()
            return content
    except FileNotFoundError:
        return 'Error: File not found'

class StopWhenJSONComplete(StoppingCriteria):
    def __init__(self, tokenizer, prompt_token_count: int):
        self.tokenizer = tokenizer
        self.prompt_token_count = prompt_token_count

    def __call__(self, input_ids, scores, **kwargs):
        # input_ids: [batch_size, seq_len]
        seq = input_ids[0][self.prompt_token_count:]  # generated part only
        if seq.numel() == 0:
            return False

        text = self.tokenizer.decode(seq, skip_special_tokens=True)

        opens = text.count("{")
        closes = text.count("}")

        return opens > 0 and opens == closes
    
def infer(message,generator,prompt_path):
    prompt_template = read_file(prompt_path)
    prompt=prompt_template+message.strip()+"\nJSON:"
    prompt_tokens = generator.tokenizer(prompt, return_tensors="pt")
    prompt_len = prompt_tokens["input_ids"].shape[1]

    stopping_criteria = StoppingCriteriaList(
        [StopWhenJSONComplete(generator.tokenizer, prompt_len)]
    )

    result = generator(
        prompt, 
        max_new_tokens=512, 
        num_return_sequences=1,
        return_full_text=False,
        stopping_criteria=stopping_criteria,
    )
    generated = result[0]["generated_text"]
    print(generated)
    reply, stressors = split_response_and_sensors(generated)
    return reply, stressors


def split_response_and_sensors(generated_text):
    
    match = re.search(r"\{[\s\S]*\}", generated_text)
    if not match:
        print("No JSON found in the generated text.")
        # model ignored instructions
        return generated_text.strip(), []

    json_str = match.group(0)
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        # model produced invalid JSON
        return generated_text.strip(), []

    reply = data.get("reply", "").strip()
    stressors_raw = data.get("stressors", [])

    stressors = []
    print("Raw stressors:", stressors_raw)
    if isinstance(stressors_raw, list):
        for item in stressors_raw:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip()
            if not name:
                continue
            stressors.append(
                {
                    "name": name,
                    "progress": int(item.get("progress", 0)),
                    "stress_level": int(item.get("stress_level", 0)),
                    "tshirt_size": str(item.get("tshirt_size", "")).lower(),
                }
            )
    print("Reply:", reply)
    print("Stressors:", stressors)
    return reply, stressors
