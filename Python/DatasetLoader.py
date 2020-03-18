import pandas as pd
import DbFunctions as db

data = pd.read_csv("C:\\Users\\cressm\\Desktop\\TCSS 554\\380000-lyrics-from-metrolyrics\\lyrics.csv") 

connection = db.GetCloudConnection()


for index, row in data.iterrows():
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO MetroLyrics (Title,Artist,Year,Genre,Lyrics) VALUES (%s,%s,%s,%s,%s) "
            cursor.execute(sql, (str(row[1]),str(row[3]),str(row[2]),str(row[4]),str(row[5])))
            connection.commit()
        cursor.close();

    except: 
        print(str(index)+ " Failed")