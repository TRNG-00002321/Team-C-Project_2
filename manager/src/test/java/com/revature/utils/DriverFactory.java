package com.revature.utils;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;

import java.util.Map;

public class DriverFactory {

    public static WebDriver createDriver(String browser, boolean headless) {
        WebDriver driver;

        switch (browser.toLowerCase()) {

            case "chrome" -> {
                WebDriverManager.chromedriver().setup();
                ChromeOptions options = new ChromeOptions();
                options.addArguments(
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--window-size=1920,1080"
                );
                if (headless) {
                    options.addArguments("--headless=new");
                }

                options.setExperimentalOption(
                        "prefs",
                        Map.of("profile.password_manager_leak_detection", false)
                );
                driver = new ChromeDriver(options);
            }

            case "firefox" -> {
                WebDriverManager.firefoxdriver().setup();
                FirefoxOptions options = new FirefoxOptions();
                if (headless) {
                    options.addArguments("-headless");
                }
                driver = new FirefoxDriver(options);
            }

            case "edge" -> {
//                WebDriverManager.edgedriver().setup();
                System.setProperty("webdriver.edge.driver", "/usr/local/bin/msedgedriver");
                EdgeOptions options = new EdgeOptions();
                options.addArguments(
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--window-size=1920,1080"
                );
                if (headless) {
                    options.addArguments("--headless=new");
                }
                driver = new EdgeDriver(options);
            }

            default -> throw new IllegalArgumentException(
                    "Unsupported browser: " + browser
            );
        }

        driver.manage().window().maximize();
        return driver;
    }
}
