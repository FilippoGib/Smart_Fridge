#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

SoftwareSerial gpsSerial(4, 3); // Arduino (RX, TX) -> GPS TX goes to arduino RX and GPS RX goes to arduino TX 
TinyGPSPlus gps;

bool stopSending = false; // Flag to stop sending data

void setup() {
  pinMode(2, INPUT);
  Serial.begin(9600);        // Monitor baud rate
  gpsSerial.begin(9600);     // GPS module baud rate
  Serial.println("Initializing GPS...");
}

void loop() {
  // Check if a command is received from the Serial (from the Python script)
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming command
    if (command == "STOP") {
      stopSending = true; // Set the flag to stop sending GPS data
    }
  }

  // If stopSending is true, exit the loop without processing GPS data
  if (stopSending) 
  {
    //DOPO CHE HO RICEVUTO STOPSENDING IGNORO I DATI GPS e mando solo i dati del sensore di movimento
    int state = digitalRead(2);
    if (state == HIGH)
    {
      Serial.print("HIGH\n");
      delay(500);
    }
    else
    {
      Serial.print("LOW\n");
      delay(500);
    }

    return;
  }

  // Read data from GPS module
  while (gpsSerial.available() > 0) {
    char c = gpsSerial.read();
    gps.encode(c);           // Feed the character to TinyGPS++
  }

  // Check if a new location is available
  if (gps.location.isUpdated()) {
    // Format the data as JSON
    String jsonData = "{";
    jsonData += "\"latitude\": " + String(gps.location.lat(), 6) + ",";
    jsonData += "\"longitude\": " + String(gps.location.lng(), 6) + ",";
    jsonData += "\"satellites\": " + String(gps.satellites.value()) + ",";
    jsonData += "\"altitude\": " + String(gps.altitude.meters(), 2);
    jsonData += "}";

    // Send JSON data over Serial
    Serial.println(jsonData);
  }
}
