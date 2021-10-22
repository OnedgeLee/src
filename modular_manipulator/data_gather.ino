#include <Wire.h>
#include <JY901.h>
#include <SPI.h>
#include <Adafruit_ADS1X15.h>

/* Define Pin & Flag */
// uint8_t ssPin    = D8;
// uint8_t resetPin = D3;
uint8_t ssPin    = 10;
uint8_t resetPin = 9;
uint8_t ch0 = 0;
uint8_t ch1 = 1;
uint8_t ch2 = 2;
uint8_t ch3 = 3;
uint8_t ch6 = 6;
uint8_t ch7 = 7;
bool DONE = false;
/* Only for Arduino to use SPI */

/* End */
uint16_t BIT_CONV = 13107;
bool IMU = true;
bool DAC = true;
bool aDC = false; 

/* ADS1115 Gain Tune 
  GAIN_TWOTHIRDS (for an input range of +/- 6.144V)
  GAIN_ONE (for an input range of +/-4.096V)
  GAIN_TWO (for an input range of +/-2.048V)
  GAIN_FOUR (for an input range of +/-1.024V)
  GAIN_EIGHT (for an input range of +/-0.512V)
  GAIN_SIXTEEN (for an input range of +/-0.256V)
*/

/* Solenoid Valve Operates when input voltage is higher than 3 V */

void softreset()
{
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
  digitalWrite(ssPin, LOW);
  buf[0] = (0x06<<4) + 0x00;
  buf[1] = 0x00;
  buf[2] = 0x00;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH);
  SPI.endTransaction();
}

void angle_print(float _r, float _p, float _y)
{
  Serial.print(_r); Serial.print(","); Serial.print(_p); Serial.print(","); Serial.println(_y);
}

void setup() 
{
  Serial.begin(115200);
  if (IMU==true) JY901.StartIIC();
  if (DAC==true)
  {
    SPI.begin();
    pinMode(resetPin, OUTPUT); pinMode(ssPin, OUTPUT);
    // digitalWrite(ssPin, LOW); 
    delay(500);
    digitalWrite(ssPin, HIGH); digitalWrite(resetPin, LOW); delay(5);
    digitalWrite(resetPin, HIGH);
    softreset();
    delay(500);
  }
  if (aDC == true) 
  {
    Adafruit_ADS1115 ads1115;
    ads1115.setGain(GAIN_SIXTEEN);
    ads1115.begin();
  }
}

void setAllChVolt(uint16_t SIG)
{
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
  digitalWrite(ssPin, LOW);
  buf[0] = (0x0B << 4) + 0x00;
  buf[1] = SIG / 256;
  buf[2] = SIG % 256;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH);
  SPI.endTransaction();
}

void setChVolt(uint16_t SIG, uint8_t _addr)
{
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
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
  if (DONE==false)
  {
    for (int i=0; i<10; i++)
    {
      JY901.GetAngle();
      float r = (float)JY901.stcAngle.Angle[0]/32768*180;
      float p = (float)JY901.stcAngle.Angle[1]/32768*180;
      float y = (float)JY901.stcAngle.Angle[2]/32768*180;
      angle_print(r, p, y);
      delay(32);
    }
    float STEP_V = 0.005;
    float ST_V   = 3.3;
    float VOLT   = 0.0;
  
    for (int i = 0; i < 341; i++)
    {
      VOLT = ST_V + (float)i*STEP_V;
      uint16_t SIG = (uint16_t) (VOLT * BIT_CONV);
      setChVolt(SIG, ch0); setChVolt(SIG, ch2); setChVolt(SIG, ch6);
      delay(5000);
      float VOLT0 = VOLT; float VOLT1 = 0.0; float VOLT2 = VOLT; float VOLT3 = 0.0; float VOLT6 = VOLT; float VOLT7 = 0.0;
      JY901.GetAngle();
      float r = (float)JY901.stcAngle.Angle[0]/32768*180;
      float p = (float)JY901.stcAngle.Angle[1]/32768*180;
      float y = (float)JY901.stcAngle.Angle[2]/32768*180;
      Serial.print(VOLT0); Serial.print(","); Serial.print(VOLT1); Serial.print(","); Serial.print(VOLT2); Serial.print(","); Serial.print(VOLT3); Serial.print(","); Serial.print(VOLT6); Serial.print(","); Serial.print(VOLT7); Serial.print(","); angle_print(r, p, y);
      delay(1000);
    }
    DONE = true;
  }
  delay(500);
}
