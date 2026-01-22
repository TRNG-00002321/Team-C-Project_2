package com.revature.integration_tests.auth;

import com.revature.utils.TestDatabaseUtil;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.stream.Stream;

import static io.restassured.RestAssured.given;

@Epic("Manager App Integration Tests")
@Feature("Manager Authentication")

@Tag("Integration")
public class TestAuthLogin {
    @BeforeAll
    static void setup(){
        RestAssured.baseURI = "http://manager_app";
        RestAssured.port = 5001;
    }

    @AfterAll
    static void tearDown(){
        RestAssured.reset();
    }

    @BeforeEach
    void resetDatabase() {
        System.out.println("Starting seed");
        TestDatabaseUtil.resetAndSeed();
        System.out.println("Finished seed");
    }

    static Stream<Arguments> loginTestData() {
        return Stream.of(
                Arguments.of("Valid login", "manager1", "password123", 200), //MI-221
                Arguments.of("Invalid login", "invalid", "invalid", 401)     //MI-222
        );
    }

    @ParameterizedTest(name = "API Manager Login Test: {0}")
    @MethodSource("loginTestData")
    void testAuthLogin(String scenario, String username, String password, int expectedStatus) {

        given()
                .contentType(ContentType.JSON)
                .body("""
                  {
                    "username": "%s",
                    "password": "%s"
                  }
                  """.formatted(username, password))
                .when()
                .post("/api/auth/login")
                .then()
                .statusCode(expectedStatus);
    }
}
