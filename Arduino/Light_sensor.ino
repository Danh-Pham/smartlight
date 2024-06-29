#define light_sensor 10
void setup() {
  // put your setup code here, to run once:
  pinMode(light_sensor,INPUT);
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int light_value = analogRead(light_sensor);
  Serial.println(light_value);
  delay(1000);
}
