from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

login_data = {
    '__RequestVerificationToken': '',
    'SCKTY00328510CustomEnabled': True,
    'SCKTY00436568CustomEnabled': True,
    'Database': 10,
    'VerificationOption': 'UsernamePassword',
    'LogOnDetails.UserName': '',
    'tempUN': '',
    'tempPW': '',
    'LogOnDetails.Password': ''
}

def getAssignments(login_data):
    with requests.Session() as ses:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = ses.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = ses.post(login_url, data=login_data)
        classes = []
        averages = []

        finaldata = {}
        string = ''

        assignments = ses.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx')
        content = BeautifulSoup(assignments.text, 'lxml')

        for x in content.find_all('div', class_='AssignmentClass'):
            header = x.find('div', class_="sg-header")
            q = header.find('a', class_='sg-header-heading').text.strip()[12:]
            w = header.find('span', class_='sg-header-heading')
            classes.append(q.strip())
            averages.append(w.text.strip()[18:])

        string += ('\n\nClass Averages:\n')
        for i in range(len(classes)):
            string += ("\n" + classes[i] + " - " + averages[i])

        finaldata['classes'] = classes
        finaldata['averages'] = averages
        print(averages)
        assignmentstable = []
        assignmentsrow = []

        finaldata['assignment'] = []
        finaldata['categories'] = []
        for x in content.find_all('div', class_='AssignmentClass'):
            table = x.find('table', class_='sg-asp-table')
            if table is not None:
                for j in x.find_all('table', class_='sg-asp-table'):
                        for row in j.find_all('tr'):
                            for element in row.find_all('td'):
                                text = element.text.strip()
                                text = text.replace("*", "")
                                assignmentsrow.append(text.strip())
                            assignmentstable.append(assignmentsrow)
                            assignmentsrow = []
                        if 'CourseCategories' in j.attrs['id']:
                            finaldata['categories'].append(assignmentstable)
                        elif 'CourseAssignments' in j.attrs['id']:
                            finaldata['assignment'].append(assignmentstable)
                        assignmentstable = []
            else:
                finaldata['assignment'].append([])
                finaldata['categories'].append([])
        ret = {}
        for i in range(len(classes)):
            average = averages[i]
            assig = finaldata['assignment'][i]
            categories = finaldata['categories'][i]
            l = {}
            l['average'] = average
            l['assignments'] = assig
            l['categories'] = categories
            ret[classes[i]] = l
        return ret

