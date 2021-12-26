from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,logout,login
from .models import TaskList
from .form import TaskForm
from django.core.paginator import Paginator
from django.contrib import messages
import datetime
from datetime import datetime, timedelta
import re
import statistics
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator

# Create your views here.
formateddate = ''
year = ''
month = ''

def index(request):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:
            if request.method == 'POST':
                request.session['formateddate'] = request.POST['date']
                if request.session['formateddate']:
                    tasks = TaskList.objects.filter(CreatedDate=request.session['formateddate'])
                    return render(request,'index.html', {
                        "tasks": tasks,
                        "newtask": True
                    })
            if request.method == 'GET':
                sessiondate = request.session.get('formateddate')
                if sessiondate:
                    tasks = TaskList.objects.filter(CreatedDate=sessiondate)
                    return render(request, 'index.html', {
                        "tasks": tasks,
                        "newtask": True
                    })

            return render(request, 'index.html',{
                "newtask": False
            })

def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dailyplanningboard:analytics')
            else:
                return render(request, 'login.html', {
                    "message": "Incorrect Credentials !!!"
                })

        else:
            return render(request, 'login.html')

def logout_view(request):
        logout(request)
        return render(request, 'login.html', {
            "message": "Logged Out !!!"
        })


def edittask(request, id):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:

            if request.method == 'POST':
                task = TaskList.objects.get(pk=id)
                updatedtask = TaskForm(request.POST or None,instance=task)
                if updatedtask.is_valid():
                    updatedtask.save()
                    return redirect('dailyplanningboard:index')

            else:
                tasks = TaskList.objects.filter(pk=id)
                lastactivity = datetime.today().strftime('%m/%d/%Y')
                return render(request, 'edittask.html', {
                    "retrievetask": tasks,
                    "lastactivity": lastactivity
                })


