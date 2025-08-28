import os

import pyodbc
from dotenv import load_dotenv

load_dotenv()


class DBConnectionHandler:
    """
    Gerenciador de conexão SQL Server
    """

    def __init__(self):
        self.server = os.getenv("SERVER")
        self.database = os.getenv("DATABASE")
        self.driver = os.getenv("DRIVER")
        self.trusted_connection = os.getenv("TRUSTED_CONNECTION")
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        try:
            if self.trusted_connection.lower() == "yes":
                conn_str = (
                    f"DRIVER={self.driver};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"TRUSTED_CONNECTION={self.trusted_connection};"
                )
            else:
                conn_str = (
                    f"DRIVER={self.driver};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={os.getenv('UID')};"
                    f"PWD={os.getenv('PWD')};"
                )
            self.connection = pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            raise ConnectionError(f"Erro ao conectar ao SQL Server: {e}") from e

    def get_cursor(self):
        if self.connection:
            return self.connection.cursor()
        raise RuntimeError(
            "Conexão não iniciada. Verifique chamada do método connect()."
        )

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
