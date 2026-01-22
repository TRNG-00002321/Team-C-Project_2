package com.revature.integration_tests.expense;

import com.revature.utils.TestDatabaseUtil;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.builder.ResponseSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.lessThan;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.stream.Stream;
@Epic("Manager App Integration Tests")
@Feature("Expense Management")

@Tag("Integration")
public class TestPostApproveExpense {

    static RequestSpecification requestSpec;
    static ResponseSpecification responseSpec;
    private static Connection connection;


    @BeforeAll
    public static void setUp() throws SQLException {
        RestAssured.baseURI="http://manager_app:5001";
        requestSpec= new RequestSpecBuilder()
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .build();
        responseSpec= new ResponseSpecBuilder()
                .expectContentType(ContentType.JSON)
                .expectResponseTime(lessThan(5000L))
                .build();
    }


    @AfterAll
    public static void tearDown() throws SQLException {
        RestAssured.reset();
    }

    @BeforeEach
    void resetDatabase() {
        TestDatabaseUtil.resetAndSeed();
    }

    @DisplayName("Test attempted approval without authentication first")
    @Test
    public void testApproveNoAuth(){
        Response response = given()
                .spec(requestSpec)
        .when()
                .post("/api/expenses/1234567/approve")
        .then()
                .statusCode(401)
                .extract().response();
        assertEquals("Authentication required", response.jsonPath().getString("title"));

        //String responseMessage = response.asString();
        //System.out.println(responseMessage);
    }


    static Stream<Arguments> postCaseData() {
        return Stream.of(
                Arguments.of("Positive", 1, "manager1", "password123", 200, "Expense approved successfully", "message"),
                Arguments.of("Approved", 2, "manager1", "password123", 200, "Expense approved successfully", "message"),
                Arguments.of("Negative", 1234567, "manager1", "password123", 404, "Expense not found or could not be approved", "title")
        );
    }
//    //Expense must be seeded in the database with the corresponding id for test to pass
    @ParameterizedTest(name = "Test approve expense: {0}")
    @MethodSource("postCaseData")
    public void testApprovalPositive(String scenario, int expenseId, String username, String password, int expectedStatus, String expectedMessage, String pathKey){
//        int expenseId = 1;
        //log in with valid credentials
        Response response1 = given()
                .spec(requestSpec)
                .body("""
                  {
                    "username": "%s",
                    "password": "%s"
                  }
                  """.formatted(username, password))
                .when()
                .post("/api/auth/login")
                .then()
                .spec(responseSpec)
                .statusCode(200)
                .extract().response();
        String jwtCookie = response1.getCookie("jwt");

        //approve an expense that is pending (already seeded in the database)
        Response response2 = given()
                .spec(requestSpec)
                .cookie("jwt", jwtCookie)
        .when()
                .post("/api/expenses/"+ expenseId +"/approve")
        .then()
                .statusCode(expectedStatus)
                .extract().response();

        String message = response2.jsonPath().getString(pathKey);
        assertEquals(expectedMessage, message);
    }
}
