void setup() {
  pinMode(2, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  int state = digitalRead(2);
  if (state == HIGH)
  {
    digitalWrite(LED_BUILTIN, HIGH); // Turn the LED on
    Serial.print("HIGH\n");
    delay(500);               // Wait for 1 second (1000 milliseconds) 
  }
  else
  {
    digitalWrite(LED_BUILTIN, LOW);  // Turn the LED off
    Serial.print("LOW\n");
    delay(500);
  }
}
