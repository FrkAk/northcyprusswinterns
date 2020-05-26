import sqlite3


class Database():

    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.name= "Database"

    @staticmethod
    def getinternshippositions():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        internshipdetail = c.execute("SELECT SOFTWARECOMPANY.companyname, INTERNSHIPPOSITION.* ,SOFTWARECOMPANY.citycode "
                                     "FROM INTERNSHIPPOSITION "
                                     "INNER JOIN SOFTWARECOMPANY ON SOFTWARECOMPANY.username = INTERNSHIPPOSITION.companyusername "
                                     "ORDER BY  deadline DESC")

        internships = internshipdetail.fetchall()

        conn.commit()
        conn.close()
        liste = []
        if internships == []:
            return liste
        else:
            for i in  internships:
                liste.append(i)
            return liste




    @staticmethod
    def getinternshippositionsforacompany(user):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        internshipdetail = c.execute(
            "SELECT internshipname,details,expectations,deadline FROM INTERNSHIPPOSITION "
            "WHERE companyusername = ? ORDER BY  deadline DESC",(user,))

        internships = internshipdetail.fetchall()

        conn.commit()
        conn.close()
        liste = []
        if internships == []:
            return liste
        else:
            for i in internships:
                liste.append(i)
            return liste

    @staticmethod
    def countRow(tablename):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        allpositions = c.execute("SELECT * FROM %s" % tablename )

        records = allpositions.fetchall()
        count = len(records)

        conn.commit()
        conn.close()

        return count    
    @staticmethod 
    def authenticationForCompany(account):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        #accoun is not none
        keyUsername = account[0]
        keyPassword = account[1]

        ACCOUNT = c.execute("SELECT username,pwd FROM SOFTWARECOMPANY WHERE username = ? AND pwd = ?",
                             (keyUsername, keyPassword,))
        ID = ACCOUNT.fetchall()

        conn.commit()
        conn.close()

        if ID == []:
            return None
        else:
            return ID[0][0]

    @staticmethod
    def registerationForCompany(registrationDetails):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        for i in registrationDetails:
            if i is None:
                return False # if return value is null value registeration will not be accepted

        keyUsername = registrationDetails[0]

        isUserExist = c.execute("SELECT username FROM SOFTWARECOMPANY "
                                "WHERE username = ?",(keyUsername,))

        user = isUserExist.fetchone()


        if user != None:
            return False
        citycode = c.execute("SELECT citycode FROM CITY WHERE cityname = ?",(registrationDetails[6],))
        city = citycode.fetchone()
        registrationDetails[6] = city[0]
        c.execute(
            "INSERT INTO SOFTWARECOMPANY(username, pwd, companyname, email, telephone,website, citycode, address, sessionid)VALUES(?,?,?,?,?,?,?,?,?)",
            registrationDetails)

        conn.commit()
        conn.close()
        return True

    @staticmethod
    def internshipAdd(intershipDetails):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        for i in intershipDetails:
            if i is None:
                return "NullValue"


        id = c.execute("SELECT MAX(ID) FROM INTERNSHIPPOSITION")

        biggestID = id.fetchone()
        biggest = biggestID[0]
        if biggestID[0] == None:
            biggest = 1
        else:
            biggest = biggest+1
        liste = []
        liste.append(biggest)
        liste.extend(intershipDetails)

        c.execute(
            "INSERT INTO INTERNSHIPPOSITION(id, internshipname, details, expectations,deadline,companyusername)VALUES(?,?,?,?,?,?)",liste)

        conn.commit()
        conn.close()

        return "Succesful"
    

    @staticmethod
    def companyDetails(companyName):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        # CİTY is missing from infos
        companyExist =c.execute("SELECT companyname,email,telephone,website,address,cityname FROM SOFTWARECOMPANY "
                                "INNER JOIN CITY ON SOFTWARECOMPANY.citycode = CITY.citycode "
                                "WHERE companyname = ? ",(companyName,))

        companyInfo = companyExist.fetchmany()
        liste = []
        for i in companyInfo[0]:
            liste.append(i)

        if companyInfo == []:
            return "Company existing error"
        else:
            return liste # add city

        conn.commit()
        conn.close()




    @staticmethod
    def searchKeyWord(keyword):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()


        internshipID =  c.execute("SELECT DISTINCT id FROM INTERNSHIPPOSITION "
                                  "WHERE expectations LIKE ?",(keyword,))

        IDs = internshipID.fetchall()

        if IDs == []:
            return False

        return IDs


        conn.commit()
        conn.close()
    @staticmethod
    def checkDatabesExistance():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        flag = False

        # get the count of tables with the name
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CITY' ''')

        # if the count is 1, then table exists
        if c.fetchone()[0] == 1:
            print('Table exists.')
            flag = True

        # commit the changes to db
        conn.commit()
        # close the connection
        conn.close()
        return flag
   
    @staticmethod
    def databaseInitiation():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""CREATE TABLE CITY (
                    citycode INTEGER PRIMARY KEY,
                    cityname TEXT NOT NULL)""")

        c.execute("""CREATE TABLE SOFTWARECOMPANY(
                    username TEXT NOT NULL PRIMARY KEY,
                    pwd TEXT NOT NULL,
                    website TEXT NOT NULL,
                    companyname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telephone INTEGER,
                    address TEXT NOT NULL,
                    sessionid INTEGER,
                    citycode INTEGER,
                    FOREIGN KEY (citycode) REFERENCES CITY (citycode))
                    """)

        c.execute("""CREATE TABLE INTERNSHIPPOSITION(
                     id INTEGER PRIMARY KEY,
                     internshipname TEXT NOT NULL,
                     details TEXT NOT NULL,
                     expectations TEXT NOT NULL,
                     deadline TEXT NOT NULL,
                     companyusername TEXT NOT NULL,
                     FOREIGN KEY (companyusername) REFERENCES SOFTWARECOMPANY (username))""")

        cities = [(1, 'Gazimagusa'),
                  (2, 'Girne'),
                  (3, 'Guzelyurt'),
                  (4, 'Iskele'),
                  (5, 'Lefke'),
                  (6, 'Lefkosa')]

        companies = [('apple','apple123','apple.com','Apple','apple@apple.com','0123456','apple blv. 123 st.','123',1)]

        intership = [(8,'kole','freekole', 'everythingbutlittlelittle','2020-05-04','apple'),(7,'efde','freaewfsekole', 'asdf','2021-04-08','apple')]

        c.executemany("INSERT INTO CITY(citycode, cityname)VALUES(?, ?)", cities)
        c.executemany("INSERT INTO SOFTWARECOMPANY(username, pwd, website, companyname, email, telephone, address, sessionid, citycode)VALUES(?,?,?,?,?,?,?,?,?)",companies)
        c.executemany("INSERT INTO INTERNSHIPPOSITION(id,internshipname, details, expectations, deadline, companyusername)VALUES(?,?,?,?,?,?)", intership)

        conn.commit()
        conn.close()


listeintern = ["googleintern","Summer Intern","Fulltime Internship","2020-04-05","google"]
listecomany = ["asdf","asf","website","cname","email","tel","add","sıd"]
account = ["username","password"]
companyname = "Apple"
db = Database()
#returnval = db.internshipAdd(listeintern)
#returnval = db.registerationForCompany(listecomany)
#returnval = db.authenticationForCompany(account)
#returnval = db.companyDetails(companyname)
#returnval = db.countRow("SOFTWARECOMPANY")
#returnval = db.getinternshippositions()
#returnval = db.searchKeyWord("as")
#print(returnval)
#db.databaseInitiation()
