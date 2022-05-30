import sys
from matplotlib import pyplot as plt
from jinja2 import Template

student_details_template ='''
<!DOCTYPE html>
<html>
    <body>
        <div class="main">
            <h1> Student Details </h1>
            <table style ="border: 1px solid black;">
                <thead>
                <tr>
                    <th style ="border: 1px solid black;"> Student id </th>
                    <th style ="border: 1px solid black;"> Course id </th>
                    <th style ="border: 1px solid black;"> Marks </th>
                </tr>
                </thead>
                <tbody>
                    {% for i in ans %}
                    <tr style ="border: 1px solid black;">
                        <td style ="border: 1px solid black;">{{ i['Student id'] }}</td>
                        <td style ="border: 1px solid black;">{{ i[' Course id'] }}</td>
                        <td style ="border: 1px solid black;">{{ i[' Marks'] }}</td>
                    </tr>
                    {% endfor %}
                    <tr style ="border: 1px solid black;">
                        <td colspan ="2" align = 'center' style ="border: 1px solid black;"> Total Marks </td>
                        <td style ="border: 1px solid black;"> {{ total }} </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
</html>
'''

course_details_template ='''
<!DOCTYPE html>
<html>
    <body>
        <div id="header">
            <h1> Course Details </h1>
        </div>
        <div id="table">
            <table style ="border: 1px solid black;">
                <thead>
                <tr>
                    <th style ="border: 1px solid black;"> Average Marks </th>
                    <th style ="border: 1px solid black;"> Maximum Marks </th>
                </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style ="border: 1px solid black;">{{ average }}</td>
                        <td style ="border: 1px solid black;">{{ maximum }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div id="histogram">
                <img src="histogram.png">
        </div>
    </body>
</html>
'''

error_template='''
<!DOCTYPE html>
<html>
    <body>
        <div id="header">
            <h1> Wrong Inputs </h1>
        </div>
        <div id="content">
            <p> Something went wrong </p>
        </div>
    </body>
</html>
'''

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
            marks.append(i[' Marks'])
    return marks
    
def histogram(L):
    fig, ax = plt.subplots(figsize =(10, 7))
    ax.hist(L)
    plt.ylabel('Frequency',fontsize=12)
    plt.xlabel('Marks',fontsize=12)
    plt.savefig('histogram.png')
    plt.close(fig)
    
first = sys.argv[1]
second = sys.argv[2]

def main():
    array = filetolist('data.csv')
    if check(array, first, second):
        if first == '-s':
            ans = student_details(array, second)
            total = totalmarks(ans)
            template = Template(student_details_template)
            content = (template.render(ans=ans, total=total))
            my_html_file = open('output.html', 'w')
            my_html_file.write(content)
            my_html_file.close()
          
        else:
            ans = course_details(array, second)
            maximum = maxi(ans)
            average = avgg(ans)
            histogram(ans)
            template = Template(course_details_template)
            content = (template.render(average=average, maximum=maximum))
            my_html_file = open('output.html', 'w')
            my_html_file.write(content)
            my_html_file.close()
          
    else:
        template = Template(error_template)
        content = (template.render())
        my_html_file = open('output.html', 'w')
        my_html_file.write(content)
        my_html_file.close()
            
if __name__ == '__main__':
    main()