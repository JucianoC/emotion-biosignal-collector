#include <Wire.h>
#include <mlx90615.h>


MLX90615 mlx = MLX90615();
const int GSR=A1;
int gsrSignal = 0;
int bvpSignal = 0;
float objectTemperature = 0.0;


void setup()
{
  Serial.begin(9600);
  mlx.begin();
  mlx.get_id();
  Serial.println("Starting collector...");
}


void loop()
{
  // at this point the PPG should be readed
  gsrSignal = analogRead(GSR);
  objectTemperature = mlx.get_object_temp();
  Serial.print(bvpSignal);
  Serial.print(",");
  Serial.print(gsrSignal);
  Serial.print(",");
  Serial.println(objectTemperature);
  delay(20);
}
