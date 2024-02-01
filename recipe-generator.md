# Recipe Generator (Agile Development)

## Repo: [github.com/ucsd-cse110-fa23/cse-110-project-team-40](https://github.com/ucsd-cse110-fa23/cse-110-project-team-40)

## General

This was a class project to simulate the experience of working in a startup environment following Agile development principles. Our goal was to create a Recipe Generator app based on a prompt given by the instructor and staff.

We needed to ask multiple clarifying questions to understand what the customer wanted. We used pull requests, issue tracking, progress tracking with a big board, tasks with specific hour values, code review sessions, pair programming sessions, and multiple stand-up meetings per week.

The goal with this project was to learn how to work in a team with other developers, including creating ideas, solutions, and especially compromise.

![Pull requests](images/cse110%20pull%20requests.png)

![Burn up chart](images/cse110%20burn%20up%20chart.png)

![Issue](images/cse110%20issue.png)

## Object-Oriented Design

For this project, we also followed object-oriented design principles, like Model-View-Presenter and factory pattern.

Example:

[Account Creation Page](https://github.com/ucsd-cse110-fa23/cse-110-project-team-40/blob/main/app/src/main/java/PantryPal/AccountCreatePage.java)

[Account Model](https://github.com/ucsd-cse110-fa23/cse-110-project-team-40/blob/main/app/src/main/java/PantryPal/AccountModel.java)

[Account API](https://github.com/ucsd-cse110-fa23/cse-110-project-team-40/blob/main/app/src/main/java/server/AccountAPI.java)

## Testing

Another major component of this project was creating tests to verify that each component of the code worked independently, in addition to using continuous integration to verify that no development was causing regressions.

Because we were using the OpenAI API, we created mock classes for ChatGPT that would allow us to test without burning resources by using the API.

```java
/**
 * The MockChatGPTBot class implements the RecipeCreator interface and provides a mock
 * implementation for testing purposes.
 */
class MockChatGPTBot implements RecipeCreator {
  // Instance variables
  private String mockOutput = "";

  /**
   * A mock implementation of the makeRecipe method.
   *
   * @param meal The type of meal for the mock recipe.
   * @param ingredients The list of ingredients for the mock recipe.
   * @return A string containing a mock recipe output.
   */
  public String makeRecipe(String meal, String ingredients) {
    return this.mockOutput;
  }

  /**
   * Sets the mockMeal and mockIngredients instance variables.
   *
   * @param mockOutput The string that will be returned when calling makeRecipe
   */
  public void setOutput(String mockOutput) {
    this.mockOutput = mockOutput;
  }
}
```