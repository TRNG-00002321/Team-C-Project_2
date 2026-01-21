package com.revature.integration_tests.info;

import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import org.junit.jupiter.api.*;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;
@Epic("Manager App Integration Tests")
@Feature("Health Check")

@Tag("Integration")
public class TestGetHealthCheck {

    private static String managerJwtCookie;

    @BeforeAll
    static void setupBaseUri(){
        RestAssured.baseURI = "http://manager_app";
        RestAssured.port = 5001;
    }

    @AfterAll
    static void cleanup(){
        RestAssured.reset();
    }

    @Test
    @DisplayName("Get HEALTH Info")
    void testHealthCheck_Returns200(){
        given()
                .log().uri()
                .when()
                .get("/health")
                .then()
                .log().status()
                .statusCode(200)
                .body("service", not(emptyString()))
                .body("version", not(emptyString()))
                .body("status", not(emptyString()));
    }
}
