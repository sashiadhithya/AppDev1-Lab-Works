from flask import Flask
from flask import request
from flask import render_template
from matplotlib import pyplot as plt

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def filetolist(fname):
    f = open(fname,'r')
    header = f.readline().strip().split(',')
    L = [ ]
    for line in f:
        D = dict()
        row = line.strip().split(',')
        for i in range(len(row)):
            val = row[i]
            D[header[i]] = val
        L.append(D)
    f.close()
    return L

array = filetolist('data.csv')

def check(array, first, second):
    students = [ ]
    courses = [ ]
    for i in array:
        students.append(i['Student id'])
        courses.append(i[' Course id'])
    if (first) not in ['-s','-c']:
        return False
    else:
        if (first) == '-c':
            if (' '+second) not in courses:
                return False
        else:
            if (second) not in students:
                return False
    return True

def student_details(array, second):
    L = [ ]
    for i in array:
        if i['Student id'] == second:
            L.append(i)
    return L

def totalmarks(L):
    total = 0
    for i in L:
        total += int(i[' Marks'])
    return total

def avgg(L):
    total, count = 0, 0
    for i in L:
        count += 1
        total += int(i)
    average = total/count 
    return(round(average, 2))

def maxi(L):
    maxi = 0
    for i in L:
        if int(i) > maxi:
            maxi = int(i)
    return maxi

def course_details(array, second):
    marks = [ ]
    for i in array:
        if (' '+second) == i[' Course id']:
            marks.append(i[' Marks'].strip(' '))
    return sorted(marks)
    
def histogram(L):
    fig, ax = plt.subplots(figsize =(10, 7))
    ax.hist(L)
    plt.ylabel('Frequency',fontsize=12)
    plt.xlabel('Marks',fontsize=12)
    plt.savefig('static\histogram.png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

@app.route("/", methods = ['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        option = request.form['ID']
        id_value = request.form['id_value']
        back = request.referrer
        if option == 'student_id':
            if check(array, '-s', id_value):
                ans = student_details(array, id_value)
                total = totalmarks(ans)
                return render_template('student_details_template.html', student_id = id_value, ans = ans, total = total, back=back)
            else:
                return render_template('error_template.html', back=back)
        elif option == 'course_id':
                if check(array, '-c', id_value):
                    ans = course_details(array, id_value)
                    maximum = maxi(ans)
                    average = avgg(ans)
                    histogram(ans)
                    return render_template('course_details_template.html', course_id = id_value, average = average, maximum = maximum, back=back, url='static\histogram.png')
                else:
                    return render_template('error_template.html', back=back)
        else:
            return render_template('error_template.html', back=back)
                
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                