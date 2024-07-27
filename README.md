<!-- README.md -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IOT Projects</title>
<style>
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
    }
    h1, h2, h3 {
        color: #333;
    }
    .container {
        width: 80%;
        margin: 0 auto;
    }
    .project {
        background: #f4f4f4;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .project h3 {
        margin-top: 0;
    }
    .code {
        background: #333;
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
    }
    a {
        color: #1e90ff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
</head>
<body>
<div class="container">
    <h1>IOT Projects</h1>
    <p>Here you can find the projects needed for the basic learning of IOT. I also provide the Proteus files and Arduino codes.</p>

    <div class="project">
        <h3>Project 1: LED Blinking</h3>
        <p>This project demonstrates the basic LED blinking using Arduino.</p>
        <div class="code">
            <pre><code>
                // Arduino code for LED Blinking
                void setup() {
                    pinMode(LED_BUILTIN, OUTPUT);
                }

                void loop() {
                    digitalWrite(LED_BUILTIN, HIGH);
                    delay(1000);
                    digitalWrite(LED_BUILTIN, LOW);
                    delay(1000);
                }
            </code></pre>
        </div>
        <a href="path/to/proteus/file">Download Proteus File</a>
    </div>

    <div class="project">
        <h3>Project 2: Temperature Sensor</h3>
        <p>This project uses a temperature sensor to read and display temperature values.</p>
        <div class="code">
            <pre><code>
                // Arduino code for Temperature Sensor
                #include <DHT.h>
                #define DHTPIN 2
                #define DHTTYPE DHT11
                DHT dht(DHTPIN, DHTTYPE);

                void setup() {
                    Serial.begin(9600);
                    dht.begin();
                }

                void loop() {
                    float h = dht.readHumidity();
                    float t = dht.readTemperature();
                    Serial.print("Humidity: ");
                    Serial.print(h);
                    Serial.print(" %\t");
                    Serial.print("Temperature: ");
                    Serial.print(t);
                    Serial.println(" *C ");
                    delay(2000);
                }
            </code></pre>
        </div>
        <a href="path/to/proteus/file">Download Proteus File</a>
    </div>
</div>
</body>
</html>
