# Police-Incident-Reports
This project is designed to connect to the Norman Police Departments's website at http://normanpd.normanok.gov/content/daily-activity , and download the latest Daily Incident Summary PDF.
The incident summary is a public document that contains information on the daily Norman PD's activity. It contains information on what the nature of the stop was for, and where the stop occured.
Here is an example of what is contained inside one Incident PDF:

Date/Time | Incident Number | Location | Nature | Incident ORI
--------- | --------------- | -------- | ------ | ------------
2/24/2020 0:04 | 2020-00003064 | 1932 E LINDSEY ST | Breathing Problems | EMSTAT
2/24/2020 0:08 | 2020-00014232 | 2146 W BROOKS ST | Open Door/Premises Check | OK0140200
2/24/2020 0:17 | 2020-00014233 | OAKWOOD DR / WYLIE RD | Traffic Stop | OK0140200

To download and run this project, first download or clone the repository, and on a Bash shell with python3 and pipenv installed, run:
    pipenv install

Once the pipenv has been initialized and all required packages have been successfully installed, you can run the scripts with:
    pipenv run python project0/main.py --incidents http://normanpd.normanok.gov/content/daily-activity
	
By default, the script will run on the most recent Incident Report. If you prefer to run on a specific Incident report, please replace the URL with your specifc PDF's URL, for example:
    pipenv run python project0/main.py --incidents http://normanpd.normanok.gov/filebrowser_download/657/2020-02-24%20Daily%20Incident%20Summary.pdf
	

# Explanation of the code
The project is broken up into 5 main functions, contained within the project0.py file.
## fetchincidents(url)
This function returns a bytes object, which is generated by using the urllib library. We use the function:
```python3
urllib.request.urlopen(url).read()
```
Which opens a connection to the provided url, and reads the data into a bytes object. The trick with this function is that if you provide the http://normanpd.normanok.gov/content/daily-activity URL, the function converts the HTML of the webpage to a string, then using regex it finds substrings with the form:
http://normanpd.normanok.gov/filebrowser_download/657/2020-02-24%20Daily%20Incident%20Summary.pdf . It then appends each of the incident PDFs into a list, and then runs urllib.request.urlopen(url).read() on the most recent one.
This function has the capability of adding all 7 Incident PDFs from the website into a list, and reading all of them. This feature is commented out, but can be easily activated.

## extractincidents(dataPDF)
This function reads the bytes object generated by fetchincidents() turns the PDF into a string in csv format. It achieves this using the PyPDF2 package, to read the bytes object, then using a series of regex statments to identify patterns in the data to split them into comma seperated columns.

Please see the comments in the code itself for details on the regex statements.

We must take special care on Page0 of the PDF, as the first line contains the column headers, and the last two lines contain extra unnecessary information that we need to remove.

We also must take special care to handle cases where no data was entered, as well as cases where the address is split into two lines.
We handle all of this with regex statements.

## createdb()
This function creates a new sqlite3 database with the following SQLite3 statement:
```sqlite3
    CREATE TABLE incidents('Date/Time' TEXT, 'Incident_Number' TEXT, 'Location' TEXT, 'Nature' TEXT, 'Incident_ORI' TEXT);
```
We take care in this function to skip the table creation if the table already exists, so that way we avoid problems if the function is run multiple times in a row.

## populatedb(db, incidents)
This function will now populate our newly-created SQLite3 table with the csv generated from extractincidents().
To achieve this, pandas can easily handle reading csv files, and writing to SQLite databases, so we take advantage of that powerful feature using the code:
```python3
    df = pandas.read_csv(incidents)
    df.to_sql("incidents", conn, if_exists='replace', index=False)
```
If a populated table already exists, the if_exists='replace' flag will ensure it gets overwritten and not appended.

## status(db)
The "Analytics" part of our code. We finally have the data in the form we want, so we can do a simple analysis of the number of distinct events, and their frequencies. We achieve this with a SQLite statement:
    SELECT DISTINCT Nature, COUNT(Nature) FROM incidents GROUP BY Nature ORDER BY Nature ASC;
We can then trap the resulting rows, and print them out in the desired pipe-seperated format using:
```python3
    rows = c.fetchall()
    for row in rows:
		print(row[0],row[1],sep="|")
```
# Questions or Comments
If you have any questions or comments about this project, please contact me at: ncejda@gmail.com
