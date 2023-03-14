// Funzione javascript che implementa un orologio
// con il numero dei secondi che si auto aggiorna

function Orologio(){
    // Assegno alle variabili ore minuti e secondi
    var data = new Date();
    var ore = data.getHours();
    var min = data.getMinutes();
    var sec = data.getSeconds();

    var settimana = new Array(6);
    settimana[1] = "Lunedì";
    settimana[2] = "Martedì";
    settimana[3] = "Mercoledì";
    settimana[4] = "Giovedì";
    settimana[5] = "Venerdì";
    settimana[6] = "Sabato";
    settimana[7] = "Domenica";

    var giorni = settimana[data.getDay()];


    // Assegno ad orario una stringa composta da ore minuti e secondi
    var orario = giorni + " " + ore + ":" + min + ":" + sec;

    // Per richiamare lo script nell'html
    // Mi aiuto con la funzione document.getElementById, che ritorna
    // l'elemento dell'id specificato.
    // Quindi nell'html lo richiamerò nei tag con id = "OROLOGIO"
    //Per far partire la funzione la lancio con onload = "Orologlio()" all'interno del body
    // Con setTimeout imposto l'intervallo di aggiornamento a 1 secondo
    document.getElementById("OROLOGIO").innerText = orario;
    window.setTimeout("Orologio()", 1000);
}