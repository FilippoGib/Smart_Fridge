const int switchPin = 12; // Pin collegato all'interruttore
// devi mettere il power in 3.3V

void setup() {
    Serial.begin(9600); // Avvia la comunicazione seriale
    pinMode(switchPin, INPUT_PULLUP); // Abilita la resistenza interna di pull-up
}

void loop() {

    int stato = digitalRead(switchPin); // Legge lo stato dell'interruttore
    
    if (stato == HIGH) {
        Serial.println("Interruttore: ON");
    } else {
        Serial.println("Interruttore: OFF");
    }

    delay(500); // Piccola pausa per evitare aggiornamenti eccessivi
}
