class Employee:
    company_name = "abcd"

    def __init__(self, e_id, name, salary):
        self.e_id = e_id
        self.name = name
        self.__salary = salary
        self.leave_days = 0
        self.tasks = []

    def get_salary(self):
        return self.__salary

    def set_salary(self, new_salary):
        if new_salary <= 0:
            print("Invalid salary.")
        else:
            self.__salary = new_salary

    def apply_leave(self, days):
        if days <= 0:
            return
        if self.leave_days + days <= 5:
            self.leave_days += days

    def add_task(self, task):
        self.tasks.append(task)


class Manager(Employee):
    def __init__(self, e_id, name, salary, bonus):
        super().__init__(e_id, name, salary)
        self.bonus = bonus

    def get_salary(self):
        return super().get_salary() + self.bonus


class Developer(Employee):
    def __init__(self, e_id, name, salary, overtime_hours):
        super().__init__(e_id, name, salary)
        self.overtime_hours = overtime_hours

    def get_salary(self):
        return super().get_salary() + (self.overtime_hours * 500)


class HRMS:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        if not self.find_employee(employee.e_id):
            self.employees.append(employee)

    def find_employee(self, e_id):
        for e in self.employees:
            if e.e_id == e_id:
                return e
        return None

    def remove_employee(self, e_id):
        e = self.find_employee(e_id)
        if e:
            self.employees.remove(e)