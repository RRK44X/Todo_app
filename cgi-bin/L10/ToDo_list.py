#r01
#22K1011 工藤理香

import cgi, sys, io
import sqlite3
import pandas as pd

from definition import Date_Time
from definition import Weather

sys.stdout=io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form=cgi.FieldStorage()
todo_date=form.getvalue("todo_date", "")
todo_title=form.getvalue("todo_title", "")
todo_about=form.getvalue("todo_about", " ")
comp=form.getvalue("comp", "")
edit=form.getvalue("edit", "")

connection=sqlite3.connect("to_do_list.sqlite3")
cur=connection.cursor()
try:
    cur.execute("create table db(id, date, title, about)")
except sqlite3.Error:
    pass

cur.execute("select max(id) from db")
l=cur.fetchone()
if l==(None,):
    id_n="0"
else:
    id_n=l[0]

error=""
if edit!="":
    cur.execute(f"update db set date='{todo_date}\', title='{todo_title}\', about='{todo_about}\' where id='{edit}\'")
elif todo_date!="" and todo_title!="":
    cur.execute(f"insert into db values('{str(int(id_n)+1)}\', '{todo_date}\', '{todo_title}\', '{todo_about}\')")
elif comp!="":
    cur.execute(f"delete from db where id == '{comp}'")
    comp=""
elif (todo_date=="" or todo_title=="") and (todo_date!="" or todo_title!=""):
    error="入力を確認してください"

        
template="""
<html>
    <head>
        <meta charset="utf-8">
        <title>to DO</title>
        <link rel="stylesheet" href="../../css/style.css">
    </head>
    <body>
        <form method="post" action="?">
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
                <p>
                <input type="date" name="todo_date" value={date} formaction="/cgi-bin/L10/ToDo_list.py">
                <input type="text" name="todo_title" placeholder="what to do" formaction="/cgi-bin/L10/ToDo_list.py">
                <input type="text" name="todo_about" placeholder="add info" formaction="/cgi-bin/L10/ToDo_list.py">
                <input type="submit" value="submit" formaction="/cgi-bin/L10/ToDo_list.py"></p>
                <p>{error}</p>
                <p>TODAY:{toDo_today}</p>
                <p>OTHER DAYS:{toDo_other}</p>
            </div>
        </form>
    </body>
</html>
"""

date, date_time=Date_Time()
weather=Weather()


column=["ID", "DATE", "TO_DO", "ABOUT"]
cur.execute(f"select * from db")
L=cur.fetchall()
today="本日の予定はありません"
other="他の日の予定はありません"
if L!=[]:
    df=pd.DataFrame(L)
    df.columns=column
    button=[]
    for y in L:
        button.append(f"""
                    <button type="submit" name="comp" value="{y[0]}" formaction="/cgi-bin/L10/ToDo_list.py" class="Button">complete</button>
                    <button type="submit" name="edit" value="{y[0]}" formaction="/cgi-bin/L10/ToDo_edit.py" class="Button">edit</button>
                    """)
    button=list(map(lambda x: x.replace("\n", ""), button))
    df["OPERATION"]=button
    df=df.drop("ID", axis=1)
    df=df.sort_values("DATE")

    df1=df[df["DATE"]==date]
    if not df1.empty:
        today=df1.to_html(escape=False, index=False, classes="ToDo_list")

    df2=df[df["DATE"]!=date]
    if not df2.empty:
        other=df2.to_html(escape=False, index=False, classes="ToDo_list")



connection.commit()

result=template.format(date_time=date_time, weather=weather, date=date, error=error, toDo_today=today, toDo_other=other)
print("Content-type: text/html\n")
print(result)