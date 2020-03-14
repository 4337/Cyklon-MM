# -*- coding: utf-8 -*-

'''
Pierwszy na świecie debugger filtrujący hehehe lol
Ogólnie fajna koncepcja, zamiast tworzyć skomplikowane oprogramowanie monitorujące
Piszemy fragment kodu debuggera instalujemy go jako "Just In Time Debugger" i filtrujemy 
procesy. Jeżeli crash występuje w jednym z procesów które nas interesują to robimy "coś"
np. logujemy crash_dump do pliku kopiujemy 'repro' etc, jeżeli nie to odłączamy debugger i olewamy 
process. Dodatkowy plus to fakt, że nie musimy się w ogóle przejmować procesami potomnymi ^^
'''

import pydbg