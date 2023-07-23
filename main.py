import re
import requests
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
import datetime

with open("FENS_Output.txt",'wt') as f :
    # urls=["https://www.fens.org/careers/job-market","https://www.fens.org/careers/job-market/page/2",
    #     "https://www.fens.org/careers/job-market/page/3","https://www.fens.org/careers/job-market/page/4"]

    urls=["https://www.fens.org/careers/job-market"]
    for url in urls:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()
        print("REQUEST SENT!")

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        href_tags = soup.find_all(href=True)

        job_links=[]
        job_url=[]
        for i in range(len(href_tags)):
            fullstring = str(href_tags[i])
            substring = "https://www.fens.org/careers/job-market/job/"
            try:
                fullstring.index(substring)
            except ValueError:
                continue
            else:
                # print(fullstring)
                job_links.append(fullstring)

        print("JOBS FETCHED!")
        for k in range(len(job_links)):
            if re.sub('<[^<]+?>', '', str(job_links[k])).isdigit():
                url_job="https://www.fens.org/careers/job-market/job/" + re.sub('<[^<]+?>', '', str(job_links[k])) + "/"
                print(url_job,file=f)
                
                # Send a request to the URL
                response = requests.get(url_job)
                response.raise_for_status()

                # Parse the content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                #Get title
                title_tags = soup.find_all('title')
                title=str(title_tags).split('>')[1].split('<')[0]
                print("Title: ",title,file=f)
                keywords=['<p>Job ID:','<p><b>Position:','<p><b>Deadline:',
                        '<p><b>Employment Start Date:','<p><b>Country:','<p><b>Institution:','URL:']
                data=[]
                for j in range(len(list(soup.find_all('p')))):
                    for keys in keywords:
                        if str(soup.find_all('p')[j]).find(keys) != -1:
                            #print(soup.find_all('p')[j])
                            print(re.sub('<[^<]+?>', '',str(soup.find_all('p')[j])),file=f)
                
                print('\n',file=f)
                print('URL:',url_job,' DONE!')


# using now() to get current time
current_time = datetime.datetime.now()

msg = EmailMessage()
msg["From"] = 'ihiteshpradhan@gmail.com'
msg["Subject"] = "FENS"+"_"+ str(current_time.day) + "_" + str(current_time.month) + "_" + str(current_time.year)
#msg["To"] = "fens_scrappingtest@googlegroups.com"
msg["To"] = "htshpradhan5@gmail.com"
msg.set_content("Please find attached the FENS weekly update")
msg.add_attachment(open('FENS_Output.txt', "r").read(), filename="FENS_Output.txt")

s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login('ihiteshpradhan@gmail.com', SOME_SECRET)
s.send_message(msg)