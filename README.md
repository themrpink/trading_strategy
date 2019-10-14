# trading_strategy

prossimi passi:

- modificare il dataExtractor, usando la libreria csv e numpy per scrivere, leggere i file csv e accedere ai dati
    - questo comporta sostituire il json con csv
    - questo permette, con numpy di accedere a un'intera colonna di valori direttamente con numpy senza for loops
    - info qua:
        - https://janakiev.com/blog/csv-in-python/
        - https://realpython.com/python-csv/
        - https://www.programiz.com/python-programming/working-csv-files
    
- algoritmo di identificazione dei gruppi di volumi:
    - realizzato e funzionante. Adesso:
        - dare la possibilità d vedere se una candela di volume è verde o rossa (da fare al momento delle candlesticks)
- sviluppo dei sistemi BUY/SELL e BUY & WAIT
    
- sviluppo della GUI con QT:
    - https://doc.qt.io/qtforpython/tutorials/index.html
    
- implementazione di layers AND e OR
- inserire nuovi indicatori, a partire da quelli della libreria di trading
    - documentazione: https://mrjbq7.github.io/ta-lib/doc_index.html
    
- creare nuovi metodi
