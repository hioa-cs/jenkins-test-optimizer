# test-optimizer

The aim  of this project is to explore the boundaries of software test automation
in a continuous delivery pipeline by implementing a re-ordering algorithm
to optimally sort the test cases such that tests with a higher likely hood of failing
are executed first, thus enabling faster feedback for failed tests to developers.

**This is a WIP**
-----------------

- DATASET: https://github.com/staiyeba/atcs-dataset
- DATASET Format notes: https://github.com/staiyeba/retecs-forked/tree/master
- Old Dataset format: https://github.com/staiyeba/test-pipeline-optimizing-algorithm/blob/master/datasets/case_1/10000_3.csv

##The Algorithm

### A Test Optimization Algorithm
### An adaption of the RR-Algorithm

```for tx in tests:
    delta_max = 0
    for ty in tests:
        delta_new = 0
        if tx != ty:
             if tx.pos < ty.pos:
                if tx.pos < pre_test_max_pos(ty) and ty.pos > subsequent_test_min_pos(tx):
                    if tx.fail_prob < ty.fail_prob:
                        delta_new = (ty.fail_prob − tx.fail_prob) ∗ (ty.pos − tx.pos)
                        if delta_max < delta_new:
                            delta_max = delta_new
            else:
                if ty.pos < pre_test_max_pos(tx) and tx.pos > subsequent_test_min_pos(ty):
                    if ty.fail_prob < tx.fail_prob:
                        delta_new = (tx.fail_prob − ty.fail_prob) ∗ (tx.pos − ty.pos)
                        if delta_max < delta_new:
                            delta_max = delta_new
    if delta_max > 0:
       swap(tx, ty)
```
