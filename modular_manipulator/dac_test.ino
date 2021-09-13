#include <Wire.h>
#include <JY901.h>
#include <SPI.h>

/* Define SPI Pin */
uint8_t ssPin   = D8; // Slave Select
uint8_t mosiPin = D7; // Master Out Slave In (WEMOS) -> SDI (DAC)
uint8_t misoPin = D6; // Master In Slave Out (WEMOS) -> SDO (DAC)
uint8_t sckPin  = D5; // Serial Clock
uint8_t rstPin  = D3; // Reset Pin

void pulseSS()
{
  digitalWrite(ssPin, HIGH);
  delayMicroseconds(25);
  digitalWrite(ssPin, LOW);
}

void softreset()
{
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
  digitalWrite(ssPin, LOW);
  // pulseSS();
  buf[0] = (0x06<<4) + 0x00;
  buf[1] = 0x00;
  buf[2] = 0x00;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH);
  // pulseSS();
  SPI.endTransaction();
}

void setup()
{
  Serial.begin(115200);
  SPI.begin();
  pinMode(ssPin, OUTPUT);
  pinMode(rstPin, OUTPUT);
  digitalWrite(ssPin, LOW);

  delay(500);
  digitalWrite(ssPin, HIGH);
  digitalWrite(rstPin, LOW);
  delay(5);
  digitalWrite(rstPin, HIGH);
  softreset();
}

void loop()
{
  for (int i=0; i<30000; i++)
  {
    uint8_t buf[3];
    SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
    buf[0] = (0x03 << 4) + 1;
    buf[1] = i/256;
    buf[2] = i%256;
    Serial.print(buf[0]); Serial.print(" "); Serial.print(buf[1]); Serial.print(" "); Serial.println(buf[2]);
    digitalWrite(ssPin, LOW);
    delayMicroseconds(20);
    SPI.transfer(buf, 3);
    digitalWrite(ssPin, HIGH);
    SPI.endTransaction();
    delay(10);
  }
  delay(500);
}
