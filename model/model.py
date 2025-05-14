from UI.controller import Controller
from database.DAO import DAO


class Model:
    def __init__(self):
        self.DAO = DAO()
        pass

    def passaColoriMO(self):
        listaColoriMO = self.DAO.getColors()
        return listaColoriMO

    def cercaNodiMO(self, color):
        listaNodi = self.DAO.getProductsOfColor(color)
        return listaNodi



