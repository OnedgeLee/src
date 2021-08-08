#include <Wire.h>
#include <JY901.h>
#include <AD5676.h>

/* Define SPI Pin */
uint8_t ssPin   = 8;
uint8_t mosiPin = 13;
uint8_t misoPin = 12;
uint8_t sckPin  = 14;
// Logical DAC (LDAC) tied to GND, Permanently Low

/* Define Control Input Voltage Variable for Sol. Valve */
float fpG_ChV, rpG_ChV, lpG_ChV; // for positive Gauge Pressure Control
float fnG_ChV, rnG_ChV, lnG_ChV; // for negative Gauge Pressure Control

/* Define Solenoid Valve Channel */
uint8_t fpG_Ch = 5; uint8_t rpG_Ch = 3; uint8_t lpG_Ch = 6; // front, right, left +
uint8_t fnG_Ch = 1; uint8_t rnG_Ch = 4; uint8_t lnG_Ch = 2; // front, right, left -

/* Initialize dac */
// AD5676 dac = AD5676(ssPin); // Initialize DAC using AD5676 Library

/* Global Variable */
bool angle_init = false;

void softreset()
{
  /* Software Reset for Innitializing DAC */
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
  digitalWrite(ssPin, LOW);
  buf[0] = (0x06<<4) + 0x00;
  buf[1] = 0x00;
  buf[2] = 0x00;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH); // End Transmission
  SPI.endTransaction();  
}

void setChannelVolt(uint16_t _out, uint8_t _addr)
{
  /* Not in Use */
  uint8_t buf[3];
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));
  digitalWrite(ssPin, LOW);
  buf[0] = (0x03 << 4) + _addr;
  buf[1] = _out / 256;
  buf[2] = _out % 256;
  SPI.transfer(buf, 3);
  digitalWrite(ssPin, HIGH);
  SPI.endTransaction();
}

void angle_print(float _r, float _p, float _y)
{
  Serial.print(_r); Serial.print(" "); Serial.print(_p); Serial.print(" "); Serial.println(_y);
}

void setup()
{
  Serial.begin(115200);
  JY901.StartIIC(); // Start IIC for IMU
  // softreset(); // Software Reset for DAC
  // Internal Reference Enable
}

void loop()
{
  /* Read Angle From IMU R, P, Y */
  JY901.GetAngle();
  float R, P, Y;
  R = (float)JY901.stcAngle.Angle[0]/32768*180;
  P = (float)JY901.stcAngle.Angle[1]/32768*180;
  Y = (float)JY901.stcAngle.Angle[2]/32768*180;
  angle_print(R, P, Y);
  if (Serial.available() > 0)
  {
    char modeSel = Serial.read();
    switch (modeSel)
    {
      case '1' :
        Serial.println("Balancing Module Using IMU");
        float r0, p0, y0;
        while (true)
        {
          /* Angle Initialize */
          if (angle_init != true)
          {
            for (int i=0; i < 10; i++)
            {
              delay(5);
              JY901.GetAngle();
              float r = (float)JY901.stcAngle.Angle[0]/32768*180;
              float p = (float)JY901.stcAngle.Angle[1]/32768*180;
              float y = (float)JY901.stcAngle.Angle[2]/32768*180;
              r0 = r0 + r; p0 = p0 + p; y0 = y0 + y;
            }
            angle_init = true;
            r0 = r0/10.0; p0 = p0/10.0; y0 = y0/10.0;
            Serial.println("Initial Angle"); angle_print(r0, p0, y0);
            delay(5);
          }

          // Do Balancing
          JY901.GetAngle();
          float r = (float)JY901.stcAngle.Angle[0]/32768*180;
          float p = (float)JY901.stcAngle.Angle[1]/32768*180;
          float y = (float)JY901.stcAngle.Angle[2]/32768*180;

          float delta_r = r - r0; float delta_p = p - p0; float delta_y = y - y0;
          angle_print(delta_r, delta_p, delta_y);

          // Case 1 while is Terminated when key 'x' is pressed
          if (Serial.available() > 0)
          {
            char inChar = Serial.read();
            if (inChar == 'x')
            {
              angle_init = false;
              break;
            }
          }
          delay(5);
        }
        break;
      case '2' :
        Serial.print("case 2"); Serial.print(" "); Serial.println(modeSel);
        break;
      case '\n' :
        break;
      case '\r' :
        break;
      default :
        Serial.println(modeSel);
        break;
    }
  }
  
  /* DAC Control F51 R34 L62 */
  /*
  // Front Sol. Valve
  dac.SetChVolt(fpG_Ch, fpG_ChV);
  dac.SetChVolt(fnG_Ch, fnG_ChV);

  // Right Sol. Valve
  dac.SetChVolt(rpG_Ch, rpG_ChV);
  dac.SetChVolt(rnG_Ch, rnG_ChV);

  // Left Sol. Valve
  dac.SetChVolt(lpG_Ch, lpG_ChV);
  dac.SetChVolt(lnG_Ch, lnG_ChV);
  */
  delay(5);
}
