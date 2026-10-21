from flask import Flask, request, redirect, jsonify, render_template_string

app = Flask(__name__)

tasks = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Task Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 50px auto;
            background: #f4f7fb;
            color: #263238;
        }
        h1 { color: #2457a7; }
        form { margin: 20px 0; }
        input[type=text] {
            padding: 12px;
            width: 65%;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button, .action {
            padding: 10px 14px;
            border: none;
            border-radius: 5px;
            background: #2457a7;
            color: white;
            cursor: pointer;
            text-decoration: none;
        }
        li {
            background: white;
            margin: 12px 0;
            padding: 15px;
            border-radius: 8px;
        }
        .completed {
            text-decoration: line-through;
            color: gray;
        }
        .delete { background: #c0392b; }
    </style>
</head>
<body>
    <h1>Student Task Manager</h1>
    <p>Organize your academic tasks in one place.</p>

    <form action="/add" method="post">
        <input type="text" name="title"
               placeholder="Enter a task..." required>
        <button type="submit">Add Task</button>
    </form>

    <h2>My Tasks</h2>
    <ul>
    {% for task in tasks %}
        <li>
            <span class="{{ 'completed' if task.completed else '' }}">
                {{ task.title }}
            </span>
            <a class="action" href="/complete/{{ task.id }}">
                {% if task.completed %}Undo{% else %}Complete{% endif %}
            </a>
            <a class="action delete" href="/delete/{{ task.id }}">
                Delete
            </a>
        </li>
    {% else %}
        <p>No tasks yet. Add your first task!</p>
    {% endfor %}
    </ul>
    <p>Total tasks: {{ tasks|length }}</p>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title", "").strip()

    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "completed": False
        })
        next_id += 1

    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    return redirect("/")


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/api/tasks")
def get_tasks():
    return jsonify(tasks), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
