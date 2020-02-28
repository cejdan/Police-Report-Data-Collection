import argparse
from project0 import project0 as myProject


def main(url):

    myPDF = myProject.fetchincidents(url)
    myCSV = myProject.extractincidents(myPDF)

    #Write the csv to a .csv file.
    f = open("incidents.csv", "w")
    f.write(myCSV)
    f.close()
    #Now I am ready to use this file as the parameter for populatedb

    myProject.createdb()
    myProject.populatedb("normanpd.db", "incidents.csv")
    myProject.status("normanpd.db")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    #Must provide the following URL
    #http://normanpd.normanok.gov/content/daily-activity
	#Or, a URL of the form: http://normanpd.normanok.gov/filebrowser_download/657/\d\d\d\d-\d\d-\d\d%20Daily%20Incident%20Summary.pdf
    
    parser.add_argument("--incidents", type=str, required=True, 
                         help="The arrest summary url.")
     
    args = parser.parse_args()
    if args:
        main(args.incidents)
