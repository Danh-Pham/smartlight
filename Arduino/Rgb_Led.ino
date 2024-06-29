int val;
int redPin = 9;
int greenPin = 10;
int bluePin = 11;
int redIntensity = 200;
int greenIntensity = 200;
int blueIntensity = 200;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String value = Serial.readStringUntil('\n');
    Serial.println(value);

    if (value.indexOf("custom") == -1) {
        if (value.equals("0")) {
          redIntensity = 0;
          blueIntensity = 0;
          greenIntensity = 0;  
        }
        
        if (value.equals("1")) {
          redIntensity = 255;
          blueIntensity = 0;
          greenIntensity = 0;
        } 
//Values from 2 to 7 is for automation only   
        if (value.equals("2")) {
          redIntensity = 0;
          blueIntensity = 255;
          greenIntensity = 0;
        } 
    
        if (value.equals("3")) {
          redIntensity = 0;
          blueIntensity = 0;
          greenIntensity = 255;
        } 
    
        if (value.equals("4")) {
          redIntensity = 255;
          blueIntensity = 0;
          greenIntensity = 255;
        }
    
        if (value.equals("5")) {
          redIntensity = 255;
          blueIntensity = 255;
          greenIntensity = 0;
        }
            
        if (value.equals("6")) {
          redIntensity = 0;
          blueIntensity = 255;
          greenIntensity = 255;
        }
    
        if (value.equals("7")) {
          redIntensity = 255;
          blueIntensity = 255;
          greenIntensity = 255;
        }
    } else {
      //user change intensity of red, green, blue 
      //serial order in form of: "custom,red: {int},green: {int},blue: {int}"
      //example: "custom,red: 100,green: 140,blue: 50"
      String str1 = value.substring(value.indexOf(',')+1, value.length()); //red: 100,green: 140,blue: 50
      String redOrder = str1.substring(0, str1.indexOf(',')); //red: 100
      redIntensity = redOrder.substring(redOrder.indexOf(' '), redOrder.length()).toInt(); // redIntensity = 100
      //Serial.println(redIntensity);

      String str2 = str1.substring(str1.indexOf(',')+1, str1.length());
      String greenOrder = str2.substring(0, str2.indexOf(',')); //green: 140
      greenIntensity = greenOrder.substring(greenOrder.indexOf(' '), greenOrder.length()).toInt();
      //Serial.println(greenIntensity);

      String str3 = str2.substring(str2.indexOf(',')+1, str2.length());
      String blueOrder = str3.substring(0, str3.indexOf(',')); //blue: 50
      blueIntensity = blueOrder.substring(blueOrder.indexOf(' '), blueOrder.length()).toInt();

      //Serial.println(blueIntensity);
    }
    
    analogWrite(redPin, redIntensity);
    analogWrite(bluePin, blueIntensity);
    analogWrite(greenPin, greenIntensity);
  }
  
}
