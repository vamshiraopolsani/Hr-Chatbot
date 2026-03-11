with open("employee.txt","w") as file:
    file.write("vamshi - core hr\n")
    file.write("anu - core hr\n")

#checking file creation

import os
print(os.listdir())

#reading file
with open("employee.txt","r") as file:
    content = file.read()
    print(content)

#reading line by line
with open("employee.txt","r") as file:
    for line in file:
        print(line.strip())

#creating a python dictionary

employee = {
    "name" : "vamshi",
    "role" : "core hr",
    "skills" : ["core hr","Python","AI"],
    "experience" : 0
}

print(employee)
print(type(employee))

#convert dict to json
import json
employee_json = json.dumps(employee,indent=4)
print(employee_json)
print(type(employee_json))

#convert back
employee_back = json.loads(employee_json)
print(employee_back)
print(type(employee_back))

#save dictionary to a json file

with open("employee.json","w") as file:
    json.dump(employee,file,indent=4)
print("file saved")

#read json file in python

with open("employee.json", "r") as file:
    loaded_employee = json.load(file)
    print(loaded_employee)
    print(loaded_employee["name"])
    print(loaded_employee["skills"])

#client setup
from dotenv import load_dotenv
import os
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#chat with groq
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "what is oracle HCM Cloud in one line?"}
    ]
)

print(response.choices[0].message.content)

#make it conversational

messages = [
    {"role": "user", "content": "what is the difference between CORE HR and TALENT MANAGEMENT in oracle HCM Cloud?"},
    {"role": "system", "content": "you are an HR TECH expert assistant."}
]
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
)
print(response.choices[0].message.content)