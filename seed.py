import csv
import model



#inserts data into database using model.Class method
def load_asanas(session):
    with open('asana_db.csv','rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                asana = model.Asana(name=row[0], breaths=row[5])
                session.add(asana)
    session.commit()        

def load_flows(session):
    with open('flow_db.csv','rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                flow = model.Flow(asana_id=row[0], flow_id=row[1], order=row[2], breaths=row[3])
                session.add(flow)
    session.commit()  




def main(session):
    load_asanas(session)
    load_flows(session)


if __name__=="__main__":
    s = model.connect()
    main(s)
