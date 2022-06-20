Feature: Test new product can be added in Django Admin
  Scenario: Django Admin can add new product
    Given I am on the Django Admin
    When I click on the "Products" link
    Then I am on the "product" page
    Then I will click on "product" add button
    Then I will add new information for Product Section