def customedit(request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:

            if request.method == 'POST':
                task = TaskList.objects.get(pk=id)
                updatedtask = TaskForm(request.POST or None, instance=task)
                if updatedtask.is_valid():
                    updatedtask.save()
                    return redirect('dailyplanningboard:custom')

            else:
                tasks = TaskList.objects.filter(pk=id)
                lastactivity = datetime.today().strftime('%m/%d/%Y')
                return render(request, 'customedit.html', {
                    "retrievetask": tasks,
                    "lastactivity": lastactivity
                })

def addtask(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:

            if request.method == 'POST':
                UnitSystem = request.POST['UnitSystem']
                Department = request.POST['Department']
                Permit = request.POST['Permit']
                SAPNum = request.POST['SAPNum']
                Description = request.POST['Description']
                Remarks = request.POST['Remarks']
                Priority = request.POST['Priority']
                Status = request.POST['Status']
                CreatedDate = request.session.get('formateddate')
                LastActivity = datetime.today().strftime('%m/%d/%Y')
                pattern_match = re.match(r"([0-9]+)/([0-9]+)/([0-9]+)", request.session.get('formateddate'))
                MonthYearID = pattern_match.group(1)+pattern_match.group(3)

                if Priority and Status and UnitSystem:
                    task = TaskList(UnitSystem=UnitSystem,Department=Department,Permit=Permit,SAPNum=SAPNum,Description=Description,Remarks=Remarks,Priority=Priority,Status=Status,CreatedDate=CreatedDate,LastActivity=LastActivity,MonthYearID=MonthYearID)
                    task.save()
                    messages.success(request,("New Task Added!!"))
                else:
                    messages.warning(request,("New Task not saved. UnitSystem or Priority or Status field is empty. Please fill these values"))

            return render(request,'addtask.html')


def deletetask(request):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:

            if request.method == 'POST':

                try:
                    deletemode = request.POST['flexRadioDefault']
                    deletevalue = request.POST[deletemode]
                except:
                    return render(request, 'deletetask.html',{
                        "messages": "No delete option was selected !!!"
                    })

                if deletevalue:
                    if deletemode == 'dbid':
                       task = TaskList.objects.filter(pk=deletevalue)
                    if deletemode == 'monthid':
                       task = TaskList.objects.filter(MonthYearID=deletevalue)
                    if deletemode == 'dayid':
                        task = TaskList.objects.filter(CreatedDate=deletevalue)

                    if len(task) == 0:
                        return render(request, 'deletetask.html', {
                            "messages": "No tasks available to delete!!!"
                        })
                    else:
                        task.delete()
                        return render(request, 'deletetask.html', {
                            "messages": "Successfully Deleted!!!"})

                else:
                    return render(request, 'deletetask.html', {
                        "messages": "No value specified. Please enter a delete value!!!"
                    })

            return render(request,'deletetask.html')


def custom(request):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:

            if request.method == 'POST':
                dates = request.POST.getlist('date')

                if (dates[0] == '') or (dates[1] == ''):
                    pass

                else:
                    radiooption = request.POST['flexRadioDefault']
                    date_format = "%m/%d/%Y"
                    from_date = datetime.strptime(dates[0], date_format)
                    to_date = datetime.strptime(dates[1], date_format)
                    delta_date = to_date - from_date
                    days = [from_date + timedelta(days=i) for i in range(delta_date.days + 1)]
                    numofdates = []


                    for i in range(delta_date.days + 1):
                        numofdates.append(days[i].strftime("%m%d%Y"))

                    if request.POST['flexRadioDefault'] == 'alltask':
                        tasks_all = TaskList.objects.filter(CreatedDate__range=[dates[0], dates[1]]).order_by('CreatedDate')
                        paginator_post = Paginator(tasks_all, 50)
                        page = request.POST.get('pg')
                        tasks_all = paginator_post.get_page(page)
                        return render(request,'custom.html',{
                            "tasks":tasks_all,
                            "paginations": True
                    })
                    if request.POST['flexRadioDefault'] == 'onlyopentask':
                        tasks_open = TaskList.objects.filter(CreatedDate__range=[dates[0], dates[1]]).filter(Status='Open')
                        return render(request,'custom.html',{
                            "tasks":tasks_open
                    })
                    if request.POST['flexRadioDefault'] == 'onlyinprogresstask':
                        tasks_inprogress = TaskList.objects.filter(CreatedDate__range=[dates[0], dates[1]]).filter(Status='Inprogress')
                        return render(request,'custom.html',{
                            "tasks":tasks_inprogress
                    })
                    if request.POST['flexRadioDefault'] == 'onlyhighprioritytask':
                        tasks_high = TaskList.objects.filter(CreatedDate__range=[dates[0], dates[1]]).filter(Priority='High')
                        return render(request,'custom.html',{
                            "tasks":tasks_high
                    })

            else:
                currentmonth = str(datetime.now().month)
                currentyear = str(datetime.now().year)
                fromdate = currentmonth + "/01/" + currentyear
                todate = currentmonth + "/31/" + currentyear
                alltasks = TaskList.objects.filter(CreatedDate__range=[fromdate, todate]).order_by('CreatedDate')

                paginator_get = Paginator(alltasks, 50)
                page = request.GET.get('pg')
                alltasks = paginator_get.get_page(page)
                return render(request, 'custom.html', {
                    "tasks": alltasks,
                    "paginations": True
                })

            return render(request,'custom.html')


def analytics(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dailyplanningboard:login'))

        else:
            if request.method == 'POST':
                analytics_months = request.POST['month']
                analytics_years = request.POST['year']
                if analytics_months == 'Month' or analytics_years == 'Year':
                    analytics_months = str(datetime.now().month)
                    analytics_years = str(datetime.now().year)
            else:
                analytics_months = str(datetime.now().month)
                analytics_years = str(datetime.now().year)

            date = [analytics_months + '/01/' + analytics_years, analytics_months + '/02/' + analytics_years,
                    analytics_months + '/03/' + analytics_years, analytics_months + '/04/' + analytics_years,
                    analytics_months + '/05/' + analytics_years, analytics_months + '/06/' + analytics_years,
                    analytics_months + '/07/' + analytics_years, analytics_months + '/08/' + analytics_years,
                    analytics_months + '/09/' + analytics_years, analytics_months + '/10/' + analytics_years,
                    analytics_months + '/11/' + analytics_years, analytics_months + '/12/' + analytics_years,
                    analytics_months + '/13/' + analytics_years, analytics_months + '/14/' + analytics_years,
                    analytics_months + '/15/' + analytics_years, analytics_months + '/16/' + analytics_years,
                    analytics_months + '/17/' + analytics_years, analytics_months + '/18/' + analytics_years,
                    analytics_months + '/19/' + analytics_years, analytics_months + '/20/' + analytics_years,
                    analytics_months + '/21/' + analytics_years, analytics_months + '/22/' + analytics_years,
                    analytics_months + '/23/' + analytics_years, analytics_months + '/24/' + analytics_years,
                    analytics_months + '/25/' + analytics_years, analytics_months + '/26/' + analytics_years,
                    analytics_months + '/27/' + analytics_years, analytics_months + '/28/' + analytics_years,
                    analytics_months + '/29/' + analytics_years, analytics_months + '/30/' + analytics_years,
                    analytics_months + '/31/' + analytics_years
                    ]
            dailytask = []
            for i in range(len(date)):
                task = TaskList.objects.filter(CreatedDate=date[i])
                dailytask.append(len(task))

            status_open = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Status='Open')
            status_closed = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Status='Completed')
            status_inprogress = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Status='Inprogress')
            priority_high = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Priority='High')
            priority_medium = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Priority='Medium')
            priority_low = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Priority='Low')

            priority_high_open = task = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Priority='High').filter(
                Status='Open')
            priority_high_inprogress = task = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(
                Priority='High').filter(Status='Inprogress')
            priority_high_closed = task = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(
                Priority='High').filter(Status='Completed')

            priority_medium_closed = task = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(
                Priority='Medium').filter(
                Status='Completed')
            priority_low_closed = task = TaskList.objects.filter(MonthYearID=analytics_months+analytics_years).filter(Priority='Low').filter(
                Status='Completed')

            unitsysname = []
            unitsyscount = []
            unitsyscomponents = task = TaskList.objects.filter(MonthYearID=analytics_months + analytics_years).values(
                'UnitSystem').annotate(dcount=Count('UnitSystem'))
            for unitsys in unitsyscomponents:
                unitsysname.append(unitsys['UnitSystem'])
                unitsyscount.append(unitsys['dcount'])

            high_delta_dates = []
            medium_delta_dates = []
            low_delta_dates = []

            for i, c in enumerate(priority_high_closed):
                date_format = "%m/%d/%Y"
                close_date = datetime.strptime(c.LastActivity, date_format)
                create_date = datetime.strptime(c.CreatedDate, date_format)
                delta_date = close_date - create_date
                if delta_date.days is not None:
                    high_delta_dates.append(delta_date.days)
                else:
                    high_delta_dates.append(0)
            for i, c in enumerate(priority_medium_closed):
                date_format = "%m/%d/%Y"
                close_date = datetime.strptime(c.LastActivity, date_format)
                create_date = datetime.strptime(c.CreatedDate, date_format)
                delta_date = close_date - create_date
                if delta_date.days is not None:
                    medium_delta_dates.append(delta_date.days)
                else:
                    medium_delta_dates.append(0)
            for i, c in enumerate(priority_low_closed):
                date_format = "%m/%d/%Y"
                close_date = datetime.strptime(c.LastActivity, date_format)
                create_date = datetime.strptime(c.CreatedDate, date_format)
                delta_date = close_date - create_date
                if delta_date.days is not None:
                    low_delta_dates.append(delta_date.days)
                else:
                    low_delta_dates.append(0)

            if len(priority_high_open) == 0 or len(priority_medium_closed) == 0 or len(priority_low_closed) == 0:
                messages.warning(request, (
                    "Not enough datapoints to display all charts!!!"))
                return render(request, 'analytics.html',{
                               "status_open": len(status_open),
                                "status_closed": len(status_closed),
                                "status_inprogress": len(status_inprogress),
                                "priority_high": len(priority_high),
                                "priority_medium": len(priority_medium),
                                "priority_low": len(priority_low),
                                "priority_high_open": len(priority_high_open),
                                "priority_high_inprogress": len(priority_high_inprogress),
                                "priority_high_closed": len(priority_high_closed),
                                "unitsysname": unitsysname,
                                "unitsyscount": unitsyscount,
                                "dailytask": dailytask,
                })
            else:

                return render(request, 'analytics.html', {
                    "status_open": len(status_open),
                    "status_closed": len(status_closed),
                    "status_inprogress": len(status_inprogress),
                    "priority_high": len(priority_high),
                    "priority_medium": len(priority_medium),
                    "priority_low": len(priority_low),
                    "priority_high_open": len(priority_high_open),
                    "priority_high_inprogress": len(priority_high_inprogress),
                    "priority_high_closed": len(priority_high_closed),
                    "high_delta_dates": statistics.mean(high_delta_dates),
                    "medium_delta_dates": statistics.mean(medium_delta_dates),
                    "low_delta_dates": statistics.mean(low_delta_dates),
                    "unitsysname": unitsysname,
                    "unitsyscount": unitsyscount,
                    "dailytask": dailytask,

                })


