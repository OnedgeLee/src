#include <Wire.h>
#include <SPI.h>
#include <JY901.h>

/* Define Pin & Flag */
uint8_t ssPin    = D8;
uint8_t resetPin = D3;
// uint8_t ssPin    = 10;
// uint8_t resetPin = 9;
uint8_t ch0 = 0;
uint8_t ch1 = 1;
uint8_t ch2 = 2;
uint8_t ch3 = 3;
uint8_t ch4 = 4;
uint8_t ch5 = 5;
uint8_t ch6 = 6;
uint8_t ch7 = 7;
/* Only for Arduino to use SPI */

/* End */
uint16_t BIT_CONV = 13107;

void softreset()
{
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
  digitalWrite(ssPin, LOW);
  buf[0] = (0x06<<4) + 0x00;
  buf[1] = 0x00;
  buf[2] = 0x00;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH);
  SPI.endTransaction();
}

void setup() 
{
  Serial.begin(115200);
  SPI.begin();
  JY901.StartIIC();
  pinMode(resetPin, OUTPUT); pinMode(ssPin, OUTPUT);
  // pinMode(D5, OUTPUT);
  digitalWrite(ssPin, LOW); 
  delay(500);
  digitalWrite(ssPin, HIGH); digitalWrite(resetPin, LOW); delay(5);
  digitalWrite(resetPin, HIGH);
  softreset();
  delay(500);
  delay(4500);
}

void setChVolt(uint16_t SIG, uint8_t _addr)
{
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
  digitalWrite(ssPin, LOW);
  buf[0] = (0x03 << 4) + _addr;
  buf[1] = SIG / 256;
  buf[2] = SIG % 256;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH);
  SPI.endTransaction();
}

void loop() 
{
  /*
  float V_VAC2  = 4.0;
  float V_VAC10 = 4.0;
  float V_VAC6  = 4.0;
  float V_P2    = 4.13; // 4.1 ~ 4.2
  float V_P10   = 4.4;  // 4.3 ~ 4.5 or 6
  float V_P6    = 4.4;  // starts from 4.4
  */

  float V_VAC2  = 0;
  float V_VAC10 = 0;
  float V_VAC6  = 4.0;
  float V_P2    = 0; // 4.1 ~ 4.2
  float V_P10   = 0;  // 4.3 ~ 4.5 or 6
  float V_P6    = 4.6;  // starts from 4.4 ~ 4.6

  uint16_t SIG2  = (uint16_t) (V_P2 * BIT_CONV);
  uint16_t SIG6  = (uint16_t) (V_P6 * BIT_CONV);
  uint16_t SIG10 = (uint16_t) (V_P10 * BIT_CONV);
  uint16_t VAC_SIG2  = (uint16_t) (V_VAC2 * BIT_CONV);
  uint16_t VAC_SIG6  = (uint16_t) (V_VAC6 * BIT_CONV);
  uint16_t VAC_SIG10 = (uint16_t) (V_VAC10 * BIT_CONV);
  JY901.GetAngle();
  float r = (float)JY901.stcAngle.Angle[0]/32768*180;
  float p = (float)JY901.stcAngle.Angle[1]/32768*180;
  float y = (float)JY901.stcAngle.Angle[2]/32768*180;
  Serial.print(r); Serial.print(","); Serial.print(p); Serial.print(","); Serial.println(y);
  // Wemos
  setChVolt(VAC_SIG6, ch6); // 6 -
  setChVolt(VAC_SIG2, ch3); // 2 -
  setChVolt(VAC_SIG10, ch1); // 10 -
  setChVolt(SIG10, ch2);     // 10 +
  setChVolt(SIG6, ch5);     // 6 +
  setChVolt(SIG2, ch4);     // 2 +
  // setChVolt(SIG, ch2); // 2 
  // setChVolt(SIG, ch3); setChVolt(VAC_SIG, ch4); // 10, 2 (+, -)
  // setChVolt(SIG, ch2); setChVolt(VAC_SIG, ch1); // 6, 10 (+, -)
  //setChVolt(SIG, ch6); setChVolt(VAC_SIG, ch5); // 2, 6  (+, -)
  delay(25);

  /*
  for (int i=0; i<1001; i++)
  {
    V_P = 3.2 + (float) i * 0.001;
    uint16_t SIG = (uint16_t) (V_P * BIT_CONV);
    uint16_t VAC_SIG = (uint16_t) (V_VAC * BIT_CONV);
    // Arduino
    // setChVolt(SIG, ch7); setChVolt(SIG, ch6);
    // setChVolt(SIG, ch3); setChVolt(SIG, ch2);
    // setChVolt(SIG, ch1); setChVolt(SIG, ch0);
    
    JY901.GetAngle();
    float r = (float)JY901.stcAngle.Angle[0]/32768*180;
    float p = (float)JY901.stcAngle.Angle[1]/32768*180;
    float y = (float)JY901.stcAngle.Angle[2]/32768*180;
    Serial.print(i); Serial.print(","); Serial.print(r); Serial.print(","); Serial.print(p); Serial.print(","); Serial.println(y);
    // Wemos
    setChVolt(VAC_SIG, ch6); //
    setChVolt(SIG, ch5);
    // setChVolt(SIG, ch2); // 2 
    // setChVolt(SIG, ch3); setChVolt(VAC_SIG, ch4); // 10, 2 (+, -)
    // setChVolt(SIG, ch2); setChVolt(VAC_SIG, ch1); // 6, 10 (+, -)
    //setChVolt(SIG, ch6); setChVolt(VAC_SIG, ch5); // 2, 6  (+, -)
    
      
    // int val = analogRead(A1);
    // Serial.println(val);
    delay(100);
  }
  */
}
