void setup() {
  // put your setup code here, to run once:
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Half Power");
  analogWrite(3, 35);
  delay(2000);
  Serial.println("Full Power");
  analogWrite(3, 255);
  delay(2000);
}
