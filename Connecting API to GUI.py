from tkinter import *
import requests
import json

root = Tk()
root.title("Registration App")
#root.geometry()

def query():
    query_mis = select_box.get()
    print(query_mis)
    r = requests.request('GET', url="http://127.0.0.1:5000/student/query_mis")

    print(r.json())

def submit():

    dictionary = {"name":name.get(), "mis":mis.get(), "branch":branch.get(), "contact":contact.get(), "email":email.get(), "description":description.get()}
    json_data = json.dumps(dictionary)
    print(dictionary)

    try:
        r = requests.request('POST',url="http://127.0.0.1:5000/student", data=json_data)

    except Exception as e:
        api = "Error..."

#Creating textboxes

name = Entry(root,width=30)
name.grid(row=0, column=1)

mis = Entry(root,width=30)
mis.grid(row=1, column=1)

branch = Entry(root,width=30)
branch.grid(row=2, column=1)

contact = Entry(root,width=30)
contact.grid(row=3, column=1)

email = Entry(root,width=30)
email.grid(row=4, column=1)

description = Entry(root,width=30)
description.grid(row=5, column=1)

select_box = Entry(root, width=30)
select_box.grid(row=9, column=1)

#Creating labels for textboxes

name_label = Label(root, text="Name")
name_label.grid(row=0,column=0)

mis_label = Label(root, text="MIS")
mis_label.grid(row=1,column=0)

branch_label = Label(root, text="Branch")
branch_label.grid(row=2,column=0)

contact_label = Label(root, text="Contact No.")
contact_label.grid(row=3,column=0)

email_label = Label(root, text="Email")
email_label.grid(row=4,column=0)

description_label = Label(root, text="Write about yourself:")
description_label.grid(row=5,column=0)

select_box_label = Label(root, text="Select ID")
select_box_label.grid(row=9,column=0)


#Creating a submit button
submit_b = Button(root, text="Add Record to Database", command=submit)
submit_b.grid(row=6, column=0, columnspan=2, padx=20, ipadx=100)

#Creating a Query button
Query_b = Button(root, text="Show selection", command=query)
Query_b.grid(row=7, column=0, columnspan=2, padx=20, ipadx=137)

#Creating a delete button
Delete_b = Button(root, text="Delete Record")
Delete_b.grid(row=10, column=0, columnspan=2, padx=20, ipadx=135)

#Creating a edit button
edit_b = Button(root, text="Edit record")
edit_b.grid(row=11, column=0, columnspan=2, padx=20, ipadx=145)



root.mainloop()