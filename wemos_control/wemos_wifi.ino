#include <ESP8266WiFi.h>

//SSID and Password of your Wi-Fi router access point

const char* ssid="smf";
const char* password="smf314312";
const char* host ="192.168.0.7";//IP Address of pc or laptop
const uint16_t port = 8080;


int sensorVal;
int sensorPin =4;
int numhits=0;
bool triggerOn=false;
IPAddress server(192, 168, 0, 7);
WiFiClient client;//Use for TCP connections

void setup(){
  pinMode(sensorPin,INPUT);
  Serial.begin(115200);
 

WiFi.begin(ssid,password);

Serial.print("Connecting");
while (WiFi.status() !=WL_CONNECTED){
  delay(500);
  Serial.print(".");
 
}


//If connection successful show IP Address in serial monitor on Arduino
Serial.println("");
Serial.print("Connected, IP Address");
Serial.println(WiFi.localIP());

  //Connect to our host
  if(!client.connect(server,port)){
 
    Serial.println("connection failed");
    Serial.println("wait 5 sec...");
    delay(5000);
    return;
  }

}


void loop(){
  client.println("hello");
  delay(50);
  while (client.available()) 
  {
    char ch = static_cast<char>(client.read());
    Serial.print(ch);
  }
  /*sensorVal=digitalRead(sensorPin);

  if((sensorVal==HIGH) &&(triggerOn==false))
  {
    triggerOn=true;
    numhits++;
    Serial.println(numhits);//Write to the serial port

    if(!client.connect(host,port))
    {
      Serial.println("Connection failed cannot write data");
    }
    else{
      client.println(numhits);//Write this data to the server
    }   
  }
  else if((sensorVal==LOW) &&(triggerOn==false))
  {
    triggerOn=false;
  }
  */

}
