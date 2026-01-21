package com.revature.end_to_end_tests.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class LoginPage extends BasePage{

    @FindBy(id="username")
    private WebElement usernameField;
    @FindBy(id="password")
    private WebElement passwordField;
    @FindBy(css="button[type='submit']")
    private WebElement loginButton;

    public LoginPage(WebDriver driver){
        super(driver);
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(DEFAULT_TIMEOUT));

        //Testing
        System.out.println("Login page init with driver" + driver.getCurrentUrl());
        PageFactory.initElements(driver, this);
    }

    public void enterUsername(String username) {
        wait.until(ExpectedConditions.visibilityOf(usernameField));
        usernameField.clear();
        usernameField.sendKeys(username);
    }

    public void enterPassword(String password) {
        wait.until(ExpectedConditions.visibilityOf(passwordField));
        passwordField.clear();
        passwordField.sendKeys(password);
    }

    public DashboardPage clickLogin() {
        System.out.println("Clicking login button on page" + driver.getCurrentUrl());
        wait.until(ExpectedConditions.elementToBeClickable(loginButton));
        System.out.println("Login button is clickable" + driver.getCurrentUrl());
        System.out.println(driver.findElement(By.cssSelector("button[type='submit']")).getText());
        System.out.println(loginButton.getText());
        loginButton.click();
        return new DashboardPage(this.driver);
    }

    public LoginPage clickLoginExpectingError(){
        wait.until(ExpectedConditions.elementToBeClickable(loginButton));
        loginButton.click();
        return this;
    }

    public DashboardPage login(String username, String password){
        enterUsername(username);
        enterPassword(password);
        return clickLogin();
    }
}
