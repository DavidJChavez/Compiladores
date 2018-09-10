#!/usr/bin/env python
# -*- coding: utf-8 -*-
import queue

class State:
    # Para inicializar se necesita un id y un conjunto de transiciones
    # State attributes
    # stateId = 0;
    # stateTransitions = set() # State transitions (Set)
    # State methods
    def __init__(self, stateId=0, stateTransitions=set()):
        self.stateId = stateId
        self.stateTransitions = stateTransitions
    def addTransitions(self, transitionSet=set()):
        self.stateTransitions = self.stateTransitions.union(transitionSet)
    def setId(self, stateId):
        self.stateId = stateId
    def cEps(self):
        # Calcula la cerradura epsilon, necesita un estado y devuelve un conjunto de estados
        stack = []
        conj = set()
        stack.append(self)
        while len(stack) != 0:
            actual_state = stack.pop()
            if actual_state not in conj:
                conj.add(actual_state)
                for t in actual_state.stateTransitions:
                    if t.symbol == "eps":
                        stack.append(t.destiny)
        return conj
    def setCEps(self, conjIn):
        conjOut = set()
        for x in conjIn:
            conjOut = conjOut.union(x.cEps())
        return conjOut
    def move(self, char):
        # Recibe un parametro de entrada: Un simbolo (String)
        conjOut = set()
        for t in self.stateTransitions:
            if t.symbol == char:
                conjOut.add(t.destiny)
        return conjOut
    def setMove(self, conjIn, char):
        # Recibe dos parametros de entrada: Un conjunto de estados (set<State>) y un simbolo (String)
        conjOut = set()
        for x in conjIn:
            conjOut = conjOut.union(x.move(char))
        return conjOut
    def goTo(self, char):
        # Recibe un parametro de entrada: Un simbolo (String)
        return self.setCEps(self.move(char))

class Transition:
    # Para inicializar se necesita un simbolo y un estado destino
    # Transition attributes
    # symbol = ''
    # destiny = object
    # Transition methods
    def __init__(self, symbol, nextState):
        self.symbol = symbol
        self.destiny = nextState
    def setSymbol(self, symbol):
        self.symbol = symbol
    def changeDestiny(self, nextState):
        self.destiny = nextState

