## script python per la simulazione di un protocollo di distance vector routing

    - Descrizione: Creare uno script Python che simuli un protocollo di routing semplice, come il Distance Vector Routing. 
        Gli studenti implementeranno gli aggiornamenti di routing tra i nodi, con il calcolo delle rotte più brevi.
    - Obiettivi: Implementare la logica di aggiornamento delle rotte, gestione delle tabelle di routing e calcolo delle distanze tra nodi.
    - Consegne richieste: Codice Python ben documentato, output delle tabelle di routing per ogni nodo e relazione finale che spieghi il funzionamento dello script.

## distance vector
    
    - ogni router inizia sapendo solo se stesso, a distanza 0
    - ogni router trova tutti i router vicini e li aggiunge con distanza 1
    - iterativamente:
        - ogni router manda ad ogni suo vicino la sua tabella
        - ogni router aggiorna la sua tabella con le tabelle che ha ricevuto
