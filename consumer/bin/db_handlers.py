from os import environ
from threading import Thread

import sqlalchemy as db
from sqlalchemy import literal_column
from sqlalchemy import Table, Column, Integer, String, MetaData, JSON

environ = dict(DB_USER="postgres", DB_PASS="postgres", DB_HOST="localhost", DB_PORT="5432", DB_NAME="postgres",
               KAFKA_TOPIC="ConsumerTopic")

connection_str = f'postgresql://{environ["DB_USER"]}:{environ["DB_PASS"]}@' \
                 f'{environ["DB_HOST"]}:{environ["DB_PORT"]}/' \
                 f'{environ["DB_NAME"]}'

class Database:

    def __init__(self):
        self.engine = db.create_engine(connection_str)
        meta = MetaData(db, schema="consumer")
        self.iterations_table = Table('iterations', meta,
                                      Column('i_id', Integer),
                                      Column('s_id', Integer),
                                      Column('i_json', JSON))
        self.scenario_table = Table('scenarios', meta,
                                    Column('s_id', Integer),
                                    Column('s_name', String),
                                    Column('s_topic_id', String),
                                    Column('s_serial', Integer),
                                    Column('s_graph', JSON))
        self.result_table = Table('result', meta,
                                  Column('r_id', Integer),
                                  Column('i_id', Integer),
                                  Column('r_service_name', String),
                                  Column('r_json', JSON))
        self.connection = self.engine.connect()
        print("DB Instance created")

    def select_id_scenario_by_topic(self, topic):
        select_statement = self.scenario_table.select().where(self.scenario_table.c.s_topic_id == topic)
        result = self.connection.execute(select_statement).fetchall()[0]
        return result[0]

    def insert_iterations(self, data):
        try:
            scenario_id = self.select_id_scenario_by_topic(environ["KAFKA_TOPIC"])
            insert_statement = self.iterations_table.insert().values(s_id=scenario_id, i_json=data).returning(
                literal_column('i_id'))
            result = self.connection.execute(insert_statement).fetchall()[0][0]
        except Exception:
            result = self.select_id_iteration_by_json(data)
        return result

    def select_id_iteration_by_json(self, data):
        select_statement = self.iterations_table.select().where(self.iterations_table.c.i_json == data)
        result = self.connection.execute(select_statement).fetchall()[0]
        return result[0]

    def insert_result(self, name, data, iter_id):
        insert_statement = self.result_table.insert().values(r_service_name=name, r_json=data,
                                                             i_id=iter_id).returning(
            literal_column('r_id'))
        result = self.connection.execute(insert_statement).fetchall()[0][0]
        return result


class DB_Saver(Thread):

    def __init__(self, message, database):
        Thread.__init__(self)
        # self.engine = _ENGINE if _ENGINE else connect()
        self.message = message
        self.database = database

    def run(self):
        try:
            i_id = self.database.insert_iterations(self.message["input"])
            print(self.database.insert_result(name=self.message["id"], data=self.message["data"], iter_id=i_id))
        except Exception as err:
            print(err)
