import json
import sqlite3


class DB:

    def __init__(self):
        self.conn = sqlite3.connect('./landings.sqlite')
        self.cur = self.conn.cursor()

    def get_offer(self, params: list):
        if len(params) > 1:
            params[1] += '%'
        params = tuple(params)
        params_name = ['partner', 'name', 'country', 'keitaro']
        query = 'SELECT * FROM offers WHERE '
        for idx, param in enumerate(params):
            if idx > 0:
                prefix = 'AND '
            else:
                prefix = ''
            query += f'{prefix}{params_name[idx]} LIKE ? '
        with self.conn:
            try:
                ex = self.cur.execute(
                    query,
                    params
                )
                return ex.fetchall()
            except sqlite3.DatabaseError as error:
                print('Find some error: ' + error.__str__())

    def add_offer(self, offer_name: str, partner: str, data: json, country: str, keitaro: str):
        with self.conn:
            try:
                ex = self.cur.execute(
                    "INSERT INTO offers (partner, name, country, keitaro, data) VALUES (?, ?, ?, ?, ?)",
                    (partner, offer_name, country, keitaro, data)
                )
                return True if ex.rowcount > 0 else False
            except sqlite3.Error as err:
                return err

    def del_stream(self, stream_id: int):
        with self.conn:
            try:
                ex = self.cur.execute(
                    "DELETE FROM offers WHERE id = ?", (stream_id, )
                )
                if ex.rowcount > 0:
                    return True
                else:
                    return False
            except sqlite3.Error as error:
                raise error
