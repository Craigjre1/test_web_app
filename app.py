from flask import Flask, render_template

app = Flask(__name__)
tasks = ["Buy groceries", "Write blog post", "Call Mum"]

@app.route("/")
def hello_world():
    return render_template("home.html",task_list=tasks)

if __name__=='__main__':
    app.run(debug=True)
