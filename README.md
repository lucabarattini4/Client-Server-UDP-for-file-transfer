# Client-Server-UDP-for-file-transfer

Istruzioni d’uso
Aprire e avviare il file server.py e il file client.py.
Digitare i comandi sulla console del client.
All’interno dell’elaborato consegnato vi saranno due cartelle, client e server,
contenenti a loro volta delle sottocartelle. Per il client troviamo le sottocartelle
”myFiles”, dove è possibile inserire alcuni file di cui si può eseguire il
comando put su server, e ”received”, cartella contenente tutti i file ricevuti
dal server. Per il server troviamo solo la cartella ”resources” che contiene
tutti i file in suo possesso. Se si necessita di inserire dei file manualmente su
server si proceda a caricare il materiale nella cartella ”resources”, altrimenti
si inseriscano nella cartella ”myFiles” del client e si proceda ad comando di
put.

Sintassi
Si noti che le parole chiave dei comandi (list, get, put e close) non sono case
sensitive, ovvero possono essere sia scritte in minuscolo, maiuscolo oppure
solo qualche lettera in maiuscolo o minuscolo, mentre i nomi dei file sono
case sensitive. In caso di scrittura del nome file in modo scorretto il file non
verrà trovato e trasmesso. In caso di assenza di estensione il file non verrà
trovato. Ci si assicuri anche che non vi siano spazi a seguire il nome del file
oppure quest’ultimo non sarà trovato.

• Comando List → list

• Comando Get → get ⟨nomeFile.estensione⟩

• Comando Put → put ⟨nomeFile.estensione⟩

• Comando Close → close


