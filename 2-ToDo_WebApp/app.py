from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    todo_task = db.Column(db.String(300), nullable= False)
    time_created = db.Column(db.DateTime, default= datetime.utcnow())
    
    def __repr__(self): 
        return f'YOur ToDo Task Created {self.id!r}'


@app.route('/', methods= ['POST','GET'])
def task_method():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(todo_task=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Task couldnt be added"
    else:
        tasks = Todo.query.order_by(Todo.time_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def task_delete(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return "Task couldnt be deleted"
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def task_update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.todo_task = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Task couldnt be updated"
    else:
        return render_template('update.html',task=task)

if __name__ == '__main__':
    app.run(debug=True)