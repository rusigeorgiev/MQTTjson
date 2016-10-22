
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

 
// Connect to the WiFi
const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";

const boolean hasRelay = false;
 
WiFiClient espClient;
PubSubClient client(espClient);
 
const byte ledPin = 5; // Pin with LED on Adafruit Huzzah
 
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  StaticJsonBuffer<200> jsonBuffer;
  char json[length];
  for (int ii=0; ii<length; ii++){
    json[ii] = payload[ii];
  }
  
  JsonObject& root = jsonBuffer.parseObject(json);

  // Test if parsing succeeds.
  if (!root.success()) {
    Serial.println("parseObject() failed");
    return;
  }

  
  const char* relayState = root["relayState"];
  String state = relayState;

  // get command for a relay:
  if(hasRelay == true){
    Serial.print("Relay state = ");
    Serial.print(state);
    Serial.print(" ");

    Serial.print("test: ");
    Serial.println(state.equals("On"));

    if (state.equals("On")){
      Serial.println("ledPin -  HIGH");
      digitalWrite(ledPin, HIGH);
    }

    if (state.equals("Off")){
      Serial.println("ledPin -  LOW");
      digitalWrite(ledPin, LOW);
    }
 
    Serial.println();

  }

  if(hasRelay == false){
    // get command for a PWM:
    Serial.print("PWM% = ");
    int pwmState = root["pwmState"];
    int PWM = pwmState;
    analogWrite(ledPin, PWM);
    Serial.print(PWM);
    Serial.print(" ");
  }
}

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    for(int i = 0; i<500; i++){
      delay(1);
    }
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
 
 
void reconnect() {
 // Loop until we're reconnected
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 // Attempt to connect
 if (client.connect("ESP8266Client")) {
  Serial.println("connected");
  // ... and subscribe to topic
  client.subscribe("hello/world");
 } else {
  Serial.print("failed, rc=");
  Serial.print(client.state());
  Serial.println(" try again in 5 seconds");
  // Wait 5 seconds before retrying
  delay(5000);
  }
 }
}
 
void setup()
{
 Serial.begin(9600);
 
 client.setServer(mqtt_server, 1883);
 client.setCallback(callback);
 
 pinMode(ledPin, OUTPUT);

 setup_wifi();
}
 
void loop()
{
 if (!client.connected()) {
  reconnect();
 }
 client.loop();
}
