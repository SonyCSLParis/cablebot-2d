# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
STATUS_NEW = 'NEW'
STATUS_RUNNING = 'RUNNING'
STATUS_FINISHED = 'FINISHED'
STATUS_ERROR = 'ERROR'
from collections import deque

#class pour fonctionnement asynchrone
class Task:
    def __init__(self, coro):
        self.coro = coro  # Coroutine à exécuter
        self.name = coro.__name__
        self.status = STATUS_NEW  # Statut de la tâche
        self.return_value = None  # Valeur de retour de la coroutine
        self.error_value = None  # Exception levée par la coroutine

    # Exécute la tâche jusqu'à la prochaine pause
    def run(self):
        try:
            # On passe la tâche à l'état RUNNING et on l'exécute jusqu'à
            # la prochaine suspension de la coroutine.
            self.status = STATUS_RUNNING
            next(self.coro)
        except StopIteration as err:
            # Si la coroutine se termine, la tâche passe à l'état FINISHED
            # et on récupère sa valeur de retour.
            self.status = STATUS_FINISHED
            self.return_value = err.value
        except Exception as err:
            # Si une autre exception est levée durant l'exécution de la
            # coroutine, la tâche passe à l'état ERROR, et on récupère
            # l'exception pour laisser l'utilisateur la traiter.
            self.status = STATUS_ERROR
            self.error_value = err

    def is_done(self):
        return self.status in {STATUS_FINISHED, STATUS_ERROR}

    def __repr__(self):
        result = ''
        if self.is_done():
            result = " ({!r})".format(self.return_value or self.error_value)

        return "<Task '{}' [{}]{}>".format(self.name, self.status, result)

class Loop:
    def __init__(self):
        self._running = deque()

    def _loop(self):
        task = self._running.popleft()
        task.run()
        if task.is_done():
            print(task)
            return
        self.schedule(task)

    def run_until_empty(self):
        while self._running:
            self._loop()

    def schedule(self, task):
        if not isinstance(task, Task):
            task = Task(task)
        self._running.append(task)
        return task
    def run_until_complete(self, task):
        task = self.schedule(task)
        while not task.is_done():
            self._loop()
