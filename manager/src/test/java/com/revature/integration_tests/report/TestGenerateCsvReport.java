package com.revature.integration_tests.report;

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

import java.sql.SQLException;
import java.util.stream.Stream;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.*;
@Epic("Manager App Integration Tests")
@Feature("Expense Reporting")

@Tag("Integration")
public class TestGenerateCsvReport {
  static RequestSpecification requestSpec;
  static ResponseSpecification responseSpec;

  @BeforeAll
  public static void setUp() throws SQLException {
    RestAssured.baseURI="http://manager_app:5001/";

    requestSpec= new RequestSpecBuilder()
      .setContentType(ContentType.JSON)
      .setAccept(ContentType.JSON)
      .build();
    responseSpec= new ResponseSpecBuilder()
      .expectContentType(ContentType.JSON)
      .expectResponseTime(lessThan(5000L))
      .build();

    String url = "jdbc:sqlite:../employee/expense_manager.db";
  }

  @AfterAll
  public static void tearDown() throws SQLException {
    RestAssured.reset();
  }

  @BeforeEach
  void resetDatabase() {
    TestDatabaseUtil.resetAndSeed();
  }



    private enum ReportCheck {
        FULL_ENTRIES, PENDING_CHECKS
    }

    // update reportData() to include the check type
    static Stream<Arguments> reportData() {
        return Stream.of(
                Arguments.of("Positive", "manager1", "password123", 200, 6,
                        "/api/reports/expenses/csv",
                        "Expense ID,Employee,Amount,Description,Date,Status,Reviewer,Comment,Review Date",
                        ReportCheck.FULL_ENTRIES),
                Arguments.of("Pending", "manager1", "password123", 200, 3,
                        "/api/reports/expenses/pending/csv",
                        "Expense ID,Employee,Amount,Description,Date,Status,Reviewer,Comment,Review Date",
                        ReportCheck.PENDING_CHECKS)
        );
    }

    // helper that performs auth, GET, and shared assertions; returns CSV string
    private String fetchCsvAndDoBasicChecks(String username,
                                            String password,
                                            String endpoint,
                                            int expectedStatus,
                                            String expectedHeader,
                                            int expectedLines) {
        Response authResponse =
                given()
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

        String jwtCookie = authResponse.getCookie("jwt");

        String csv =
                given()
                        .spec(requestSpec)
                        .cookie("jwt", jwtCookie)
                        .when()
                        .get(endpoint)
                        .then()
                        .statusCode(expectedStatus)
                        .contentType("text/csv")
                        .extract()
                        .asString();

        assertTrue(csv.startsWith(expectedHeader));
        String[] lines = csv.split("\\R");
        assertEquals(expectedLines, lines.length);

        return csv;
    }

    // single parameterized test that delegates shared work to the helper and runs case-specific checks
    @ParameterizedTest(name = "Get Expense Report: {0}")
    @MethodSource("reportData")
    public void getExpenseReportCsvLoggedIn(String caseName,
                                            String username,
                                            String password,
                                            int expectedStatus,
                                            int expectedLines,
                                            String endpoint,
                                            String expectedHeader,
                                            ReportCheck check) {

        String csv = fetchCsvAndDoBasicChecks(username, password, endpoint, expectedStatus, expectedHeader, expectedLines);

        switch (check) {
            case FULL_ENTRIES -> {
                String[] expectedEntries = {
                        "1,employee1,50.0",
                        "2,employee1,200.0",
                        "3,employee1,30.0",
                        "4,employee2,75.0",
                        "5,employee2,450.0"
                };
                for (String entry : expectedEntries) {
                    assertTrue(csv.contains(entry), "CSV does not contain expected entry: " + entry);
                }
            }
            case PENDING_CHECKS -> {
                assertTrue(csv.contains(",pending,"), "Pending report should contain pending entries");
                assertFalse(csv.contains(",approved,"), "Pending report should not contain approved entries");
                assertFalse(csv.contains(",denied,"), "Pending report should not contain denied entries");
            }
        }
    }

