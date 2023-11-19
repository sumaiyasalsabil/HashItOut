#include <Wire.h>
#include <WiFi.h>
#include <Adafruit_DRV2605.h>
#include <HTTPClient.h>
#include <iostream>
#include <chrono>
#include <thread>


const char *ssid = "SOAIBA";
const char *password = "11111111";
const char *serverUrl = "http://192.168.193.46:8000/feed";
int vibrate = 0;


// Define the DRV2605 instance
Adafruit_DRV2605 drv;

void setup() {
  Serial.begin(9600); 

  // Connect to open Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting to WiFi...");
  }

  Serial.println("Conected to WiFi");
  Serial.print(ssid);
  Serial.print("IP Address ");
  Serial.println(WiFi.localIP());

    Serial.println("Connected to WiFi");

    // Send HTTP request to Django endpoint to trigger action
    HTTPClient http;
    http.begin(serverUrl);

    int httpResponseCode = http.GET();
    if (httpResponseCode == 200) {
        String payload = http.getString();
        if (payload == "{\"status\": true}") {
          vibrate = 1;
          }
        // Process the response if needed
    } else {
        Serial.print("HTTP Request failed with error code: ");
        Serial.println(httpResponseCode);
    }

    http.end();

  // Initialize the DRV2605
  if (!drv.begin()) {
    Serial.println("Couldn't find DRV2605, check connections!");
    while (1);
  }
}

void loop() {
// Send HTTP request to Django endpoint to trigger action
  HTTPClient http;
  http.begin(serverUrl);
  vibrate = 0;
  int httpResponseCode = http.GET();
  if (httpResponseCode == 200) {
    String payload = http.getString();
    if (payload == "{\"status\": true}") {
      vibrate = 1;
    }
    Serial.println(payload);
    // Process the response if needed
  } else {
    Serial.print("HTTP Request failed with error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();

  // Vibrate the motor if vibrate flag is set
  if (vibrate == 1) {
    drv.setWaveform(0, 100);  // Change the second parameter for different vibration effects
    drv.go();
    delay(1000);  // Vibrate for 1 second
    drv.stop();
  }
  delay(500); // Wait for 0.5 second before the next HTTP request
}
