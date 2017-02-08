import cgi, cgitb
data= cgi.FieldStorage()
name = data.getvalue("name");
age = data.getvalue("age");
def printinfo( name, age ):
    print ("Name: ", name)
    print ("Age ", age)
    return name,age