def getInfo(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        ret = {}
        assignments = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Registration.aspx')
        content = BeautifulSoup(assignments.text, 'lxml')
        ret['name'] = content.find('span', id='plnMain_lblRegStudentName').text.strip()
        ret['grade'] = content.find('span', id='plnMain_lblGrade').text.strip()
        ret['school'] = content.find('span', id='plnMain_lblBuildingName').text.strip()
        ret['dob'] = content.find('span', id='plnMain_lblBirthDate').text.strip()
        ret['councelor'] = content.find('span', id='plnMain_lblCounselor').text.strip()
        ret['language'] = content.find('span', id='plnMain_lblLanguage').text.strip()
        ret['cohort-year'] = content.find('span', id='plnMain_lblCohortYear').text.strip()
        return ret

def getAssignmentClass(login_data,class_name):
    with requests.Session() as ses:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = ses.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = ses.post(login_url, data=login_data)
        classes = []
        averages = []

        finaldata = {}
        string = ''

        assignments = ses.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx')
        content = BeautifulSoup(assignments.text, 'lxml')

        for x in content.find_all('div', class_='AssignmentClass'):
            header = x.find('div', class_="sg-header")
            q = header.find('a', class_='sg-header-heading').text.strip()[12:]
            w = header.find('span', class_='sg-header-heading')
            classes.append(q.strip())
            averages.append(w.text.strip()[18:])

        string += ('\n\nClass Averages:\n')
        for i in range(len(classes)):
            string += ("\n" + classes[i] + " - " + averages[i])

        finaldata['classes'] = classes
        finaldata['averages'] = averages
        print(averages)
        assignmentstable = []
        assignmentsrow = []

        finaldata['assignment'] = []
        finaldata['categories'] = []
        for x in content.find_all('div', class_='AssignmentClass'):
            table = x.find('table', class_='sg-asp-table')
            if table is not None:
                for j in x.find_all('table', class_='sg-asp-table'):
                        for row in j.find_all('tr'):
                            for element in row.find_all('td'):
                                text = element.text.strip()
                                text = text.replace("*", "")
                                assignmentsrow.append(text.strip())
                            assignmentstable.append(assignmentsrow)
                            assignmentsrow = []
                        if 'CourseCategories' in j.attrs['id']:
                            finaldata['categories'].append(assignmentstable)
                        elif 'CourseAssignments' in j.attrs['id']:
                            finaldata['assignment'].append(assignmentstable)
                        assignmentstable = []
            else:
                finaldata['assignment'].append([])
                finaldata['categories'].append([])
        ret = {}
        for i in range(len(classes)):
            if(classes[i] == class_name):
                average = averages[i]
                assig = finaldata['assignment'][i]
                categories = finaldata['categories'][i]
                l = {}
                l['average'] = average
                l['assignments'] = assig
                l['categories'] = categories
                ret[classes[i]] = l
                return ret

        return json.dumps({"error":"class not found"}), 404, {'ContentType':'application/json'}

def getAverages(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        classes = []
        averages = []
        assignments = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx')
        content = BeautifulSoup(assignments.text, 'lxml')

        for x in content.find_all('div', class_='AssignmentClass'):
            header = x.find('div', class_="sg-header")
            q = header.find('a', class_='sg-header-heading').text.strip()[12:]
            w = header.find('span', class_='sg-header-heading')
            classes.append(q.strip())
            averages.append(w.text.strip()[18:])

        ret = {}
        for i in range(len(classes)):
            ret[classes[i]] = averages[i]
        return ret

def getClasses(login_data):
    with requests.Session() as session:
        print('faslkdfjlakjd')
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        classes = []
        assignments = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx')
        content = BeautifulSoup(assignments.text, 'lxml')

        for x in content.find_all('div', class_='AssignmentClass'):
            header = x.find('div', class_="sg-header")
            q = header.find('a', class_='sg-header-heading').text.strip()[12:]
            classes.append(q.strip())

        ret = {}
        ret['classes'] = classes
        return ret

def getReport(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        finaldata = {}
        reportcard = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/ReportCards.aspx')
        reportcardcontent = BeautifulSoup(reportcard.text, 'lxml')
        headers = ['Course', 'Description', 'Period', 'Teacher', 'Room', '1st', '2nd', '3rd', 'Exam1', 'Sem1', '4th', '5th', '6th', 'Exam2', 'Sem2', 'CND1', 'CND2', 'CND3', 'CND4', 'CND5', 'CND6']
        row = []
        data = []
        finaldata['headers'] = headers
        counter = 0
        for x in reportcardcontent.find_all('td'):
            counter += 1
            # if counter <= 32:
            #     headers.append(x.text.strip())
            if counter > 32:
                row.append(x.text.strip())
            if (len(row) % 32 == 0) and (counter > 32):
                data.append(row)
                row = []
        for j in data:
            del j[31]
            del j[30]
            del j[29]
            del j[28]
            del j[27]
            del j[26]
            del j[25]
            del j[24]
            del j[23]
            del j[6]
            del j[5]
        finaldata['data'] = data
        return finaldata

def getProgressReport(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        finaldata = {}
        string = ''
        reportcard = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/InterimProgress.aspx')
        reportcardcontent = BeautifulSoup(reportcard.text, 'lxml')

        headers = []
        row = []
        data = []
        for x in reportcardcontent.find_all('tr'):
            for c in x.find_all('td'):
                row.append(c.text.strip())
            data.append(row)
            row = []
        headers = data[0]
        data.pop(0)
        finaldata['headers'] = headers
        finaldata['data'] = data
        return finaldata

def getTranscript(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'lxml')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        finaldata = []
        year = []
        semester = []
        transcript = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Transcript.aspx')
        content = BeautifulSoup(transcript.text, 'lxml')
        with open('transcript.html', 'w') as f:
            f.write(str(content))
        transcript = {}
        
        for x in content.find_all('td', class_='sg-transcript-group'):
            semester = {}
            table1 = x.find_next('table')
            table2 = table1.find_next('table')
            table3 = table2.find_next('table')
            for y in table1.find_all('span'):
                if "YearValue" in y.attrs['id']:
                    semester['year'] = y.text.strip()
                if "GroupValue" in y.attrs['id']:
                    semester['semester'] = y.text.strip()
                if "GradeValue" in y.attrs['id']:
                    semester['grade'] = y.text.strip()
                if "BuildingValue" in y.attrs['id']:
                    semester['school'] = y.text.strip()
            data = []
            semester['data'] = []
            for z in table2.find_all('tr'):
                if "sg-asp-table-header-row" in z.attrs['class']:
                    for a in z.find_all('td'):
                        data.append(a.text.strip())
                    semester['data'].append(data)
                    data = []
                if "sg-asp-table-data-row" in z.attrs['class']:
                    for a in z.find_all('td'):
                        data.append(a.text.strip())
                    semester['data'].append(data)
                    data = []
            for z in table3.find_all('label'):
                if "CreditValue" in z.attrs['id']:
                    semester['credits'] = z.text.strip()
            transcript[semester['year'] + " - Semester "+ semester['semester']] = semester
        x = content.find('table', id='plnMain_rpTranscriptGroup_tblCumGPAInfo')
        for y in x.find_all('tr', class_="sg-asp-table-data-row"):
            for z in y.find_all('span'):
                if "GPADescr" in z.attrs['id']:
                    num = z.find_next('span')
                    text = z.text.strip()
                    transcript[text] = num.text.strip()
        return transcript


@app.route('/', methods=['GET'])
def home():
    return json.dumps({'success': True, 'message': 'This is the home page'}), 200, {"Content-Type": "application/json"}

@app.route('/help', methods=['GET'])
def help():
    return json.dumps({'message': 'Official documentation for this API is available at https://homeaccesscenterapi-docs.vercel.app'}), 200, {"Content-Type": "application/json"}

@app.route('/api/classes', methods=['GET'])
def classes():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        content = getClasses(data)
        return json.dumps(content), 200, {"Content-Type": "application/json"}

@app.route("/api/ipr", methods=['GET'])
def ipr():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        content = getProgressReport(data)
        return json.dumps(content), 200, {"Content-Type": "application/json"}

@app.route("/api/reportcard", methods=['GET'])
def reportcard():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        content = getReport(data)
        return json.dumps(content), 200, {"Content-Type": "application/json"}
        
@app.route("/api/averages", methods=['GET'])
def averages():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        content = getAverages(data)
        return json.dumps(content), 200, {"Content-Type": "application/json"}
        
@app.route("/api/assignments", methods=['GET'])
def assignments():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        if 'class' in request.args:
            content = handlers.getAssignmentClass(data, request.args['class'])
            return json.dumps(content), 200, {"Content-Type": "application/json"}
        content = getAssignments(data) 
        return json.dumps(content), 200, {"Content-Type": "application/json"}
        
@app.route("/api/info", methods=['GET'])
def info():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        content = getInfo(data)
        return json.dumps(content), 200, {"Content-Type": "application/json"}

@app.route('/api/transcript')
def transcript():
    if 'user' in request.args and 'pass' in request.args:
        data = login_data
        data['LogOnDetails.UserName'] = request.args['user']
        data['LogOnDetails.Password'] = request.args['pass']
        content = getTranscript(data)
        return json.dumps(content), 200, {"Content-Type": "application/json"}

@app.route('/api/')
def transcript():
    return json.dumps({'success': True, 'message': 'This is the home page'}), 200, {"Content-Type": "application/json"}
