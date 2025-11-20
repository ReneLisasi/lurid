from flask import Flask, render_template, request
from slm import infer, init_model
import os

app = Flask(__name__)

# --- their model setup (keep this) ---
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
    # your textarea is named "message" in talk.html
    user_message = request.form.get("message", "").strip()

    # if empty, just return them to the talk page with an error
    if not user_message:
        return render_template(
            "talk.html",
            message="Please enter a message.",
            response_text=None,
            stressors=[],
            show_stressors=False
        )

    # use their infer() pipeline
    response_text, stressors = infer(user_message, generator, PROMPT_TEMPLATE_PATH)

    # OPTION: show results on a separate results.html page
    # You can pass stressor data to the chart via Jinja/JS
    return render_template(
        "results.html",
        response_text=response_text,
        stressors=stressors,
        analysis_text="Here’s how your emotions are showing up based on what you wrote."
    )


if __name__ == '__main__':
    app.run(debug=True)
