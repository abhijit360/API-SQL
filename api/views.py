from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
import json, re
# Create your views here.

def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


@csrf_exempt
def get_data(request):
    if request.method == "GET":
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT name,phone,email,subject,message FROM contactResponse;")
            data = dictfetchall(cursor)

            user_dict = {}
            for index,datum in enumerate(data):
                name = datum['name']    
                phone = datum['phone']
                email = datum['email']
                subject = datum['subject']
                message = datum['message']
                user_dict[f"Request {index}"] = {'name':name, 'phone': phone , 'email': email, 'subject': subject, 'message':message}


            return JsonResponse({"status" : 100, "data":user_dict})
    
    if request.method =="POST":
        return JsonResponse({"status" : 101, "message":"POST request not allowed"})
    

@csrf_exempt
def post_request(request):
    if request.method =="GET":
        return JsonResponse({"status" : 101, "message":"GET request not allowed"})
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        phone = data['phone']
        email = data['email']
        subject = data['subject']
        message = data['message']

        error_array =[]

        if len(name) > 100:
             error_array.append("Name must be below 100 characters")
        if phone.isdigit():
            if len(phone) < 10 or len(phone) > 10:
                error_array.append("Phone must be 10 digits")
        else:
            error_array.append("Phone must contain only digits [0-9]")
        
        if not re.search('(\w+)@(\w+).com', email):
            error_array.append("Email format is incorrect")
        
        if len(subject) > 80:
            error_array.append("Subject must be below 80 characters")
        
        if len(message) > 1500:
            error_array.append("Message must be below 1500 characters")

        if len(error_array) > 0:
            return JsonResponse({"status" : 103, "errors":error_array})
        
        with connections["default"].cursor() as cursor:
            query = "INSERT INTO contactresponse (name, phone, email, subject, message) VALUES (%s, %s, %s, %s, %s)"
            values = (name, phone, email, subject, message)
            cursor.execute(query, values)
            return JsonResponse({"status" : 100, "message":"success"})


     
     
     