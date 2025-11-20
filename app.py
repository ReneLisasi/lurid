#from urllib import request
from flask import Flask, render_template, request
from slm import infer,init_model
import os


app=Flask(__name__)
generator=init_model()

PROMPT_TEMPLATE_PATH = os.path.join(
    app.root_path,
    "static",
    "prompts",
    "lurid_prompt_template1.md"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/talk')
def talk():
    return render_template('talk.html',message=None)

@app.route('/send_message', methods=["POST"])
def send_message():
    print("dfs")

    user_message = request.form.get("user_message", "")
    
    #infer here
    #generator='text'
    if not user_message.strip():
        return render_template("talk.html", message="Please enter a message.", stressors=[])

    response_text, stressors = infer(user_message, generator, PROMPT_TEMPLATE_PATH)
    return render_template("talk.html", response_text=response_text, stressors=stressors)


if __name__=='__main__':
    app.run(debug=True)