from usuario.config.mysqlconnection import connectToMySQL

class Country:
    name_db = "app_dojo"

    def __init__(self, id, nombre, created_at):
        self.id = id
        self.nombre = nombre
        self.created_at = created_at

    @classmethod
    def getCountry(self):
        query = "SELECT * FROM pais"
        resultado = connectToMySQL("app_dojo").query_db(query)
        return resultado