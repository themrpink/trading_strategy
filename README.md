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


- ORGANIZZAZIONE DEL CODICE

deve essere chiaro come è organizzato il codice.
    - motore - estrattore - disegnatore - strategie
    - indicatori
    - metodi 
    - visual interface
    
    i dati che vengono prodotti devono essere chiaramente rintracciabili con un criterio uniforme
    anche il modo di salvare i dati deve essere ottimizzato per quelle che saranno le sue funzioni:
        1) calcolare statistiche
        2) confrontare dati
        3) disegnare grafici
    al momento ho una gran confusione su quali dati salvo, come e dove.
        1) ci sono i file csv principali con tutti i dati raw
            a) andranno creati dei sottofile raw con dei timeframe specifici limitati scelti come prima cosa dall'utente
        2) da questi estraggo i dati e creo delle candlestick in json (ogni candlestick un dizionario)
        3) li creano gli indicatori, con un meccanismo un po' contorto 
            a) salvano il file creato in una lista, così da non crearlo più volte
            b) riducono il timeframe al timestamp corrente con l'avanzare della strategia, cioè solo dopo che un layer è stato completato
        4) il metodo prende i risultati dell'indicatori, li confronta e restituisce un risultato completo alla strategia
        5) la strategia, una volta finita, restituisce tutti i risultati ordinati e l'esito con timestamp finale
        6) queste informazioni vengono salvate in un file come json
            a) potrebbe essere utile, oltre alla parte verbosa, codificare i dati così da eleborarli meglio (codici di indicatori per                  
               esempio che corrispondono a enum
            b) capire il formato migliore per salvare i file
