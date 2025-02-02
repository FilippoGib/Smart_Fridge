#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

#define CAMERA_LED 9
#define CODE_LED 8
#define DATE_LED 7
#define SERVER_LED 6
#define ERROR_LED 5

#define BASE_STATE 0
#define CAMERA_STATE 1
#define CODE_STATE 2
#define DATE_STATE 3
#define SERVER_STATE 4
#define ERROR_STATE 5

int state = BASE_STATE;
long timer;
unsigned long cheekyTimer = 0;
bool cheeky = false;


SoftwareSerial gpsSerial(4, 3); // Arduino (RX, TX) -> GPS TX goes to arduino RX and GPS RX goes to arduino TX 
TinyGPSPlus gps;

const int switchPin = 12; //You have to put the power of the switch in 3.3V

bool stopSendingGPSData = false; // Flag to stop sending data
bool stopSendingSwitchState = false;

void setup() 
{
  pinMode(2, INPUT);         // To read movement sensor data
  ///////
  pinMode(switchPin, INPUT);
  ///////
  pinMode(CODE_LED, OUTPUT);
  pinMode(CAMERA_LED, OUTPUT);
  pinMode(DATE_LED, OUTPUT);
  pinMode(SERVER_LED, OUTPUT);
  pinMode(ERROR_LED, OUTPUT);
  timer = millis();
  ///////
  Serial.begin(9600);        // Monitor baud rate
  gpsSerial.begin(9600);     // GPS module baud rate
  Serial.println("Initializing GPS...");
}

void changeState(int s) {
  state = s;
  timer = millis();
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
    Serial.println(state);
    int move_sensor_state = digitalRead(2);
    if (move_sensor_state == HIGH)
    {
      //leggo lo stato dell'interruttore e lo mando insieme a HIGH sul seriale
      int switch_state = digitalRead(switchPin); // Legge lo stato dell'interruttore
      String message;
      if (switch_state == HIGH) {
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
    //check states:
    //base state: switch to camera if receive message c (camera on)
    if (state == BASE_STATE && Serial.available() > 0) {
      int msg = Serial.read();
      if (msg == 'c') {
        changeState(CAMERA_STATE);
        digitalWrite(CAMERA_LED, HIGH);
      }
    }
    //camera state: switch to code if receive message b (barcode read) or to error if receive error
    if (state == CAMERA_STATE) {
      if (Serial.available() > 0) {
        int msg = Serial.read();
        if (msg == 'b') {
          changeState(CODE_STATE);
          digitalWrite(CODE_LED, HIGH);
        } else if (msg == 'o') {
        	changeState(BASE_STATE);
        	digitalWrite(CAMERA_LED, LOW);
        }
      }
    }
    //code state: switch to code if receive message d (date read) or switch to error if receive error
    else if (state == CODE_STATE) {
      if (Serial.available() > 0) {
        int msg = Serial.read();
        if (msg == 'd') {
          changeState(DATE_STATE);
          digitalWrite(DATE_LED, HIGH);
        } else if (msg == 'e') {
          changeState(ERROR_STATE);
          digitalWrite(ERROR_LED, HIGH);
          digitalWrite(CODE_LED, LOW);
        } else if (msg == 'o') {
        	changeState(BASE_STATE);
        	digitalWrite(CAMERA_LED, LOW);
          digitalWrite(CODE_LED, LOW);
        }
      }
    }
    //date state: switch to server if receive message s (server response received) or switch to error if receive error
    else if (state == DATE_STATE) 
    {
      if (cheeky == false) 
      {
        cheekyTimer = millis();
        cheeky = true;
      }
      if (millis() - cheekyTimer > 2000) 
      {
        changeState(SERVER_STATE);
        digitalWrite(SERVER_LED, HIGH);
        cheeky = false;
      }
      
      if (Serial.available() > 0) 
      {
        int msg = Serial.read();
        if (msg == 's') {
          changeState(SERVER_STATE);
          digitalWrite(SERVER_LED, HIGH);
        } else if (msg == 'e') {
          changeState(ERROR_STATE);
          digitalWrite(ERROR_LED, HIGH);
          digitalWrite(CODE_LED, LOW);
          digitalWrite(DATE_LED, LOW);
        } else if (msg == 'o') {
        	changeState(BASE_STATE);
        	digitalWrite(CAMERA_LED, LOW);
          digitalWrite(CODE_LED, LOW);
          digitalWrite(DATE_LED, LOW);
        }
      }
    }
    //server or error state: switch back to camera state after 0.5 sec
    else if ((state == SERVER_STATE || state == ERROR_STATE) && millis() - timer > 500) {
      changeState(CAMERA_STATE);
      digitalWrite(ERROR_LED, LOW);
      digitalWrite(CODE_LED, LOW);
      digitalWrite(DATE_LED, LOW);
      digitalWrite(SERVER_LED, LOW);
    }
    ///////////////////////////////////////////////////
  }

  if(!stopSendingGPSData)
  {
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
}
