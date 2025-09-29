int VRx = A0;
int VRy = A1;
int SW = 2;

void setup() {
  Serial.begin(9600);
  pinMode(SW, INPUT_PULLUP);  // joystick button
}

void loop() {
  int x = analogRead(VRx);  // 0–1023
  int y = analogRead(VRy);  // 0–1023
  int button = digitalRead(SW);

  // Send values as "x,y,button"
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(button);

  delay(50);  // reduce spam
}
