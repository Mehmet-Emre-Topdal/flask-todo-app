
from flask import Flask,render_template,redirect,url_for,request
from wtforms import Form,StringField,validators,IntegerField

import sqlite3 as sqlite


#Form class
class AddTaskForm(Form):
   taskName = StringField("Task name:", validators=[validators.DataRequired()])
   importance = IntegerField("Importance",validators=[validators.NumberRange(min=1, max=3),validators.DataRequired()])
   duration = IntegerField("Duration",validators=[validators.NumberRange(min=1, max=3),validators.DataRequired()])

app = Flask(__name__)


@app.route("/")
def index():
   con = sqlite.connect("tasks.sqlite")
   con.row_factory = sqlite.Row
   cur = con.cursor()
   cur.execute("select * from Tasks")
   rows = cur.fetchall() #Tüm satırları çekmek

   return render_template("index.html", tasklist = rows)


#TASK EKLEME
@app.route("/addtask", methods=["GET","POST"])
def addtask():
   form = AddTaskForm(request.form)

   if request.method == "POST" and form.validate(): 
      taskName = form.taskName.data
      importance = form.importance.data
      duration = form.duration.data

      with sqlite.connect("tasks.sqlite") as con:
          
         cursor_=con.cursor()
         query = """INSERT INTO Tasks (taskname, importance, duration) VALUES ("{}", {}, {})""".format(taskName,importance,duration)
         cursor_.execute(query)
         con.commit()    

      return redirect(url_for("index"))#işin bitince ana sayfaya geri dön
   else:
      return render_template("addtask.html", form=form)

#TASK SİLME
@app.route("/delete/<string:id>")
def delete(id):
   
   with sqlite.connect("tasks.sqlite") as con:
         cur=con.cursor()
         query = """DELETE FROM Tasks WHERE id = {}""".format(id)
         cur.execute(query)
         con.commit()

   return redirect(url_for("index"))


#TASK GÜNCELLEME-EDİT
@app.route("/edit/<string:id>",methods = ["GET","POST"])
def update(id):

   if request.method == "GET":      
      #güncellenecek verilerin başlangıçta formda gözükmesi
      updateForm = AddTaskForm()

      with sqlite.connect("tasks.sqlite") as con:
         con.row_factory = sqlite.Row#Burdaki satır verileri obje şeklinde, kullanıma uygun biçimde almaya yarıyor
         #verilerin dictionary şeklinde dönmesini sağlıyor

         cur=con.cursor()
         query = """ SELECT taskname,importance,duration from Tasks WHERE (ID = {})""".format(id)
         cur.execute(query)
         row = cur.fetchone()#1 tane satır çekme

      updateForm.taskName.data = row["taskname"]
      updateForm.importance.data = row["importance"]
      updateForm.duration.data = row["duration"]

      return render_template("update.html", form=updateForm)

   if request.method == "POST":
      updateForm = AddTaskForm(request.form)
      newTitle = updateForm.taskName.data
      newImportance = updateForm.importance.data
      newDuration = updateForm.duration.data

      with sqlite.connect("tasks.sqlite") as con:
         con.row_factory = sqlite.Row
         cur=con.cursor()
         query = """ UPDATE Tasks SET taskname = "{}", importance = {}, duration = {} WHERE (ID = {})""".format(newTitle,newImportance,newDuration,id)
         cur.execute(query)
         con.commit() #database'e yapılan işlemlerin tamamlanması
      return redirect(url_for("index"))
      

@app.route("/about")
def about():
   return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


