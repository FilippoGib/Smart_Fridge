#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

SoftwareSerial gpsSerial(4, 3); // Arduino (RX, TX) -> GPS TX goes to arduino RX and GPS RX goes to arduino TX 
TinyGPSPlus gps;

const int switchPin = 12; //You have to put the power of the switch in 3.3V

bool stopSendingGPSData = false; // Flag to stop sending data
bool stopSendingSwitchState = false;

void setup() 
{
  pinMode(2, INPUT);         // To read movement sensor data
  ///////
  pinMode(LED_BUILTIN, OUTPUT);
  ///////
  Serial.begin(9600);        // Monitor baud rate
  gpsSerial.begin(9600);     // GPS module baud rate
  Serial.println("Initializing GPS...");
}

void loop() 
{
  // Check if a command is received from the Serial (from the Python script)
  if (Serial.available() > 0) 
  {
    String command = Serial.readStringUntil('\n'); // Read the incoming command
    if (command == "STOP") 
    {
      stopSendingGPSData = true; // Set the flag to stop sending GPS data
    }
  }

  // If stopSendingGPSData is true, exit the loop without processing GPS data
  if (stopSendingGPSData) 
  {
    //DOPO CHE HO RICEVUTO stopSendingGPSData IGNORO I DATI GPS e mando solo i dati del sensore di movimento

    int state = digitalRead(2);
    if (state == HIGH)
    {
      //leggo lo stato dell'interruttore e lo mando insieme a HIGH sul seriale
      int state = digitalRead(switchPin); // Legge lo stato dell'interruttore
      String message;
      if (state == HIGH) {
        message = "HIGH, INSERTION\n";
      } else {
        message = "HIGH, EXTRACTION\n";
      }
      Serial.print(message);
      delay(500);
    }

    else
    {
      Serial.print("LOW\n");
      delay(500);
    }

    ////////////////////////////////////////////////////
    if(Serial.available() > 0)
    {
      String status = Serial.readStringUntil('\n'); // Read the incoming command
      if (status == "CAMERA OK")
      {
          digitalWrite(LED_BUILTIN, HIGH);
      }
      if (status == "BARCODE OK") 
      {
        digitalWrite(LED_BUILTIN, LOW); // Set the flag to stop sending GPS data
      }
      // FOR DEBUGGING PURPOSES
      else if (status == "DATE OK")
      {
        digitalWrite(LED_BUILTIN, HIGH); // Set the flag to stop sending GPS data
      }

      else if(status == "PRODUCT OK")
      {
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
    ///////////////////////////////////////////////////
  
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
