#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font
import tkinter
import statemachine as sm
from random import sample

class mainApp():
    # Variables de clase
    afnArray = ["", "", "", ""]
    def __init__(self):
        self.root = Tk()
        self.root.title("Automatas 1")
        # Config de app
        # Seccion de estilo
        fuenteTitulos = font.Font(weight='bold')
        self.root.configure(bg = '#7caeff')
        self.root.geometry("200x250")
        # Seccion de componentes:
        # -> Botones
        self.btnCrear = ttk.Button(self.root, text="Crear nuevo", command=self.winCrear)
        self.btnModif = ttk.Button(self.root, text="Modificar AFN", command=self.winModif)
        self.btnTransf = ttk.Button(self.root, text="Transformar", command=self.winTransformar)
        self.btnMostrar = ttk.Button(self.root, text="Mostrar AFN", command=self.winMostrar)
        self.btnSalir = ttk.Button(self.root, text="Salir", command=quit)
        # Asignar lugar a componentes:
        self.btnCrear.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.btnModif.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.btnTransf.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.btnMostrar.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.btnSalir.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        # Run
        self.root.mainloop()

    def winCrear(self):
        self.builder = tkinter.Toplevel(self.root)
        self.builder.title("Builder")
        # Config de app:
        # -> Seccion de estilo
        fuenteTitulos = font.Font(weight='bold')
        self.builder.configure(bg = '#7caeff')
        self.builder.geometry("300x250")
        # -> Seccion de componentes:
        self.etiqSim = ttk.Label(self.builder, text="Simbolo:", font=fuenteTitulos)
        self.ctextSim = ttk.Entry(self.builder, width=10)
        self.btnCrear = ttk.Button(self.builder, text="Crear", command=self.crear)
        self.comboAFNindex = ttk.Combobox(self.builder, state="readonly", values=["0", "1", "2", "4"])
        # -> Asignar lugar a componentes:
        self.etiqSim.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)
        self.ctextSim.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)
        self.comboAFNindex.pack(side=TOP, expand=False, padx=10, pady=10)
        self.btnCrear.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)

    def crear(self):
        newSM = sm.StateMachine(self.ctextSim.get())
        self.afnArray[int(self.comboAFNindex.get())] = newSM
        print(newSM.maxId)
        # print(len(self.afnArray))
        # print(sample(self.afnArray[0].transitions, 1)[0].symbol)

    def winModif(self):
        self.modif = tkinter.Toplevel(self.root)
        self.modif.title("Modificar AFN")
        # Config de app:
        # -> Seccion de estilo
        fuenteTitulos = font.Font(weight='bold')
        self.modif.configure(bg = '#7caeff')
        self.modif.geometry("480x350")
        # -> Seccion de componentes:
        self.etiqAFN1 = ttk.Label(self.modif, text="AFN 1", font=fuenteTitulos)
        self.etiqOp = ttk.Label(self.modif, text="Operacion", font=fuenteTitulos)
        self.etiqAFN2 = ttk.Label(self.modif, text="AFN 2", font=fuenteTitulos)
        self.etiqNota = ttk.Label(self.modif, text="Nota: El AFN2 desapareceria de la lista", font=fuenteTitulos)
        self.comboOp = ttk.Combobox(self.modif, state="readonly", values=["Union", "Concatenacion", "+", "*", "?"])
        self.comboAFN1 = ttk.Combobox(self.modif, state="readonly", values=["0", "1", "2", "3"])
        self.comboAFN2 = ttk.Combobox(self.modif, state="readonly", values=["0", "1", "2", "4"])
        self.btnAcept = ttk.Button(self.modif, text="Aceptar", command=self.acept)
        # -> Asignar lugar a componentes:
        self.etiqAFN1.pack(side=TOP, expand=False, padx=10, pady=10)
        self.comboAFN1.pack(side=TOP, expand=False, padx=10, pady=10)
        self.etiqOp.pack(side=TOP, expand=False, padx=10, pady=10)
        self.comboOp.pack(side=TOP, expand=False, padx=10, pady=10)
        self.etiqAFN2.pack(side=TOP, expand=False, padx=10, pady=10)
        self.comboAFN2.pack(side=TOP, expand=False, padx=10, pady=10)
        self.etiqNota.pack(side=TOP, expand=False, padx=10, pady=10)
        self.btnAcept.pack(side=TOP, expand=False, padx=10, pady=10)
    
    def acept(self):
        if self.comboOp.get() == "Union":
            AFN1 = self.afnArray[int(self.comboAFN1.get())]
            AFN2 = self.afnArray[int(self.comboAFN2.get())]
            AFN1.union(AFN2)
            self.afnArray[int(self.comboAFN2.get())] = ""
        elif self.comboOp.get() == "Concatenacion":
            AFN1 = self.afnArray[int(self.comboAFN1.get())]
            AFN2 = self.afnArray[int(self.comboAFN2.get())]
            AFN1.concat(AFN2)
            self.afnArray[int(self.comboAFN2.get())] = ""
        elif self.comboOp.get() == "*":
            AFN1 = self.afnArray[int(self.comboAFN1.get())]
            AFN1.cEst()
        elif self.comboOp.get() == "+":
            AFN1 = self.afnArray[int(self.comboAFN1.get())]
            AFN1.cPos()
        elif self.comboOp.get() == "?":
            AFN1 = self.afnArray[int(self.comboAFN1.get())]
            AFN1.cuantif()
        else:
            pass
    
    def winMostrar(self):
        self.show = tkinter.Toplevel(self.root)
        self.show.title("Mostrar AFN")
        # Config de app:
        # -> Seccion de estilo
        fuenteTitulos = font.Font(weight='bold')
        self.show.configure(bg = '#7caeff')
        self.show.geometry("300x250")
        # -> Seccion de componentes:
        self.etiq4 = ttk.Label(self.show, text="AFN para mostrar:", font=fuenteTitulos)
        aux = []
        for v in self.afnArray:
            if v != "":
                aux.append(str(self.afnArray.index(v)))
        self.comboAFNindex = ttk.Combobox(self.show, state="readonly", values=aux)
        self.btnShow = ttk.Button(self.show, text="Mostrar", command=self.mostrar)
        # -> Asignar lugar a componentes:
        self.etiq4.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)
        self.comboAFNindex.pack(side=TOP, expand=False, padx=10, pady=10)
        self.btnShow.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)
    
    def mostrar(self):
        self.show2 = tkinter.Toplevel(self.show)
        self.show2.title("AFN")
        # -> Seccion de estilo
        self.show2.configure(bg = '#7caeff')
        self.show2.geometry("250x500")
        # Obtenemos el AFN seleccionado
        automata = self.afnArray[int(self.comboAFNindex.get())]
        # Creamos Grid para hacer una tabla
        # --- Codigo para checar la cerradura epsilon
        # aux = set()
        # for x in automata.iniState.cEps():
        #     aux.add(x.stateId)
        # print("Cerradura epsilon del estado inicial: " + str(aux))
        # --- Fin de codigo para checar la cerradura epsilon
        l4 = ttk.Label(self.show2, text="Alfabeto")
        l5 = ttk.Label(self.show2, text=str(automata.alphabet))
        l6 = ttk.Label(self.show2, text="Estado inicial:")
        l7 = ttk.Label(self.show2, text=str(automata.iniState.stateId))
        l8 = ttk.Label(self.show2, text="Estados finales:")
        idFinales = set()
        for x in automata.finalStates:
            idFinales.add(x.stateId)
        l9 = ttk.Label(self.show2, text=str(idFinales))
        l4.grid(column=1, row=1)
        l5.grid(column=2, row=1)
        l6.grid(column=1, row=2)
        l7.grid(column=2, row=2)
        l8.grid(column=1, row=3)
        l9.grid(column=2, row=3)
        fila = 4
        for e in automata.states:
            c1 = str(e.stateId)
            for t in e.stateTransitions:
                c2 = str(t.symbol)
                c3 = str(t.destiny.stateId)
                l1 = ttk.Label(self.show2, text=c1 + " ->")
                l2 = ttk.Label(self.show2, text=c2 + " ->")
                l3 = ttk.Label(self.show2, text=c3)
                l1.grid(column=1, row=fila)
                l2.grid(column=2, row=fila)
                l3.grid(column=3, row=fila)
                fila += 1

    def winTransformar(self):
        self.show3 = tkinter.Toplevel(self.root)
        self.show3.title("Mostrar AFN")
        # Config de app:
        # -> Seccion de estilo
        fuenteTitulos = font.Font(weight='bold')
        self.show3.configure(bg = '#7caeff')
        self.show3.geometry("300x250")
        # -> Seccion de componentes:
        self.etiq5 = ttk.Label(self.show3, text="AFN para transformar:", font=fuenteTitulos)
        aux = []
        for v in self.afnArray:
            if v != "":
                aux.append(str(self.afnArray.index(v)))
        self.comboAFDindex = ttk.Combobox(self.show3, state="readonly", values=aux)
        self.btnShow2 = ttk.Button(self.show3, text="Mostrar", command=self.transformar)
        # -> Asignar lugar a componentes:
        self.etiq5.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)
        self.comboAFDindex.pack(side=TOP, expand=False, padx=10, pady=10)
        self.btnShow2.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)

    def transformar(self):
        AFN = self.afnArray[int(self.comboAFDindex.get())]
        self.afnArray[3] = AFN.convert()

# Inicia app
mainApp()