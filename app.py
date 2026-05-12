from flask import Flask, render_template, request, redirect
from hrms_logic import HRMS, Employee, Manager, Developer
import json

app = Flask(__name__)
system = HRMS()


# ---------- LOAD DATA ----------
def load_data():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)

            for emp in data:
                if emp["type"] == "employee":
                    e = Employee(emp["id"], emp["name"], emp["salary"])

                elif emp["type"] == "manager":
                    e = Manager(emp["id"], emp["name"], emp["salary"], emp["bonus"])

                elif emp["type"] == "developer":
                    e = Developer(emp["id"], emp["name"], emp["salary"], emp["overtime"])

                e.leave_days = emp["leave_days"]
                e.tasks = emp["tasks"]

                system.employees.append(e)
    except:
        pass


# ---------- SAVE DATA ----------
def save_data():
    data = []

    for emp in system.employees:
        if isinstance(emp, Manager):
            emp_type = "manager"
            bonus = emp.bonus
            overtime = 0

        elif isinstance(emp, Developer):
            emp_type = "developer"
            overtime = emp.overtime_hours
            bonus = 0

        else:
            emp_type = "employee"
            bonus = 0
            overtime = 0

        data.append({
            "id": emp.e_id,
            "name": emp.name,
            "salary": emp._Employee__salary,
            "leave_days": emp.leave_days,
            "tasks": emp.tasks,
            "type": emp_type,
            "bonus": bonus,
            "overtime": overtime
        })

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


load_data()


# ---------- ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html', employees=system.employees)


@app.route('/add', methods=['POST'])
def add():
    e_id = request.form['id']
    name = request.form['name']
    salary = float(request.form['salary'])
    emp_type = request.form['type']

    if emp_type == "employee":
        emp = Employee(e_id, name, salary)

    elif emp_type == "manager":
        emp = Manager(e_id, name, salary, float(request.form['bonus']))

    elif emp_type == "developer":
        emp = Developer(e_id, name, salary, int(request.form['overtime']))

    system.add_employee(emp)
    save_data()
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    system.remove_employee(request.form['id'])
    save_data()
    return redirect('/')


@app.route('/task', methods=['POST'])
def task():
    emp = system.find_employee(request.form['id'])
    if emp:
        emp.add_task(request.form['task'])
        save_data()
    return redirect('/')


@app.route('/leave', methods=['POST'])
def leave():
    emp = system.find_employee(request.form['id'])
    if emp:
        emp.apply_leave(int(request.form['days']))
        save_data()
    return redirect('/')


@app.route('/salary', methods=['POST'])
def salary():
    emp = system.find_employee(request.form['id'])
    if emp:
        emp.set_salary(float(request.form['salary']))
        save_data()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)