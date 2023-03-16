import sqlite3 as sq
import pandas as pd
import numpy as np
import matplotlib as plt

class Connection():
    def __init__(self):
        self.conn = sq.connect('Expense_Tracker.db')
        cursor = self.conn.cursor()
        # create a table
        cursor.execute("""CREATE TABLE if not exists data_table(
                [date] NUMERIC, [category] TEXT, [price] REAL, [description] TEXT) """)

        self.conn.commit()

    def insert_data(self, date, category, price, description):
        cursor = self.conn.cursor()
        bd = '''INSERT INTO data_table( DATE, CATEGORY , PRICE, DESCRIPTION)
        VALUES('{}', '{}', '{}', '{}')'''.format(date, category, price, description)
        cursor.execute(bd)
        self.conn.commit()
        cursor.close()

    def show_data(self):
        cursor = self.conn.cursor()
        bd = "SELECT * FROM data_table "
        cursor.execute(bd)
        records = cursor.fetchall()
        return records

    def find_data(self, date):
        cursor = self.conn.cursor()
        bd = '''SELECT * FROM data_table WHERE DATE={}'''.format(add_date)
        cursor.execute(bd)
        numberX = cursor.fetchall()
        cursor.close()

        return numberX

    def actualize_data(self, id, date, category, price, description):
        cursor = self.conn.cursor()
        bd = '''UPDATE data_table SET DATE = '{}', CATEGORY = '{}', PRICE = '{}', DESCRIPTION = '{}'
        WHERE ID = '{}' '''.format(date, category, price, description, id)
        cursor.execute(bd)
        a = cursor.rowcount
        self.conn.commit()
        cursor.close()

        return a



class Analitycs():
    def __init__(self):
        self.con = sq.connect('Expense_Tracker.db')
        self.df_expense = pd.read_sql_query('SELECT * FROM data_table', self.con)

    def sum_all(self):
        sum = self.df_expense['price'].cumsum()
        res = sum.iat[-1]
        return res

    def sum_category(self, ctg):
        category = [ctg]
        res = self.df_expense[self.df_expense.isin(category)]
        return res

    def sum_category_date(self, ctg, date1, date2):
        category = str(ctg)
        data = self.df_expense
        data['date'] = pd.to_datetime(data['date'])
        data['date'] = data['date'].dt.date
        data[((data['date'] >= date1) & (data['date'] <= date2))]
        new = data['category'].isin([category])

        return data[new]

    def all_category_but_time(self, date1, date2):
        data = self.df_expense
        data['date'] = pd.to_datetime(data['date'])
        data['date'] = data['date'].dt.date
        data[((data['date'] >= date1) & (data['date'] <= date2))]
        res = data.groupby(['category'])['price'].sum()

        #ctg = data['category'].unique()
        return res

    #def only_full_ctg(self, data1, data2):
     #   data= self.df_expense
      #  data['date'] = pd.to_datetime(data['date'])
       # data['date'] = data['date'].dt.date
        #data[((data['date'] >= date1) & (data['date'] <= date2))]










