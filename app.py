from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {"id": 1, "description": "Buy groceries","completed":False},
    {"id": 2, "description": "Write blog post","completed":False},
    {"id": 3, "description": "Build website","completed":False}
]

nextID = 4

@app.route("/",methods=['POST','GET'])
def home():
    global tasks
    if request.method == 'POST':
        new_task = request.form.get("task")
        if new_task and new_task.strip():
            add_dict_tolist(new_task)

    return render_template("home.html",task_list=tasks)

@app.route("/delete/<int:id_num>", methods=['POST','GET'])
def delete(id_num):
    global tasks
    if request.method =='POST':
        tasks = [task for task in tasks if task['id']!=id_num]

    return redirect(url_for('home'))

@app.route("/complete/<int:id_num>", methods=['POST','GET'])
def complete(id_num):
    global tasks
    if request.method =='POST':
        for task in tasks:
            if task['id']==id_num:
                task['completed']=True

    return redirect(url_for('home'))

def add_dict_tolist(item) -> None:
    global nextID
    new_dict = {"id": nextID,"description":item,"completed":False} #create dictionary for new item
    tasks.append(new_dict) # append new dictionary to the list with new numbering
    nextID +=1

if __name__=='__main__':
    app.run(debug=True)
