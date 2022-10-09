from sqlite3 import connect

class DbSqlite:
    def __init__(self, local:str=None):
        self.local = local
    
    def connect(self):
        self.conn = connect(self.local)
        return self.conn
    
    def disconnect(self):
        self.conn.close()
    
    def get_tables(self):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT * FROM sqlite_master WHERE type='table';""")
        list_to_return = [i[1] for i in cursor.fetchall()]
        self.disconnect()
        return list_to_return
    
    def get_table(self, tabela:str, columns:tuple='*'):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT {str(columns).replace("'", "")} FROM {tabela};""")
        list_to_return = cursor.fetchall()
        self.disconnect()
        return list_to_return
    
    #Retorna lista de colunas de uma tabela.
    def get_table_columns(self, table:str):
        cursor = self.connect().cursor()
        cursor.execute(f"""PRAGMA table_info({table});""")
        lista = cursor.fetchall()
        self.disconnect()
        return (i[1] for i in lista)
    
    #Retorna instância de uma tabela. (key -> [atributo, valor])
    def get_instance(self, table:str, key:list, columns:tuple='*'):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT {columns} FROM {table} WHERE {key[0]} = '{key[1]}'""")
        lista = cursor.fetchall()
        self.disconnect()
        return lista
    
    def new_table(self, table_name:str, table_columns:tuple):
        cursor = self.connect().cursor()
        cursor.execute(f"""
        CREATE TABLE {table_name} {str(table_columns).replace("'", "")};""")
        self.disconnect()
    
    #Cria nova instância de uma tabela. 
    def new_instance(self, table:str, tupla:tuple):
        conn = self.connect()
        cursor = conn.cursor()
        mapa = self.get_table_columns(table)
        cursor.execute(f"""
        INSERT INTO {table} {tuple(i.replace("'", "") for i in mapa)} VALUES {tuple(tupla)}
        """)
        conn.commit()
        self.disconnect()
    
    #Edita instância de uma tabela. (key -> [atributo, valor])
    def edit_instance(self, table:str, key:list, attribute:str, value):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE {table} SET {attribute} = '{value}' WHERE {key[0]} = '{key[1]}'""", ())
        conn.commit()
    
    #Remove instância de uma tabela. (key -> [atributo, valor])
    def del_instance(self, table:str, key:list):
        conn = self.connect()
        cursor = conn.cursor()
        key =  f"WHERE {key[0]} = '{key[1]}'"
        cursor.execute(f"""DELETE FROM {table} {key}""",)
        conn.commit()

def main():
    pass
    
if __name__ == '__main__':
    main()
