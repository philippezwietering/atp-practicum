import Controller
import unittest

def runtests(cont, amount):
    if amount < 1:
        print("More than 0 iterations for proper testing")

    for i in range(amount):
        cont.update()