# employee management system
employees = []

def add_employee(name, age, salary, department):
    employee = {
        "name": name,
        "age": age,
        "salary": salary,
        "department": department
    }
    employees.append(employee)
    print(f" {name} added successfully!")

def show_all_employees():
    print("\n ----All Employees----")
    for employee in employees:
        print(f"Name: {employee['name']}| Age: {employee['age']}| Salary: {employee['salary']}| Department: {employee['department']}")

def get_employee_status(name):
            for employee in employees:
                if employee["name"] == name:
                    if employee["salary"] > 50000:
                        return f"{name} is a senior employee"
                    elif employee["salary"] > 30000:
                        return f"{name} is a mid-level employee"
                    else:
                        return f"{name} is a junior employee"
                    
def total_salary_bill():
                        total = sum(employee["salary"] for employee in employees)
                        print(f"\nTotal Salary Bill: {total}")
add_employee("vamshi", 24, 50000, "IT")
add_employee("anu", 22, 45000, "HR")
add_employee("ram", 30, 60000, "Finance")
show_all_employees()
print(get_employee_status("vamshi"))
print(get_employee_status("anu"))
print(get_employee_status("ram"))
total_salary_bill()