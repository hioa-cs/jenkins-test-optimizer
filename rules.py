import random

class Rules:
    def __init__(self, dataset: dict) -> None:
        self.dataset = dataset
        self.available_tests = [id for id in dataset.keys()]

    def construct_one_rule_on_test(self, depend_number: int) -> None:
        # Pick a test to construct this number of dependencie on.
         test_id = random.choice(self.available_tests)
         self.available_tests.remove( test_id )

         possible_dependencies = [key for key in self.dataset.keys() if key is not test_id]
         choosen_dependencies = random.sample(possible_dependencies, k=depend_number)

         #Add this number of dependencies to this test
         self.dataset[test_id]['Depend'] = choosen_dependencies

         print("Test_ID {} with rules {}".format(test_id, choosen_dependencies))

    def construct_one_ruleset(self, tests_number: int, depend_number: int) -> None:
        for i in range(0, tests_number):
            self.construct_one_rule_on_test(depend_number)

    def construct_all_ruleset(self, test_depend_rules: tuple):
        for ruleset in test_depend_rules:
            tests_number = ruleset[0]  # Number of tests
            depend_number = ruleset[1] # Number of dependencies for 'tests_number' of rules
            self.construct_one_ruleset(tests_number, depend_number)
