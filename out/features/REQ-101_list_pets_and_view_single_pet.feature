Feature: List pets and view single pet
  As a user of the API
  I want list pets and view single pet
  So that the service behaves as specified

  Background:
    Given the API base URL is "http://localhost:8000"

Scenario: REQ-101 hits GET /pets
    When I call GET /pets
    Then I receive a 200 response
    And the response matches the contract for operationId "listPets"
Scenario: REQ-101 hits GET /pets/{petId}
    When I call GET /pets/{petId}
    Then I receive a 200 response
    And the response matches the contract for operationId "getPet"
