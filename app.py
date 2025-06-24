from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id}>'

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/todos', methods=['POST'])
def create_todo():
    content = request.json.get('content')

    if not content:
        return jsonify({'error': 'No content'}), 400

    new_todo = Todo(content=content)

    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo created successfully!', 'id': new_todo.id}), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()

    result = []
    for todo in todos:
        todo_data = {
            'id': todo.id,
            'content': todo.content,
            'completed': todo.completed
        }
        result.append(todo_data)

    return jsonify({'todos': result})

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    todo.completed = not todo.completed
    db.session.commit()

    return jsonify({'message': 'Todo updated successfully!', 'completed': todo.completed})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
