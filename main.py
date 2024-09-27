import sys
import support
import os.path
import random 
import argparse
import rules

# Run with: python .\main.py -f dataset/iofrol.csv -t 10 15 -d 8 2
def main(dataset_name: str, test_depend_rules: tuple) -> None:
    dataset = support.get_dataset(dataset_name) 
    generator = rules.Rules(dataset)
    generator.construct_all_ruleset(test_depend_rules)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Algorithm for optimizing test sets')

    parser.add_argument("-f", type=str, dest='dataset_name', help='The input file name of dataset')
    parser.add_argument('-t', type=int, dest='tests',  default=[],  nargs='+', help='An array specifying the number of tests (-t) x which should have a dependency (-d) y, can not exceed maximum number of tests available')
    parser.add_argument("-d", type=int, dest='dependencies', default=[],  nargs='+', help='For each test x in -t, specifies the number of dependencies that should be created')

    args = parser.parse_args()

    if len(args.dependencies) != len(args.tests):
        print("The number of tests don't correspond with the number of added dependencies...")
        print("Tests {}, Dependencies {}".format(len(args.dependencies), len(args.tests)))
        print("Exiting script...")
        exit(0)
    if not os.path.isfile(args.dataset_name):
        print ("File {} does not exist".format(args.filename))
        print("Exiting script...")
        exit(0)
 
    test_depend_rules = list(map(lambda x, y:(x,y), args.dependencies, args.tests)) ## a tuple of ints [(10, 2), (20,4)]
    main(args.dataset_name, test_depend_rules)




