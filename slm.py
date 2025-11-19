from transformers import pipeline

#load slm
def init_model():
    # generator = pipeline('text-generation', model='distilgpt2')
    generator='text'
    return generator

def read_file(filepath):
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            content=f.read()
            return content
    except FileNotFoundError:
        return 'Error: File not found'

def infer(message,generator,prompt_path):
    prompt_template = read_file(prompt_path)
    prompt=prompt_template+message
    result = generator(prompt, max_length=50, num_return_sequences=1)
    print(result[0]['generated_text'])
    return result[0]['generated_text']