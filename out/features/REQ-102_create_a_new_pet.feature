Feature: Create a new pet
  As a user of the API
  I want create a new pet
  So that the service behaves as specified

  Background:
    Given the API base URL is "http://localhost:8000"

Scenario: REQ-102 hits POST /pets
    When I call POST /pets
    Then I receive a 200 response
    And the response matches the contract for operationId "createPet"
