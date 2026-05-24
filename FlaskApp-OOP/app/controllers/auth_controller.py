from flask import render_template, request
class AuthController:
    def login(self):
        if request.method=="POST":
            print (request.form)

        return render_template("login.html")

        
    def register(self):
        return render_template("register.html")
    def home(self):
       product=[
          {"name":"mobile","price":"120k","modal":"s24"},
          {"name":"mobile1","price":"12k","modal":"s24"},
          {"name":"mobile2","price":"13k","modal":"s24"},
          {"name":"mobile3","price":"140k","modal":"s24"},
          {"name":"mobile4","price":"150k","modal":"s24"},
          
       ]
       return render_template("home.html",product=product)