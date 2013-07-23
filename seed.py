import csv
import model



#inserts data into database using model.Class method
def load_asanas(session):
    with open('initial_database.csv','rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                print row[2]
                asana = model.Asana(name=row[0], position=row[1], movement=row[2], time=row[3])
                session.add(asana)
    session.commit()        

# Asana Name    Position    Movement    Time




def main(session):
    load_asanas(session)


if __name__=="__main__":
    s = model.connect()
    main(s)
