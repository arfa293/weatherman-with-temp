
from django.http import HttpResponse
from django.shortcuts import render , redirect
from .classes import Fileparser,Calculation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    year = int(request.GET.get("year", 2024)) 
    month = int(request.GET.get("month", 1))  

    parser = Fileparser()
    files = parser.get_files_by_year(year)
    
    all_data = []
    required_columns = ["PKT", "PKST", "Max TemperatureC", "Min TemperatureC", "Max Humidity", "Min Humidity", "Mean Humidity"]
    
    for file in files:
        all_data.extend(parser.get_file_data(file, required_columns))

    calc = Calculation(all_data)
    
    avg_max_temp = calc.average_max_temperature(year, month)
    avg_min_temp = calc.average_min_temp(year, month)

    
    highest_temp = calc.get_max_temperature()  
    lowest_temp = calc.get_min_temperature()  
    most_humid_day = calc.get_max_huimidity()  

    
    avg_max_temp = int(avg_max_temp) if isinstance(avg_max_temp, (int, float)) else 0
    avg_min_temp = int(avg_min_temp) if isinstance(avg_min_temp, (int, float)) else 0

    
    max_temp_stars = "*" * avg_max_temp
    min_temp_stars = "*" * avg_min_temp

    context = {
        "year": year,
        "month": month,
        "avg_max_temp": avg_max_temp,
        "avg_min_temp": avg_min_temp,
        "max_temp_stars": max_temp_stars,
        "min_temp_stars": min_temp_stars,
        "highest_temp": highest_temp,
        "lowest_temp": lowest_temp,
        "most_humid_day": most_humid_day,
    }
    
    return render(request, "weather_report.html", context)
@login_required
def save(request):
    if request.method == "POST":
        date = request.POST.get("date")
        if not date:
            return HttpResponse("Date is required") 

        max_temp = request.POST.get("max_temperature")
        min_temp = request.POST.get("min_temperature")
        humidity = request.POST.get("humidity")
        max_humidity = request.POST.get("max_humidity")
        min_humidity = request.POST.get("min_humidity")

        obj, created = WeatherRecord.objects.get_or_create(
            date=date,
            defaults={
                "min_Temperature": min_temp,
                "max_Temperature": max_temp,
                "humidity": humidity,
                "max_Humidity": max_humidity,
                "min_humidity": min_humidity,
            }
        )

        message = "Created successfully" if created else "Record already exists"

        return render(request, "weather_form.html", {"message": message})

    # If the request method is GET, return the form page
    return render(request, "weather_form.html")           

@login_required(login_url='login')
def weather_data(request):
    record=WeatherRecord.objects.all()
    return render(request,"weather_list.html",{"records":record})

def delete_data(request, record_id):
    try:
        record = WeatherRecord.objects.get(id=record_id)
        record.delete()
        return HttpResponse("Record deleted successfully.")
    except WeatherRecord.DoesNotExist:
        return HttpResponse("Record not found.", status=404)
    
def signup_page(request):
    if request.method == "POST":
        username=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confpassword=request.POST.get("confirm-password")
        if password != confpassword:
            return HttpResponse("password does not match")
        if User.objects.filter(username=username).exists():
            return HttpResponse("user name alredy exist")
        my_user=User.objects.create_user(username=username,email=email,password=password)
        my_user.save()
        return HttpResponse("signup sucessfully") 
    return render(request,"signup.html")  

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)  
        except User.DoesNotExist:
            return HttpResponse("No user found with this email.")

        authenticated_user = authenticate(request, username=user.username, password=password) 

        if authenticated_user is not None:
            login(request, authenticated_user) 
            return redirect("weather-form")
        else:
            return HttpResponse("Invalid credentials, try again.")

    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("login")