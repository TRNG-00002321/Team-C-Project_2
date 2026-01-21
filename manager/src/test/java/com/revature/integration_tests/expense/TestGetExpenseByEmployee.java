package com.revature.integration_tests.expense;

import com.revature.utils.TestDatabaseUtil;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.restassured.RestAssured;
import org.junit.jupiter.api.*;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;
@Epic("Manager App Integration Tests")
@Feature("Expense Management")

@Tag("Integration")
public class TestGetExpenseByEmployee {
    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "http://manager_app";
        RestAssured.port = 5001;
    }

    @AfterAll
    public static void tearDown(){
        RestAssured.reset();
    }

    @BeforeEach
    void resetDatabase() {
        TestDatabaseUtil.resetAndSeed();
    }

    private String loginAndGetJwtCookie() {
        return given()
                .contentType("application/json")
                .accept("application/json")
                .body("""
            {
              "username": "manager1",
              "password": "password123"
            }
        """)
                .when()
                .post("/api/auth/login")
                .then()
                .statusCode(200)
                .extract()
                .cookie("jwt");
    }

    // MI-213
    @Test
    void getExpensesByEmployee_success() {
        int employeeId = 1;
        String jwt = loginAndGetJwtCookie();

        given()
                .cookie("jwt", jwt)
                .accept("application/json")
                .pathParam("employeeId", employeeId)
                .when()
                .get("/api/expenses/employee/{employeeId}")
                .then()
                .statusCode(200)
                .body("success", equalTo(true))
                .body("employeeId", equalTo(employeeId))
                .body("data", notNullValue());
    }

    // MI-214
    @Test
    void getExpensesByEmployee_failure() {
        int invalidEmployeeId = 1000;
        String jwt = loginAndGetJwtCookie();

        given()
                .cookie("jwt", jwt)
                .accept("application/json")
                .pathParam("employeeId", invalidEmployeeId)
                .when()
                .get("/api/expenses/employee/{employeeId}")
                .then()
                .statusCode(200)
                .body("count", equalTo(0));
    }
}
