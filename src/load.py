from database import Region, engine, User
from transformation import flatten_json_data, normalize_user_data, normalize_region_data
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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
    users_data = []
    regions_data = []
    for line in file:
        json_data = json.loads(line)
        user_data, region_data = flatten_json_data(json_data)
        user_data = normalize_user_data(user_data)
        region_data = normalize_region_data(region_data)
        users_data.append(user_data)
        regions_data.append(region_data)
    
    return users_data, regions_data
    


def read_csv_lines(file):
    for line in file:
        user_data = ...
        user_data = normalize_user_data(user_data)
        
        pass
        yield user_data, {'city': None, 'state': None}


@click.command()
@click.argument('input_file', type=click.File('rt'))
def process(input_file):
    print(input_file)
    
    ext = input_file.name.split('.')[-1]
    if ext == 'json':
        users_data, regions_data = read_json_lines(input_file)
    elif ext =='csv':
        records = ...
    else:
        raise RuntimeError('something here')
    
    with Session(engine) as session:
        for i, (user_data, region_data) in enumerate(zip(users_data, regions_data), start=1):
            region = upsert_region(session, region_data)
            upsert_user(session, user_data, region)
            if i % 100 == 0:
                session.commit()
        session.commit()
    
    
        
    # classify, is it csv or json or raise error
    # if csv, call one parser, if json - another
    # they both return lists or iterators of data items
    # for each item, normalize, validate
    # create new User
    # add (upsert) to db
    # commit every 100 users
    pass

def upsert_region(session, region_data):
    region = session.query(Region).filter_by(**region_data).first()
    if not region:
        region = Region(**region_data)
        session.add(region)
        try:
            session.flush()
        except SQLAlchemyError:
            session.rollback()
    return region

def upsert_user(session, user_data, region):
    try:
        user = session.query(User).filter_by(email=user_data['email']).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.region = region
        else:
            user = User(**user_data, region=region)
            session.add(user)
        session.flush()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"SQLAlchemyError occurred: {e}")

if __name__ == "__main__":
    process()
