#define red_LED 2
#define motion_sensor 6


void setup() {
  // put your setup code here, to run once:
  pinMode(motion_sensor,INPUT);
  pinMode(red_LED,OUTPUT);
  Serial.begin(9600);
  cli(); // Stop interrupts for till we make the settings
  // reset the control register to make sure starting with everything disabled
  TCCR1A = 0;
  TCCR1B = 0;
  // set prescalar
  TCCR1B |= B00000100;
  // enable compare match mode on register A
  TIMSK1 |= B00000010;
  // set the value of register A to 31250
  OCR1A = 65535;
  // enable back the interrupts
  sei();
}
// this IRS triggers each 1000ms
ISR(TIMER1_COMPA_vect){
  TCNT1 = 0;
  int motion_value = digitalRead(6);
  Serial.println(motion_value);
//  Serial.print(" ");
//  Serial.println(light_value);
  }
  
void loop() {
  // put your main code here, to run repeatedly:
  int motion_value = digitalRead(motion_sensor);
    if(motion_value==HIGH){
        digitalWrite(red_LED,HIGH);
      }
    else{
        digitalWrite(red_LED,LOW);
      }
}
