BDD is the practice of taking an acceptance criteria, and writing a functional test for it. Then you write code at each layer starting from UI to controller downwards using TDD.
Finally once the functional test passes, it means the acceptance criteria is complete
and the functional test is written in a language like FITNESSE or Cucumber or Calabash which is very english sounding in nature, so even non tech people can understand functional tests

but to write that test
you have to write adapters that adapt what you've written in the test to an actual programming language
it leads to a messy spaghetti of adapters

https://blog.e-mundo.de/post/my-cucumber-is-better-than-your-fitnesse
