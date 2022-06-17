import random

import pandas as pd
from pandas import DataFrame, Series
from sqlalchemy import create_engine
from sqlalchemy.future import Engine


class SqliteManager:
    chat_table: DataFrame
    engine: Engine

    def __init__(self):
        self.chat_table = DataFrame()
        self.engine = create_engine('sqlite:///exchanges.sqlite')
        self.chat_table = pd.read_sql('chat_table', self.engine,
                                      columns=['name', 'description'])

    def delete_row(self, name) -> int:
        self.chat_table = self.chat_table[self.chat_table.name != name]
        return self.chat_table.to_sql('chat_table', self.engine, if_exists='replace')

    def is_name_in(self, name) -> bool:
        return name in self.chat_table['name'].values

    def insert_row(self, name: str, description: str):
        name = name
        description = description
        if (len(self.chat_table) != 0) and self.is_name_in(name):
            raise ValueError('Error! Chat name is not unique')
        row = DataFrame([{
            "name": name,
            "description": description,
        }])
        self.chat_table = pd.concat([self.chat_table, row])
        return self.chat_table.to_sql('chat_table', self.engine, if_exists='replace')


sqlite_manager = SqliteManager()
