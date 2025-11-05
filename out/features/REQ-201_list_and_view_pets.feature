Feature: List and view pets
  As a user of the API
  I want list and view pets
  So that the service behaves as specified

  Background:
    Given the API base URL is "http://localhost:8000"

Scenario: REQ-201 hits GET /pets
    When I call GET /pets
    Then I receive a 200 response
    And the response matches the contract for operationId "listPets"
Scenario: REQ-201 hits GET /pets/{petId}
    When I call GET /pets/{petId}
    Then I receive a 200 response
    And the response matches the contract for operationId "getPet"
