#r01
#22K1011 工藤理香

import cgi, sys, io
import sqlite3

from definition import Date_Time
from definition import Weather

sys.stdout=io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form=cgi.FieldStorage()
edit=form.getvalue("edit", "")

connection=sqlite3.connect("to_do_list.sqlite3")
cur=connection.cursor()

cur.execute(f"select * from db where id='{edit}\'")
A=list(cur.fetchone())

template="""
<html>
    <head>
        <meta charset="utf-8">
        <title>to DO</title>
        <link rel="stylesheet" href="../../css/style.css">
    </head>
    <body>
        <form method="post" action="/cgi-bin/L10/ToDo_list.py">
            <div class="Flex">
            <div class="DateTime">
                <p>{date_time}</p>
            </div>
            <div class="Weather">
                <p>{weather}</p>
            </div>
            </div>
            <div class="ToDo">
                <p class="title">　to Do</p>
                <p>edit:
                <input type="date" name="todo_date" value="{date}">
                <input type="text" name="todo_title" value="{title}">
                <input type="text" name="todo_about" value="{about}">
                <input type="hidden" name="edit" value="{edit}">
                <input type="submit" value="submit"></p>
                {toDo}
            </div>
        </form>
    </body>
</html>
"""


date, date_time=Date_Time()

weather=Weather()


column=["DATE", "TO_DO", "ABOUT"]
todo="<table border='1' class='ToDo_list'><tr>"
for x in column:
    todo+=f"<th>{x}</th>"
todo+="</tr><tr>"
for y in A[1:]:
    todo+=f"<td>{y}</td>"
todo+="</tr></table>"



connection.commit()

result=template.format(date_time=date_time, weather=weather, toDo=todo, date=A[1], title=A[2], about=A[3], edit=edit)
print("Content-type: text/html\n")
print(result)

