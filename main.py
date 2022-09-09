import sys
import os
import csv
import time
from tkinter import N
from google_play_scraper import app
from google_play_scraper import search
from google_play_scraper import permissions

# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv)-1)
# print("The arguments are: " , str(sys.argv))

#default_path = 'C:\\Users\\Hack_Rider\\Documents\\CCToolkit\\Keywords\\'
default_path =os.getcwd()+'\\Keywords\\'
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("app scanning stated at time: ",timestr)



# this is for banner

is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console , colorama
        win_unicode_console.enable()
        colorama.init()
        #Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed, no coloring will be used [Check the readme]")
        G = Y = B = R = W = G = Y = B = R = W = ''


else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white

def no_color():
    global G, Y, B, R, W
    G = Y = B = R = W = ''


def banner():
    print("""%s
      ____ ____ _____           _ _    _ _   
     / ___/ ___|_   _|__   ___ | | | _(_) |_ 
    | |  | |     | |/ _ \ / _ \| | |/ / | __|
    | |__| |___  | | (_) | (_) | |   <| | |_ 
     \____\____| |_|\___/ \___/|_|_|\_\_|\__|%s%s

                # Coded By IIT Kanpur - @ninja_pandit_
    """ % (R, W, Y))
    
# Banner completed





def filter_currency_developer(orglist):
    count=1
    result = []
    for app in orglist:
        # if(app['currency'] == 'INR'):
            # if(app['developerEmail'] == '' or app['developerEmail'].endswith('@gmail.com') or app['developerEmail'].endswith('@hotmail.com') or app['developerEmail'].endswith('@yahoo.com')):
        if(app['developerEmail'].endswith('@gmail.com') or app['developerEmail'].endswith('@hotmail.com') or app['developerEmail'].endswith('@yahoo.com')):
            result.append(app)
            print("\n\nSuspected App Number: ",count)
            count+=1
            print("App Title : ",app['title'])
            print("google Play URL: \n")
            x='https://play.google.com/store/apps/details?id=' + app['appId']
            print(x)
            print("\n")
    print("\nTotal Suspected apps ",count-1)
    return result

def search_apps(query):

    result = search(query, country="in", n_hits=100)
    return result

#writting results in csv file

def csv_export(filtered_list,name,path):
    url='https://play.google.com/store/apps/details?id='
    name1=path+"\\output\\"+name+timestr+'.csv'
    #print(name1)
    header=['Title','URL','icon','Installed','ReleaseDate','Genre','Summarry','Devloper','DevloperID','DevloperEmail','DevloperWebsite','DevloperAddress','Ratings','Reviews','Description']


    f=open(name1, 'a', encoding='UTF8', newline="")
        
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    

    for apps in filtered_list:
            data = [apps['title'], url+apps['appId'], apps['icon'], apps['installs'],apps['released'],apps['genre'],apps['summary'],apps['developer'],apps['developerId'],apps['developerEmail'],apps['developerWebsite'],apps['developerAddress'],apps['ratings'],apps['reviews'],apps['description']]
              # write the data
            writer.writerow(data)
    print("Result is written in the CSV file: ",name1)
    f.close()
    

def appdetails(terms,name,path):
    appslist=[]

    for term in terms:
        for tempapp in search_apps(term):
            app_details = app(tempapp['appId'])
            appslist.append(app_details)
    sizex=len(appslist)
    #print("Total Searched app collected are: ",sizex)
    
    #filtering the suspicious app based on email
    filtered_list = filter_currency_developer(appslist)
    
    #exporting the suspicious app in csv file
    csv_export(filtered_list,name,path)

banner() #printing the banner
NumArg=len(sys.argv)

#in case when user give "all", scan all the folder apps
if(NumArg==2 and sys.argv[1]=="all" ):
    print("scanning all the folders")
    files = os.listdir(default_path)
    print(files)
    for x in range(0,len(files)):
        print(x)
        path=default_path+files[x]
        temp_files = os.listdir(path)
        filename=[]
        for i in temp_files:
            if(i[-4:]=='.txt'):
                filename.append(i)
        print(filename)
        for txtfile in filename:
            keywords_file = open(path+"\\"+txtfile, "r", encoding='utf-8', errors='ignore')
            terms = keywords_file.read().splitlines()
            print(terms)
            appdetails(terms,files[x],path)
            keywords_file.close()



#this will scan specific given commands only
else:
    for i in range(0,NumArg-1):
        path=default_path+sys.argv[i+1]
        temp_files = os.listdir(path)
        #print(temp_files)
        filename=[]
        for x in temp_files:
            if(x[-4:]=='.txt'):
                filename.append(x)
        #print(filename)
        for txtfile in filename:
            keywords_file = open(path+"\\"+txtfile, "r", encoding='utf-8', errors='ignore')
            terms = keywords_file.read().splitlines()
            #print(terms)
            appdetails(terms,sys.argv[i+1],path)
            keywords_file.close()




