const int solv0_D0 = 16;
const int solv1_D1 = 5;
const int solv2_D2 = 4;
const int solv3_D3 = 0;
const int solv4_D4 = 2;
const int solv5_D5 = 14;
const int solv6_D6 = 12;
const int solv7_D7 = 13;
const int solv8_D8 = 15;


void setup() 
{
  Serial.begin(115200);
  //pinMode(solv1, OUTPUT);
  //pinMode(solv2, OUTPUT);
  // pinMode(solv3, OUTPUT);
  pinMode(solv0_D0, OUTPUT);
}

void loop() 
{
  if(Serial.available()>1)
  {
    int port = Serial.parseInt();
    int pwmV = Serial.parseInt();
    Serial.print("port: "); Serial.print(port); Serial.print(" pwmValue: "); Serial.println(pwmV);
    if(port==16)
    {
      // sol_valve connected to D0
      analogWrite(solv0_D0, pwmV);
      delay(100);
      //analogWrite(solv0_D0, 0);
      //delay(5000);
    }
    else if(port==5)
    {
      // sol_valve connected to D1
      analogWrite(solv1_D1, pwmV);
      delay(100);
    }
    else if(port==4)
    {
      // sol_valve connected to D2
      analogWrite(solv2_D2, pwmV);
      delay(100);
    }
  }
}
