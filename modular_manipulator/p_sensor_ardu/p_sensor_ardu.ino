#include <Adafruit_ADS1X15.h>
#include <Wire.h>

float mv_per_step = 0.125; // 0.125 mV / step

Adafruit_ADS1115 ads1115;

void setup() 
{
  Serial.begin(115200);
  ads1115.begin();
  ads1115.setGain(GAIN_ONE);
}

void loop() 
{
  float adc0, adc1, adc2, V1, p1, V2, p2, V0, p0;

  adc0 = ads1115.readADC_SingleEnded(0);
  adc1 = ads1115.readADC_SingleEnded(1);
  adc2 = ads1115.readADC_SingleEnded(2);
  
  V0 = adc0 * mv_per_step / 1000.0;
  V1 = adc1 * mv_per_step / 1000.0;
  V2 = adc2 * mv_per_step / 1000.0;
  p0 = 20.0 * (V0 - 2.5); // kPa
  p1 = 20.0 * (V1 - 2.5); // kPa
  p2 = 20.0 * (V2 - 2.5); // kPa

  Serial.print(p0); Serial.print(","); Serial.print(p1); Serial.print(","); Serial.println(p2);
  delay(25);
}