  @DisplayName("Get Employee Expense Report, Logged In")
  @Test
  public void getEmployeeExpenseReportCsvLoggedIn() {
    String credentials = """
      {
          "username":"manager1",
          "password":"password123"
      }
      """;
    Response authResponse =
      given()
        .spec(requestSpec)
        .body(credentials)
      .when()
        .post("/api/auth/login")
      .then()
        .spec(responseSpec)
        .statusCode(200)
        .extract().response();
    String jwtCookie = authResponse.getCookie("jwt");

    int employeeId = 1;

    String csv =
      given()
        .spec(requestSpec)
        .cookie("jwt", jwtCookie)
      .when()
        .get("/api/reports/expenses/employee/" + employeeId + "/csv")
      .then()
        .statusCode(200)
        .contentType("text/csv")
        .extract()
        .asString();

    assertTrue(csv.startsWith(
      "Expense ID,Employee,Amount,Description,Date,Status,Reviewer,Comment,Review Date"
    ));

    String[] lines = csv.split("\\R");
    assertEquals(4, lines.length);

    assertTrue(csv.contains(",employee" + employeeId + ","));;
    assertFalse(csv.contains(",employee2,"));
  }

  @DisplayName("Get Date Range Expense Report, Logged In")
  @Test
  public void getDateRangeExpenseReportCsvLoggedIn() {
    String credentials = """
      {
          "username":"manager1",
          "password":"password123"
      }
      """;
    Response authResponse =
      given()
        .spec(requestSpec)
        .body(credentials)
      .when()
        .post("/api/auth/login")
      .then()
        .spec(responseSpec)
        .statusCode(200)
        .extract().response();
    String jwtCookie = authResponse.getCookie("jwt");

    String csv =
      given()
        .spec(requestSpec)
        .cookie("jwt", jwtCookie)
        .queryParam("startDate", "2025-01-05")
        .queryParam("endDate", "2025-01-06")
      .when()
        .get("/api/reports/expenses/daterange/csv")
      .then()
        .statusCode(200)
        .contentType("text/csv")
        .extract()
        .asString();

    assertTrue(csv.startsWith(
      "Expense ID,Employee,Amount,Description,Date,Status,Reviewer,Comment,Review Date"
    ));

    String[] lines = csv.split("\\R");
    assertEquals(4, lines.length);

    assertTrue(csv.contains(",2025-01-05,"));;
    assertTrue(csv.contains(",2025-01-06,"));;
    assertFalse(csv.contains(",2025-01-07,"));;
    assertFalse(csv.contains(",2025-01-09,"));
  }

  @DisplayName("Get Category Expense Report, Logged In")
  @Test
  public void getCategoryExpenseReportCsvLoggedIn() {
    String credentials = """
      {
          "username":"manager1",
          "password":"password123"
      }
      """;
    Response authResponse =
      given()
        .spec(requestSpec)
        .body(credentials)
      .when()
        .post("/api/auth/login")
      .then()
        .spec(responseSpec)
        .statusCode(200)
        .extract().response();
    String jwtCookie = authResponse.getCookie("jwt");

    String category = "Hotel";

    String csv =
      given()
        .spec(requestSpec)
        .cookie("jwt", jwtCookie)
      .when()
        .get("/api/reports/expenses/category/" + category + "/csv")
      .then()
        .statusCode(200)
        .contentType("text/csv")
        .extract()
        .asString();

    assertTrue(csv.startsWith(
      "Expense ID,Employee,Amount,Description,Date,Status,Reviewer,Comment,Review Date"
    ));

    String[] lines = csv.split("\\R");
    assertEquals(2, lines.length);

    assertTrue(csv.contains(",Hotel stay,"));
    assertTrue(csv.contains("1,"));;
    assertFalse(csv.contains(",2,"));
  }
}
