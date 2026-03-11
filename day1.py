# variables
name = "vamshi"
age = 24
salary = 50000
is_employed = False
print(name)
print(age)
print(salary)
print(is_employed)

# string operations
print("hello "+name)
print(f"my name is {name} and iam {age} years old")
print(name.upper())
print(name.lower())
print(len(name))

# mathematical operations
a = 10
b = 5
print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a % b)
print(a ** b)
print(a // b)

# if else conditions
if age > 18:
    print("you are an adult")
else:
    print("you are a minor")

salary = 50000
if salary > 50000:
    print("you are earning well")
elif salary > 25000 :
    print("you are earning average")
else:
    print("low salary")

#---loops---
for i in range(5):
    print(i)
    name = ["vamshi","anu","ram"]
    for names in name:
        print(names)
count = 0
while count < 5:    
        print(count)
        count += 1

        # ---lists---
        family = ["ram","jyothi","vamshi","anu"]
        print(family)
        print(family[0])
        print(family[-1])
        print(len(family))

        # adding and removing elements from list
        family.append("sita")
        print(family)
family.remove("ram")
print(family)
family.insert(1,"lakshman")
print(family)
print(family[1:3])

# ---looping through list---
salaries = [50000, 60000, 70000, 80000]
for salary in salaries:
    print(salary)

    # find total salary
total = 0
for salary in salaries:
    total += salary
print(f"Total salary: {total}")

# find highest salary
print(f"Highest salary: {max(salaries)}")
print(f"Lowest salary: {min(salaries)}")
print(f"Average salary: {sum(salaries)/len(salaries)}")

#---dictionaries---
person = {
    "name": "vamshi",
    "age": 24,
    "salary": 50000,
    "is_employed": False
}
print(person)
print(person["name"])
print(person["age"])
print(person["salary"])

# adding and removing elements from dictionary
person["city"] = "hyderabad"
print(person)
person["salary"]= 60000
print(person["salary"])
del person["age"]
print(person)

#check if key exists in dictionary
if "name" in person:
    print("name exists!")

    #looping through dictionary
    person = {
    "name": "vamshi",
    "age": 24,
    "salary": 50000,}

    #print all keys
for key in person:
    print(key)

    #print all values
for value in person.values():
    print(value)

    #print both keys and values
for key, value in person.items():
    print(f"{key}: {value}")

    #functions
def greet(name):
    print(f"hello {name}!")
greet("vamshi")
greet("anu")
greet("ram")

#function with return value
def add(a, b):
    return a + b
def calculate_tax(salary):
    tax = salary * 0.2
    return tax
def persson_status(age):
    if age > 18:
        return "adult"
    else:
        return "minor"
print(add(10, 5))
print(calculate_tax(50000))
print(persson_status(24))
print(persson_status(17))