
import urllib.request
import PyPDF2
import tempfile
import re
import sqlite3
from sqlite3 import Error
import pandas
import os


class project0:
    def fetchincidents(url):
        #NOTE, you MUST supply the following url: "http://normanpd.normanok.gov/content/daily-activity"
        #Or a url of the form: "http://normanpd.normanok.gov/filebrowser_download/657/\d\d\d\d-\d\d-\d\d%20Daily%20Incident%20Summary.pdf"
        
        allData = []
        inputPattern = re.compile(r"http://normanpd.normanok.gov/filebrowser_download/657/\d\d\d\d-\d\d-\d\d%20Daily%20Incident%20Summary.pdf")

        if(re.search(inputPattern, url)):
            allData.append(urllib.request.urlopen(url).read())
            return allData

        elif(url == "http://normanpd.normanok.gov/content/daily-activity"):
            #This opens a connection to the normanpd website.
            police = urllib.request.urlopen(url)
            policeStr = police.read()
            #.read actually closes the connection to the website, but you get the data saved in a variable.
            #This line converts the entire HTML page into one huge string.
            policeStr = policeStr.decode("UTF-8")

            #Now I want generate a list of all the Incident Summary.pdfs

            incidentNames = re.findall(r"\d\d\d\d-\d\d-\d\d%20Daily%20Incident%20Summary.pdf", policeStr)

            #print(incidentNames)
            #Cool. That works. Now, for each item in that list, append the correct http:// ... string

            extraString = "http://normanpd.normanok.gov/filebrowser_download/657/"
            fullIncidentNames = []

            for x in range(len(incidentNames)):
                fullIncidentNames.append(extraString + incidentNames[x])

            #print(fullIncidentNames)
            #Sweet action. It prints the url of each Incident Summary pdf, so we can access just the latest day's incident report with:
            #fullIncidentNames[0]

            allData = []

            allData.append(urllib.request.urlopen(fullIncidentNames[0]).read())

            #Run this block if you want to download ALL 7 Incident PDFs on that page.
            #Slower, but allows you to access WAY more data.
            # =============================================================================
            # #Now, let's loop through, and open a connection to each unique pdf on that list, saving the contents into a variable.
            # for x in range(len(fullIncidentNames)):
            #     allData.append(urllib.request.urlopen(fullIncidentNames[x]).read())
            # #I now have all 7 pdfs downloaded. They are of type binary.
            # =============================================================================
            return allData
        else:
            raise NameError("The url was invalid. Please input the following url: http://normanpd.normanok.gov/content/daily-activity")

    def extractincidents(dataPDF):
        
        fp = tempfile.TemporaryFile()
        fp.write(dataPDF[0])
        reader = PyPDF2.PdfFileReader(fp)
        allPages = ""
        pageNums = reader.getNumPages()
        full_pattern = re.compile(r"(.+)\n(\d{4}-\d{8})\n(.+)(\n)?(.+)?\n([A-Z][a-z]|[A-Z]{3} |[9][1][1] )(.+)\n(.+)\n")
        #  Ok, the above regex is a little complex. I will try to explain.
        #  First, it finds the Date / Time with .+\n
        #  Then, it finds any Incident Number (ex. 2020-00001484) with \d{4}-\d{8}\n
        #  Then, it finds the Location. Location has a problem, which is sometimes things are split into 2 lines
        #  So, we look for .+ then an optional \n and an optional .+  then we find the non-optional \n
        #  Next, we need to find the Nature, which always has the pattern CAPITALlower... or 3x CAP then a space
        #  or 911 then a space. This is this piece:([A-Z][a-z]|[A-Z]{3} |[9][1][1] )
        #  Then we find the remaining word with .+\n  
        #  Finally, we find the Incident ORI with another .+\n
        #  This specific pattern will find the items in the correct order.
        #  The 8 () groups allow us to do a subsitution to create our desired csv format
 

     #Now we start a loop, doing once for each page
        for page in range(0,pageNums):
            myPage = reader.getPage(page)
            pageStr = myPage.extractText()
         
            if(page == 0): #Cleans up page 0
                extraCommas = re.compile(r",")
                subbed_page = extraCommas.sub(r";", pageStr)
                column_headers = re.compile(r"(Date) / (Time)\n(Incident) (Number)\n(Location)\n(Nature)\n(Incident) (ORI)\n")
                subbed_page = column_headers.sub(r"\1/\2,\3_\4,\5,\6,\7_\8\n", subbed_page)
                extraText1 = re.compile(r"NORMAN POLICE DEPARTMENT\n")
                extraText2 = re.compile(r"Daily Incident Summary \(Public\)")
                subbed_page = extraText1.sub(r"", subbed_page)
                subbed_page = extraText2.sub(r"", subbed_page)
                subbed_page = full_pattern.sub(r"\1,\2,\3\5,\6\7,\8\n", subbed_page)
                allPages = allPages + subbed_page
            else:
                extraCommas = re.compile(r",")
                subbed_page = extraCommas.sub(r";", pageStr)
                subbed_page = full_pattern.sub(r"\1,\2,\3\5,\6\7,\8\n", subbed_page)
                allPages = allPages + subbed_page 
        
    #Now do the final clean-up:
        emptyLine = re.compile(r"\n\n")
        finalLine = re.compile(r".+$")
        allPages = emptyLine.sub(r"\n", allPages)
        allPages = finalLine.sub(r"", allPages)
 
    #Ok, there can still be an issue. Some Incident pdfs have BLANKS for Nature. Need to address it now.
        blankNature = re.compile(r"(.+)\n(\d{4}-\d{8})\n(.+)(\n)?(.+)?\n(OK|EM|[\d][\d])(.+)\n")
        allPages = blankNature.sub(r"\1,\2,\3\5,NA,\6\7\n", allPages)
        
        return allPages

    def createdb():
        #Code modified from https://www.sqlitetutorial.net/sqlite-python/creating-database/
        conn = None
          
        try:
            conn = sqlite3.connect("normanpd.db")
            #print("Connection opened. Sqlite3 version:",sqlite3.version)
            
            try:
                c = conn.cursor()
                c.execute("""CREATE TABLE incidents('Date/Time' TEXT, 
                                                'Incident_Number' TEXT, 
                                                'Location' TEXT, 
                                                'Nature' TEXT, 
                                                'Incident_ORI' TEXT)""")
            except:
                pass
        except Error:
            print(Error)
        finally:
            if conn:
                #print("Connection closed")
                conn.commit()
                conn.close()

    def populatedb(db, incidents):
        try: 
            conn = sqlite3.connect(db)
        except Error:
            print("Error")
        finally:
            if conn:
                df = pandas.read_csv(incidents)
                df.to_sql("incidents", conn, if_exists='replace', index=False)
                conn.commit()
                conn.close()

    def status(db):
        try:
            conn = sqlite3.connect(db)
        except Error:
            print("Error")
        finally:
            if conn:
                c = conn.cursor()
				#Here we select all the Distinct Nature, and add a count column. We group by Nature, and order by ascending.
                c.execute("SELECT DISTINCT Nature, COUNT(Nature) FROM incidents GROUP BY Nature ORDER BY Nature ASC;")
                rows = c.fetchall()     
				
				#We can output the desired format like so:
                for row in rows:
                    print(row[0],row[1],sep="|")
                    
                return rows


# #=============================================================================
# #This is the main method basically. I moved it to main.py
#myProject = project0()
#myPDF = myProject.fetchincidents("http://normanpd.normanok.gov/content/daily-activity")
#myCSV = myProject.extractincidents(myPDF)
# 
# #Write the csv to a .csv file.
#f = open("incidents.csv", "w")
#f.write(myCSV)
#f.close()
# #Now I am ready to use this file as the parameter for populatedb
# 
#myProject.createdb()
#myProject.populatedb("normanpd.db", "incidents.csv")
#myProject.status("normanpd.db")
# #=============================================================================


