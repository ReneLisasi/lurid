from flask import Flask, render_template
# from slm import infer,init_model

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/talk')
def talk():
    return render_template('talk.html',message=None)

# @app.route('send_message')
# def send_message(message,prompt_template_path):
#     #infer here
#     generator='text'
#     inference=infer(message,generator,prompt_template_path)
#     return render_template('talk',message=inference)

if __name__=='__main__':
    # generator=init_model()
    app.run(debug=True)