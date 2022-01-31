from usuario.config.mysqlconnection import connectToMySQL

class CivilStatus:
    name_db = "app_dojo"

    def __init__(self, id, nombre, created_at):
        self.id = id
        self.nombre = nombre
        self.created_at = created_at

    @classmethod
    def getCivilStatus(self):
        query = "SELECT * FROM estado_civil"
        resultado = connectToMySQL("app_dojo").query_db(query)
        return resultado
