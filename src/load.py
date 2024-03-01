from database import Region, engine
from transformation import flatten_json_data
from sqlalchemy.orm import Session

import click
import json


def find_or_create_region(session, city, state):
    region = session.query(Region).filter_by(city=city, state=state).first()
    if not region:
        region = Region(city=city, state=state)
        session.add(region)
        session.commit()
    return region

def read_json_lines(file):
    for line in file:
        json_data = json.loads(line)
        user = flatten_json_data(json_data)
        yield user
        
        
def read_csv_lines(file):
    for line in file:
        pass

@click.command()
@click.argument('input_file', type=click.File('rt'))
def process(input_file):
    print(input_file)
    
    ext = input_file.name.split('.')[-1]
    if ext == 'json':
        records = read_json_lines(input_file)
    elif ext =='csv':
        pass
    else:
        raise RuntimeError('something here')
    
    with Session(engine) as session:
        for rec in records:
            session.add(rec)
            print(rec)
            session.commit()
    
        
    # classify, is it csv or json or raise error
    # if csv, call one parser, if json - another
    # they both return lists or iterators of data items
    # for each item, normalize, validate
    # create new User
    # add (upsert) to db
    # commit every 100 users
    pass


if __name__ == "__main__":
    process()
