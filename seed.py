import csv
import model



#inserts data into database using model.Class method
def load_asanas(session):
    with open('initial_db_reformat.csv','rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                print row[4]
                asana = model.Asana(name=row[0], routine=row[4])
                session.add(asana)
    session.commit()        






def main(session):
    load_asanas(session)


if __name__=="__main__":
    s = model.connect()
    main(s)
