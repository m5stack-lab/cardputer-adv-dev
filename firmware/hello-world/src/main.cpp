#include <M5Cardputer.h>

void setup() {
  auto cfg = M5.config();
  M5Cardputer.begin(cfg);

  M5Cardputer.Display.setRotation(1);
  M5Cardputer.Display.setTextSize(2);
  M5Cardputer.Display.fillScreen(BLACK);
  M5Cardputer.Display.setCursor(0, 0);
  M5Cardputer.Display.println("Cardputer ADV");
  M5Cardputer.Display.println("hello, world");

  Serial.begin(115200);
  Serial.println("Cardputer ADV booted, USB-CDC serial up.");
}

void loop() {
  M5Cardputer.update();

  if (M5Cardputer.Keyboard.isChange() && M5Cardputer.Keyboard.isPressed()) {
    auto status = M5Cardputer.Keyboard.keysState();
    for (auto c : status.word) {
      Serial.print(c);
      M5Cardputer.Display.print(c);
    }
  }

  delay(10);
}
