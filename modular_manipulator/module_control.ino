#include <Wire.h>
#include <JY901.h>
#include <SPI.h>
#include <Adafruit_ADS1X15.h>

/* Define Pin & Flag */
// uint8_t ssPin    = D8;
// uint8_t resetPin = D3;
uint8_t ssPin    = 10;
uint8_t resetPin = 9;
uint8_t ch1 = 0;
uint8_t ch2 = 6;
uint8_t ch3 = 7;
/* Only for Arduino to use SPI */

/* End */
uint16_t BIT_CONV = 13107;
bool IMU = false;
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

void setup() 
{
  Serial.begin(115200);
  if (IMU==true) JY901.StartIIC();
  if (DAC==true)
  {
    SPI.begin();
    Serial.println("DAC GO");
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
  /*
  if (aDC==true)
  {
    int16_t adc0, adc1, adc2;
    adc0 = ads1115.readADC_SingleEnded(0);
    adc1 = ads1115.readADC_SingleEnded(1);
    adc2 = ads1115.readADC_SingleEnded(2);
  }
  */
  if (Serial.available()>0)
  {
    int MODE = Serial.parseInt();
    switch (MODE)
    {
      case 1 :
        Serial.println("MODE 1, Valve is actuated with Same Voltage");
        while (true)
        {
          if (Serial.available() > 0)
          {
            float VOLT = Serial.parseFloat(SKIP_ALL, "\n");
            if (VOLT > 5.0) 
            {
              Serial.println("Terminated");
              uint16_t SIG = (uint16_t) (0);
              setAllChVolt(SIG);
              break;
            }
            else if (0.0 < VOLT && VOLT < 5.1)
            {
              // Actuate Solenoid Valve
              uint16_t SIG = (uint16_t) (VOLT * BIT_CONV);
              setAllChVolt(SIG);
              Serial.print("Voltage: "); Serial.print(VOLT); Serial.print(" "); Serial.print("SIG: "); Serial.println(SIG);
            }
            delay(500);          
          }
        }
        break;
      case 2 :
        Serial.println("MODE 2, Single Valve Control");
        int counter = 0;
        while (true)
        {
          if (Serial.available() > 0)
          {
            Serial.read();
            while (Serial.available() == 0)
            {
              
            }
            float VOLT1 = Serial.parseFloat(SKIP_WHITESPACE, "\n");
            float VOLT2 = Serial.parseFloat(SKIP_WHITESPACE, "\n");
            float VOLT3 = Serial.parseFloat(SKIP_WHITESPACE, "\n");
            if (VOLT1 > 5.0 | VOLT2 > 5.0 | VOLT3 > 5.0) 
            {
              Serial.println("Terminated");
              uint16_t SIG = (uint16_t) (0);
              setAllChVolt(SIG);
              break;
            }
            if (0.0 < VOLT1 && VOLT1 < 5.1)
            {
              uint16_t SIG1 = (uint16_t) (VOLT1 * BIT_CONV);
              setChVolt(SIG1, ch1);
            }
            else
            {
              uint16_t SIG1 = (uint16_t) (0);
              setChVolt(SIG1, ch1);
            }
            if (0.0 < VOLT2 && VOLT2 < 5.1)
            {
              uint16_t SIG2 = (uint16_t) (VOLT2 * BIT_CONV);
              setChVolt(SIG2, ch2);
            }
            else
            {
              uint16_t SIG2 = (uint16_t) (0);
              setChVolt(SIG2, ch2);
            }
            if (0.0 < VOLT3 && VOLT3 < 5.1)
            {
              uint16_t SIG3 = (uint16_t) (VOLT3 * BIT_CONV);
              setChVolt(SIG3, ch3);
            }
            else
            {
              uint16_t SIG3 = (uint16_t) (0);
              setChVolt(SIG3, ch3);
            }
            Serial.print("V1: "); Serial.print(VOLT1); Serial.print(" "); Serial.print("V2: "); Serial.print(VOLT2); Serial.print(" "); Serial.print("V3: "); Serial.println(VOLT3);            
            delay(500);
          }
        }
        break;
      case 3 :
        // do something when incoming MODE is equal to 3
        break;
    }
  }
  delay(500);
}
