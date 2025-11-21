from flask import Flask, render_template, request
from slm import infer, init_model
import os

app = Flask(__name__)

generator = init_model()

PROMPT_TEMPLATE_PATH = os.path.join(
    app.root_path,
    "static",
    "prompts",
    "lurid_prompt_template1.md"
)

# --------------------
# ROUTES
# --------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/talk')
def talk():
    # first load: no stressors yet, don’t show the right card
    return render_template(
        'talk.html',
        message=None,
        response_text=None,
        stressors=[],
        show_stressors=False
    )


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get("message", "").strip()

    if not user_message:
        return render_template(
            "talk.html",
            message="Please enter a message.",
            response_text=None,
            stressors=[],
            show_stressors=False
        )

    response_text, stressors = infer(user_message, generator, PROMPT_TEMPLATE_PATH)

    return render_template(
        "results.html",
        response_text=response_text,
        stressors=stressors
    )

if __name__ == '__main__':
    app.run(debug=True)
