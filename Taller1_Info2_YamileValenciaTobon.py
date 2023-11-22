# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 20:42:21 2023

@author: Yami
"""

class Maquina:
    def __init__(self, precio, stock, modelo, empresa):
        self._precio = precio
        self._stock = stock
        self._modelo = modelo
        self._empresa = empresa
    
    def __str__(self):
        return f"Modelo: {self._modelo}\nEmpresa: {self._empresa}\nPrecio: {self._precio}\nStock: {self._stock}"

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        self._precio = nuevo_precio

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock):
        self._stock = nuevo_stock

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, nuevo_modelo):
        self._modelo = nuevo_modelo

    @property
    def empresa(self):
        return self._empresa

    @empresa.setter
    def empresa(self, nueva_empresa):
        self._empresa = nueva_empresa

class Desfibrilador(Maquina):
    def __init__(self, precio, stock, modelo, empresa, energia_maxima):
        super().__init__(precio, stock, modelo, empresa)
        self._energia_maxima = energia_maxima
    
    def __str__(self):
        return super().__str__() + f"\nEnergía máxima: {self._energia_maxima}"

    @property
    def energia_maxima(self):
        return self._energia_maxima

    @energia_maxima.setter
    def energia_maxima(self, nueva_energia_maxima):
        self._energia_maxima = nueva_energia_maxima

class Electrocardiografo(Maquina):
    def __init__(self, precio, stock, modelo, empresa, num_derivaciones):
        super().__init__(precio, stock, modelo, empresa)
        self._num_derivaciones = num_derivaciones
    
    def __str__(self):
        return super().__str__() + f"\nNúmero de derivaciones: {self._num_derivaciones}"

    @property
    def num_derivaciones(self):
        return self._num_derivaciones

    @num_derivaciones.setter
    def num_derivaciones(self, nuevo_num_derivaciones):
        self._num_derivaciones = nuevo_num_derivaciones

class ResonanciaMagnetica(Maquina):
    def __init__(self, precio, stock, modelo, empresa, intensidad_campo_magnetico):
        super().__init__(precio, stock, modelo, empresa)
        self._intensidad_campo_magnetico = intensidad_campo_magnetico
    
    def __str__(self):
        return super().__str__() + f"\nIntensidad de campo magnético: {self._intensidad_campo_magnetico}"

    @property
    def intensidad_campo_magnetico(self):
        return self._intensidad_campo_magnetico

    @intensidad_campo_magnetico.setter
    def intensidad_campo_magnetico(self, nueva_intensidad_campo_magnetico):
        self._intensidad_campo_magnetico = nueva_intensidad_campo_magnetico

#Uso
desfibrilador = Desfibrilador(5000, 10, "DF-2000", "MedTech", 200)
print(desfibrilador)

electrocardiografo = Electrocardiografo(8000, 5, "ECG-500", "MedTech", 12)
print(electrocardiografo)

resonancia = ResonanciaMagnetica(150000, 2, "RM-7000", "MedTech", 3.0)
print(resonancia)
