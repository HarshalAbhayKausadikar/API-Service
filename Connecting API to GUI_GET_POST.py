from tkinter import *
import requests
import json

root = Tk()
root.title("Registration App")
#root.geometry()

root.iconbitmap("registration.ico")

def query():

    top = Toplevel()
    #top.geometry("800x200")
    top.title("Information")
    query_mis = select_box.get()
    print(query_mis)
    s_link = "http://127.0.0.1:5000/student/" + query_mis
    #print(s_link)
    r = requests.request('GET', url=s_link)

    my_label = r.json()

    # for i in r:
    #     my_label += str(i)
    #
    my_lbl = Label(top, text=my_label).pack()


    print(r.json())

def submit():

    dictionary = {"name":name.get(), "mis":mis.get(), "branch":branch.get(), "contact":contact.get(), "email":email.get(), "description":description.get()}
    json_data = json.dumps(dictionary)
    #print(dictionary)

    try:
        response = requests.request('POST', url="http://127.0.0.1:5000/student", json=json_data)
        print(response.json())

    except Exception as e:
        api = "Error..."

    name.delete(0, END)
    mis.delete(0, END)
    branch.delete(0, END)
    contact.delete(0, END)
    email.delete(0, END)
    description.delete(0, END)

def update():
    dictionary = {"name":name.get(), "mis":mis.get(), "branch":branch.get(), "contact":contact.get(), "email":email.get(), "description":description.get()}
    json_data = json.dumps(dictionary)

    query_mis = select_box.get()
    print(query_mis)

    s_link = "http://127.0.0.1:5000/student/" + query_mis
    print(s_link)
    r = requests.request('PUT', url=s_link)

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
Query_b = Button(root, text="Show Data", command=query)
Query_b.grid(row=10, column=0, columnspan=2, padx=20, ipadx=137)


root.mainloop()