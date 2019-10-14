# trading_strategy

prossimi passi:

- modificare il dataExtractor, usando la libreria csv e numpy per scrivere, leggere i file csv e accedere ai dati
    - questo comporta sostituire il json con csv
    - questo permette, con numpy di accedere a un'intera colonna di valori direttamente con numpy senza for loops
    - info qua:
        - https://janakiev.com/blog/csv-in-python/
        - https://realpython.com/python-csv/
        - https://www.programiz.com/python-programming/working-csv-files

- dare la possibilità d vedere se una candela di volume è verde o rossa (da fare al momento delle candlesticks)
- sviluppo dei sistemi BUY/SELL (FATTO) e BUY & WAIT
    
- sviluppo della GUI con QT:
    - https://doc.qt.io/qtforpython/tutorials/index.html
    
- implementazione di layers AND e OR
- inserire nuovi indicatori, a partire da quelli della libreria di trading
    - documentazione: https://mrjbq7.github.io/ta-lib/doc_index.html
    
- creare nuovi metodi


buy and wait:
come deve essere
lancio una normale strategia di buy e ottengo i risultati
per la strategia di vendita devo solo impostare un periodo massimo di valutazione.
si cerca in questo periodo, dopo ogni segnale di acquisto, il valore massimo che si ottiene.
statisticamente devo ricavare: 
    - tutti i valori massimi
    - fare una media dei valori, così da ottenere il guadagno medio
    - a questo punto ripercorro e trovo in che date (cioè a quale distanza di tempo) vengono ottenuti i valori medi (se vengono ottenuti)
    - cosi posso calcolare a quale distanza media si ottiene un valore medio
    - devo pero' calcolare anche le percentuali di successo
    - i vari risultati devono essere salvati in modo da poter essere confrontati (il senso di questa strategia è cercare
        il tasso di successo migliore variando i periodi di sell)
    
