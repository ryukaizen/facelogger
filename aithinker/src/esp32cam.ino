#include "WifiCam.hpp"
#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "images.h"
#include <WebServer.h>

#define I2C_SDA 15
#define I2C_SCL 14
TwoWire I2Cbus = TwoWire(0);

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &I2Cbus, OLED_RESET);

int demoMode = 0;
int counter = 0;

static const char* WIFI_SSID = "wifi_name";
static const char* WIFI_PASS = "wifi_password";

esp32cam::Resolution initialResolution;
WebServer server(80);

void write(String text, int fontSize) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(fontSize);
  display.setTextColor(SSD1306_WHITE);
  display.print(text);
  display.display();
}

void handleRoot() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("Hello, world!");
  display.display();
  server.send(200, "text/plain", "Hello, world!");
}

void handleUpdate() {
  if (server.hasArg("plain") == false) {
    server.send(400, "text/plain", "Body not received");
    return;
  }
  String message = server.arg("plain");
  display.clearDisplay();
  display.setTextSize(2);
  // display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print(message);
  display.display();
  server.send(200, "text/plain", message);
}

void setup() {
  Serial.begin(115200);
  Serial.println("[==================== Face Logger Initialized Successfully ====================]\n");
  Serial.println();

  I2Cbus.begin(I2C_SDA, I2C_SCL, 100000);

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.printf("SSD1306 OLED display failed to initialize.\nCheck that display SDA is connected to pin %d and SCL connected to pin %d\n", I2C_SDA, I2C_SCL);
    while (true);
  }

  write("ESP32\nStarted!", 2);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  Serial.println("\n[======================== Trying to connect to the WIFI ========================]");

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi failure");
    write("Wifi\nFailure!", 2);
    delay(5000);
    ESP.restart();
  }
  Serial.println("WiFi connected");
  write("Wifi\nConnected!", 2);
  delay(1000);

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("Camera initialize failure");
      write("Camera\ninitialize\nfailure", 2);
      delay(5000);
      ESP.restart();
    }
    Serial.println("Camera initialize success");
    write("Camera\ninitialize\nsuccess", 2);
    delay(1000);
  }

  Serial.println("Camera starting");
  write("Camera\nstarting...", 2);
  delay(1000);
  Serial.print("http://");
  Serial.println(WiFi.localIP());
  write("Connected to: \n" + (WiFi.localIP()).toString(), 2);

  addRequestHandlers();

  // Setup server routes
  server.on("/", handleRoot);
  server.on("/update", HTTP_POST, handleUpdate);

  server.begin();
}

void loop() {
  server.handleClient();
}