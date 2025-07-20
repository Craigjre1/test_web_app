from flask import Flask, render_template, request

app = Flask(__name__)

tasks = [
    {"id": 1, "description": "Buy groceries"},
    {"id": 2, "description": "Write blog post"},
    {"id": 3, "description": "Build website"}
]

@app.route("/",methods=['POST','GET'])
def hello_world():
    if request.method == 'POST':
        new_task = request.form.get("task")
        if new_task and new_task.strip():
            add_dict_tolist(new_task,tasks) # will also renumber tasks, allowing for deletions

    return render_template("home.html",task_list=tasks)

def add_dict_tolist(item,my_list):
    new_ID = 1
    for my_dict in my_list: #renumber all existing items in the list (allowing for deletions)
        my_dict["id"] = new_ID
        new_ID+=1
    
    new_dict = {"id": new_ID,"description":item} #create dictionary for new item
    my_list.append(new_dict) # append new dictionary to the list with new numbering


if __name__=='__main__':
    app.run(debug=True)
