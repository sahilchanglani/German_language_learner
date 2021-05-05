import pandas
import MySQLdb


data = pandas.read_csv("data/german_words.csv")
dict_data = data.to_dict(orient="records")

connection = MySQLdb.connect(host="localhost", user="root", password="", database="german_words")
cursor = connection.cursor()
count = 0
for card in dict_data:
    try:
        count += 1
        str = "INSERT INTO words VALUES('%s','%s', '%s')"
        args = (count, card["German"], card["English"])
        cursor.execute(str % args)
        connection.commit()
    except:
        print(f"There's error on row {count}")

connection.close()

