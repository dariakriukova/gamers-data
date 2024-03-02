from datetime import datetime
from pathlib import Path
import pandas as pd
from database import upsert_region, upsert_user, engine
from transformation import flatten_json_data, normalize_user_data, normalize_region_data
from sqlalchemy.orm import Session
import click
import json
import itertools


def read_json_lines(file):
    users_data = []
    regions_data = []
    with file.open() as f:
        for line in f:
            json_data = json.loads(line)
            user_data, region_data = flatten_json_data(json_data)
            user_data = normalize_user_data(user_data)
            region_data = normalize_region_data(region_data)
            users_data.append(user_data)
            regions_data.append(region_data)

    return users_data, regions_data


def read_csv_lines(file):
    df = pd.read_csv(file, usecols=["first_name","last_name","email","gender","dob"])
    users_data = []
    for i, row in df.iterrows():
        user_data = normalize_user_data(row.to_dict())

        users_data.append(user_data)
    return users_data

def process_file(input_file):
    ext = input_file.name.split(".")[-1]
    if ext == "json":
        users_data, regions_data = read_json_lines(input_file)
    elif ext == "csv":
        users_data = read_csv_lines(input_file)
        regions_data = itertools.cycle([{'city': None, 'state': None}])
    else:
        print(f'Skipping file {input_file}')

    with Session(engine) as session:
        for i, (user_data, region_data) in enumerate(
            zip(users_data, regions_data), start=1
        ):
            region = upsert_region(session, region_data)
            upsert_user(session, user_data, region)
            if i % 100 == 0:
                session.commit()
        session.commit()


@click.command()
@click.argument("game", type=click.Choice(['WWC', 'HB'], case_sensitive=False))
@click.argument("date", type=click.DateTime(formats=["%Y-%m-%d"]))
def process(game: str, date: datetime):
    
    # look for file
    parent_dir = Path(f'./data/{game.lower()}/{date.strftime("%Y/%m/%d")}/')
    if not parent_dir.exists():
        raise RuntimeError('bla bla')
    
    for file in parent_dir.glob('*.*'):
        process_file(file)
    


if __name__ == "__main__":
    process()