class StateMachine:
    # Para inicializar se necesita un simbolo solamente
    # StateMachine attributes
    # states = set()
    # iniState = object
    # alphabet = set()
    # transitions = set()
    # finalStates = set()
    maxId = -1
    # StateMachine attributes
    def __init__(self, symbol=""):
        self.alphabet = {symbol}
        temp_state2 = State(StateMachine.maxId + 2, set())
        temp_transition = Transition(symbol, temp_state2)
        self.transitions = set()
        self.transitions.add(temp_transition)
        temp_state1 = State(StateMachine.maxId + 1, {temp_transition})
        self.states = {temp_state1, temp_state2}
        self.iniState = temp_state1
        self.finalStates = {temp_state2}
        StateMachine.maxId += 2

    def union(self, FSM):
        # Crea una transicion a self.iniState -> Crea un estado -> Asigna el nuevo estado como inicial
        temp_transition = Transition("eps", self.iniState)
        self.transitions.add(temp_transition)
        temp_state = State(StateMachine.maxId + 1, {temp_transition})
        StateMachine.maxId += 1
        self.states.add(temp_state)
        self.iniState = temp_state
        # Crea una transicion a FSM.iniState -> Agrega transicion a self.iniState
        temp_transition = Transition("eps", FSM.iniState)
        self.transitions.add(temp_transition)
        self.iniState.stateTransitions.add(temp_transition)
        # Crea estado final -> Agrega el estado a self.states
        temp_state = State(StateMachine.maxId + 1, set())
        StateMachine.maxId += 1
        self.states.add(temp_state)
        # Agrega las transiciones finales de self y FSM -> Las agrega a self.transitions
        temp_transition = Transition("eps", temp_state)
        self.transitions.add(temp_transition)
        for x in self.finalStates:
            x.addTransitions({temp_transition})
        self.finalStates.clear()
        self.finalStates = self.finalStates.union({temp_state})
        for x in FSM.finalStates:
            x.addTransitions({temp_transition})
        # Une los alfabetos de self y FSM -> Agrega los estados y transiciones de FSM a self -> Reemplaza self.finalStates
        self.alphabet = self.alphabet.union(FSM.alphabet)
        self.states = self.states.union(FSM.states)
        self.transitions = self.transitions.union(FSM.transitions)

    def concat(self, FSM):
        # Asigna las transiciones de FSM.iniState a self.finalStates
        for x in self.finalStates:
            x.addTransitions(FSM.iniState.stateTransitions)
        # Eliminamos el estado de FSM
        FSM.states.discard(FSM.iniState)
        #Agregamos todos los estados y transiciones y alfabeto de FSM a self
        self.states = self.states.union(FSM.states)
        self.transitions = self.transitions.union(FSM.transitions)
        self.alphabet = self.alphabet.union(FSM.alphabet)
        # Asignamos FSM.finalStates como self.finalStates
        self.finalStates = FSM.finalStates

    def cEst(self):
        # Creamos trancision entre el self.finalStates y self.iniState
        temp_transition = Transition("eps", self.iniState)
        self.transitions.add(temp_transition)
        for x in self.finalStates:
            x.addTransitions({temp_transition})
        # Crea una transicion a self.iniState -> Crea un estado -> Asigna el nuevo estado como inicial
        temp_transition = Transition("eps", self.iniState)
        self.transitions.add(temp_transition)
        temp_state = State(StateMachine.maxId + 1, {temp_transition})
        StateMachine.maxId += 1
        self.states.add(temp_state)
        self.iniState = temp_state
        # Crea estado final -> Agrega el estado a self.states
        temp_state = State(StateMachine.maxId + 1, set())
        StateMachine.maxId += 1
        self.states.add(temp_state)
        # Agregar transiciones finales
        temp_transition = Transition("eps", temp_state)
        self.transitions.add(temp_transition)
        for x in self.finalStates:
            x.addTransitions({temp_transition})
        self.finalStates = {temp_state}
        for x in self.finalStates:
            temp_transition = Transition("eps", x)
        self.transitions.add(temp_transition)
        self.iniState.addTransitions({temp_transition})
        
    def cPos(self):
        # Creamos trancision entre el self.finalStates y self.iniState
        temp_transition = Transition("eps", self.iniState)
        self.transitions.add(temp_transition)
        for x in self.finalStates:
            x.addTransitions({temp_transition})
        # Crea una transicion a self.iniState -> Crea un estado -> Asigna el nuevo estado como inicial
        temp_transition = Transition("eps", self.iniState)
        self.transitions.add(temp_transition)
        temp_state = State(StateMachine.maxId + 1, {temp_transition})
        StateMachine.maxId += 1
        self.states.add(temp_state)
        self.iniState = temp_state
        # Crea estado final -> Agrega el estado a self.states
        temp_state = State(StateMachine.maxId + 1, set())
        StateMachine.maxId += 1
        self.states.add(temp_state)
        # Agregar transiciones finales
        temp_transition = Transition("eps", temp_state)
        self.transitions.add(temp_transition)
        for x in self.finalStates:
            x.addTransitions({temp_transition})
        self.finalStates = {temp_state}

    def cuantif(self):
        # Crea una transicion a self.iniState -> Crea un estado -> Asigna el nuevo estado como inicial
        temp_transition = Transition("eps", self.iniState)
        self.transitions.add(temp_transition)
        temp_state = State(StateMachine.maxId + 1, {temp_transition})
        StateMachine.maxId += 1
        self.states.add(temp_state)
        self.iniState = temp_state
        # Crea estado final -> Agrega el estado a self.states
        temp_state = State(StateMachine.maxId + 1, set())
        StateMachine.maxId += 1
        self.states.add(temp_state)
        # Agregar transiciones finales
        temp_transition = Transition("eps", temp_state)
        self.transitions.add(temp_transition)
        for x in self.finalStates:
            x.addTransitions({temp_transition})
        self.finalStates = {temp_state}
        for x in self.finalStates:
            temp_transition = Transition("eps", x)
        self.transitions.add(temp_transition)
        self.iniState.addTransitions({temp_transition})

    def convert(self):
        E = set()
        aux = StateSi(0, self.iniState.cEps(), set())
        Si_NoAnalizados = queue.Queue()
        Si_NoAnalizados.put(aux)
        E.add(aux)
        newAFD = AFD({aux}, set(),self.alphabet)
        newAFD.iniState = aux
        SiId = 1
        # Empieza analisis
        # Nota: Rehacer el algoritmo de transformacion a AFD
        while not Si_NoAnalizados.empty():
            Si = Si_NoAnalizados.get()
            for x in self.alphabet:
                setStates = Si.setGoTo(x)
                for y in E.copy():
                    if len(setStates) == 0:
                        pass
                    elif setStates == y.setStates:
                        y.stateTransitions.add(Transition(x, y))
                        for z in setStates:
                            if (self.finalStates - setStates) != self.finalStates:
                                newAFD.finalStates.add(y)
                    else:
                        newSi = StateSi(SiId, setStates, set())
                        SiId += 1
                        Si_NoAnalizados.put(newSi)
                        E.add(newSi)
                        Si.stateTransitions.add(Transition(x, newSi))
                        newAFD.states.add(newSi)
                        for z in setStates:
                            if self.finalStates - setStates != self.finalStates:
                                newAFD.finalStates.add(newSi)
        for x in newAFD.states:
            newAFD.transitions = newAFD.transitions.union(x.stateTransitions)
        return newAFD
                
class AFD:
    def __init__(self, states=set(), setTransitions=set(), alphabet=set()):
        self.states = states
        self.transitions = set()
        self.transitions = setTransitions
        self.alphabet = alphabet
        self.iniState = object
        self.finalStates = set()
        StateMachine.maxId += 2


class StateSi:
    def __init__(self, stateId, setStates=set(), setTransitions=set()):
        self.stateId = stateId
        self.setStates = setStates
        self.stateTransitions = setTransitions
        self.check = False
    def setGoTo(self, char):
        conjOut = set()
        for x in self.setStates:
            conjOut = conjOut.union(x.goTo(char))
        return conjOut
# Nota mental: Python usa las variables declaradas en la clase como "static" en Java
# es decir, para todas las instancias es el mismo valor

# Preguntas: Puede un automata tener varios estados finales?