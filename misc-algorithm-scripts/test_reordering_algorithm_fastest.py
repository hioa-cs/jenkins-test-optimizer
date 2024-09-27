#! /usr/bin/env python

#####Note: The test position found in testdataset is not used in sorting.
##### They will be used for other computations

import sys
import operator
import time

filename = sys.argv[1]
tests = []
test_pos = {}
dataset = []
pre_tests = {}
sub_tests = {}
sub_tests_combo = []
global no_of_swap
no_of_swap = 0

######################### GETTING TESTS from FILE #########################

def get_data(filename): # funtion in class as attribute can be a METHOD
    f = open(filename,"r")
    dataset = f.readlines()

    for line in dataset:
        line.split(',')
        tests.append(line.replace('\n',''))
    print "TEST DATA COLLECTED FROM FILE and Stored in List"
#    print tests
    return tests


######################### GETTING SUB TESTS #########################

def get_subtest(testkey,pre_tests,k,origin):
    # ptest = one test list such as > C:'B','A'
    # pre_tests = is a dictionary of dependencies of each test
    # k = key
    combo = testkey + ":" + k + ":" + origin
    if combo not in sub_tests_combo:
        sub_tests_combo.append(combo)
    else:
        return

    ptest = pre_tests[testkey]

    if len(ptest) == 1 and ptest == '' :
        print "No known subtest for " + k + ", skipping"
        return

    for tname in ptest:
        if tname == k:
            if not testkey in sub_tests[origin]:
                # print 'storing {} as a subtest for {} in get_subtest'.format(testkey, origin)
                sub_tests[origin].append(testkey)
            for ktest in pre_tests:
                get_subtest(ktest,pre_tests,testkey,origin)

def compute_subtest(tests,pre_tests):
    for k in pre_tests:
        ptest = pre_tests[k]
        #print k
        #print ptest

        for tname in ptest:
            if tname == '' :
                print "No known pre test for " + k + ", skipping"
            else:
                #print "tname " + tname
                if not tname in sub_tests:
                    sub_tests[tname] = []
                print "tname in compute sub_tests " + tname
                if not k in sub_tests[tname]:
                    #print 'storing {} as a subtest for {}'.format(k, tname)
                    sub_tests[tname].append(k)
                # print sub_tests
                for ktest in pre_tests:
                    if not ktest + ":" + k + ":" + tname in sub_tests[tname]:
                        get_subtest(ktest,pre_tests,k,tname)

    for k in pre_tests:
        if not k in sub_tests:
            sub_tests[k] = []
    #    print sub_tests
    return sub_tests


def compute_subtest_fast(tests,pre_tests):

    for target in tests:
        target_name = target.split(",")[0]
        sub_tests[target_name] = []
        for current in tests:
            current_name = current.split(",")[0]
            if not current_name == target_name:
#                print "checking if " + current_name + " is has " + target_name + " as a dependency "
                ptests = []
                ptests = current.split(",")[3:]
                if target_name in ptests:
                    print current_name + " depends directly on " + target_name
                    sub_tests[target_name].append(current_name)
                elif [i for i in sub_tests[target_name] if i in ptests]:
                    print current_name + " depends indirectly on " + target_name
                    sub_tests[target_name].append(current_name)


 #   print sub_tests
    return sub_tests
######################### END OF GETTING SUB TESTS #########################


############################## Getting pre_tests - dependencies for test ###############################

def get_dependencies(test,ptest,ptests):
    # ptests has the same thing as tests
    # test = the test we are searching on behalf of
    # ptest = a test we found down the dependencie line (ptest is a list containing everything about this test)
    # pre_list = is an empty list that is assigned the ptest[] list as found in test
    pre_list = []
    pre_list = ptest.split(',')[3:]
    # print "pre_list"
    # print pre_list
    # 1. get all known get_dependencies
    print "Finding all unknown dependencies for " + test + " from " + ptest[0]
    if len(pre_list) == 1 and pre_list[0] == '':
        print "No known dependencies for " + ptest[0] + ", skipping"
        return

    for t in pre_list:
        if t not in pre_tests[test]:
            print "storing " + t + " as a dependencie for " + test
            pre_tests[test].append(t)
            for dep in ptests:
                if t == dep[0]:
                    get_dependencies(test,dep,ptests)

    # 2. add all known dependencies to t's list (if not there already)

    # 3. Call get dependencies for all known dependencies

def compute_pre_tests(ptests): # whole tests list, particular test positon - pos
    # ptests has the same thing as tests
    # print 'Compute pre test'
    # print ptests
    # pre_list = is an empty list that is assigned the r[3:] list of dependencies as found in ptests[]
    print "======= STARTS COMPUTING PRE-TESTS ======="
    pre_list = []

    counter = 0
    for r in ptests:
        r = r.split(',')
        pre_list = r[3:]
        test_pos[r[0]] = counter
        counter += 1
        #print ptests
        # print "pre_list"
        # print pre_list
        sublen = len(pre_list)
        tname = r[0]
        # print "tname in pre_tests" + tname
        pre_tests[tname] = []
        # print "Finding all dependencies for " + tname
        if len(pre_list) == 1 and pre_list[0] == '':
            print "No known dependencies for " + tname + ", skipping"
        #    return # with this return it skips finding dependencies if pre_list is empty
        #        print pre_list
        for t in pre_list:
            # print pre_list
            # print t
            #t = t.split(',') #newly added for splitting, because t was printing and storing the commas as values
            print 'storing {} as a dependency for {}'.format(t,tname)
            pre_tests[tname].append(t)
            for test in ptests:
                if t == test[0]:
                    get_dependencies(tname,test,ptests)
                    # test.append(tname)

#    print pre_tests
    return pre_tests

######################### END of Getting pre_tests - dependencies for test #####################

########################### COMPUTING MAX AND MIN VALUES ########################################

def find_max(tests, pos, tlist):
#    print "=== Finding MAX position for dependency list ==="
#    print tlist

    if tlist == []:
        return -1
    max_position = 0

    for t in tlist:
        # find t_position
        t_position = test_pos[t]
        if int(t_position) > int(max_position):
            max_position = t_position
#
    # print "Max position for list: "
    # print max_position
    return max_position

def find_min(tests, pos, tlist):

    #print "=== Finding MIN position for dependency list ==="
    #print tlist

    if tlist == []:
#        print "     -> find_min() deps empty, returning len(tests)"
        return len(tests) + 1
    min_position = len(tests)
    #print min_position

    for t in tlist:
    #    i = 0
        t_position = test_pos[t]
        if int(t_position) < int(min_position):
            min_position = t_position

    # print "Min postion for list: "
    # print min_position
#    print "     -> min position is " + str(min_position)
    return min_position

########################### END OF COMPUTING MAX AND MIN VALUES ############################

############ find POSITION #############

def find_xpos(tests,tx):
    tlen = len(tests)
    #print 'Finding position of x for swapping'
#    i = 0
    return test_pos[tx[0]]

    for t in tests:
    #    i = tests.index(t)+1
        if tx[0] == t.split(',')[0]:
            #print t[0:40]
            #print tx[0]
            xpos = tests.index(t)

    print xpos
    return int(xpos)


def find_ypos(tests,ty):
    tlen = len(tests)
    #print 'finding position of y for swapping'
#    i = 0
    return test_pos[ty[0]]

    for t in tests:
#        i = tests.index(t)+1
        if ty[0] == t.split(',')[0]:
            #print t[0:40]
            #print ty[0]
            ypos = tests.index(t)

    #print ypos
    return int(ypos)


##################################### SWAPPING TESTS #######################################
def swap(tests, tx, ty): # tx and ty contains list of each test

    #print "Swapping is Valid, therefore SWAPPING tests:"
    temp = []
    t = []
    xpos = find_xpos(tests,tx)
    ypos = find_ypos(tests,ty)
#    t = tx
    temp = tests[xpos]
#    tx = ty
    tests[xpos] = tests[ypos]
#    ty = t
    tests[ypos] = temp

    temp_pos = test_pos[tx[0]]
    test_pos[tx[0]] = test_pos[ty[0]]
    test_pos[ty[0]] = temp_pos

    return tests


##################################### REORDER ALGORITHM #######################################
#Using Lists
def reorder(tests,pre_tests,sub_tests,no_of_swap):

    print " ====== ***** Running Reorder Algorithm ***** ======"
    #print tests
#    i = 0
    time_now = []
    startreorder = time.time()
    original_tests = tests[:]
    for rx in original_tests:
        i = tests.index(rx)
        rx = rx.split(',')
        txname = rx[0]
        xpos = int(i)
        x_prob_fail= float(rx[2])
        delta_max = 0.0
        delta_max_test = 0.0

#        print "Testing RX: " + txname + " position: " + str(xpos)
#        j = 0

        for ry in tests:
            j = tests.index(ry)
            ry = ry.split(',')
            tyname = ry[0]
            delta_new = 0.0
            ypos = int(j)
            y_prob_fail = float(ry[2])
#            print " -> Testing RY: " + tyname + " position: " + str(ypos)
            if rx != ry:
                if xpos < ypos:
                    # if there are no dependencies these functions return zero
                    rx_sub_test_minpos = int(find_min(tests, xpos, sub_tests[txname]))
                    ry_pre_test_maxpos = int(find_max(tests, ypos, pre_tests[tyname]))
#                    print "  -> rx_sub_test_minpos: " + str(rx_sub_test_minpos) + " ry_pre_test_maxpos: " + str(ry_pre_test_maxpos)
                    # if there are no dependencies at all the loop fails to continue
                    if int(xpos) > int(ry_pre_test_maxpos) and int(ypos) < int(rx_sub_test_minpos):
                        #print "Comparing positions of tests for swapping"
                        if float(y_prob_fail) > float(x_prob_fail) :
                            # new value of decrease in time by doing swapping
                            # difference in test positions - difference in porbability of a test failing
                            delta_new = (y_prob_fail - x_prob_fail) * (ypos - xpos)
#                            print "   -> delta is " + str(delta_new)
                            if delta_max < delta_new:
                                delta_max = delta_new
                                delta_max_test = ry
#                                print "     -> storing " + tyname + " as swap candidate"
                                #print delta_max

                else:

#                    print "     -> calling find_min() for ry"
                    ry_sub_test_minpos = int(find_min(tests, ry, sub_tests[tyname]))
#                    print "     -> calling find_max() for rx"
                    rx_pre_test_maxpos = int(find_max(tests, rx, pre_tests[txname]))
                    if int(ypos) > int(rx_pre_test_maxpos) and int(xpos) < int(ry_sub_test_minpos):
                        #print "Comparing positions of tests for swapping"
                        if float(x_prob_fail) > float(y_prob_fail) :
                            delta_new = (x_prob_fail - y_prob_fail) * (xpos - ypos)
#                            print "   -> delta is " + str(delta_new)
                            # print delta_new
                            if delta_max < delta_new:
                                delta_max = delta_new
                                delta_max_test = ry # the whole test and its elements
#                                print "     -> storing " + tyname + " as swap candidate" # print delta_max

        if delta_max > 0:
            #print delta_max
            no_of_swap += 1
#            print no_of_swap
#            print " +> Swapping " + txname + " (" + str(xpos) + ") with " + delta_max_test[0]
            swap(tests, rx, delta_max_test)
#            for tmp in tests:
#                print tmp

        if ((i%100) == 0):
                time_now.append(time.time() - startreorder)


    print "====== Finished Running Reorder Algorithm ======"
    print "no_of_swap: " + str(no_of_swap)
    return delta_max, no_of_swap, time_now

##################################### END OF REORDER ALGORITHM ####################################

def main():
    starttime = time.time()
    print "Start time :", starttime
    compute_pre_tests(get_data(filename))
    endofpretests = time.time() - starttime
    print "pre_tests collection completed"
    #print pre_tests
    print "======== STARTS COMPUTING SUB TESTS ======="
    start_ofpretests = time.time()
    compute_subtest_fast(tests,pre_tests)
    endofsubtests = time.time() - start_ofpretests
    print "sub_tests collection completed"
    #print sub_tests
    start_ofreorder = time.time()
    delta_max, swapcounter, time_now = reorder(tests, pre_tests, sub_tests, no_of_swap)
    endofreordertests = time.time() - start_ofreorder

    #print tests

    print "Storing sorted list to csv"

    endtime = time.time()
    print "End time :", endtime

    timetaken = endtime - starttime
    print "total time taken to sort in seconds: ", timetaken

    #timestr = time.strftime("%H%M%S")
    outfile_name = '{0}{1}{2}'.format(filename,"_sorted",".csv")
#    with open('datasets/sorted_testdataset.csv', 'w') as f:
    with open(outfile_name, 'w') as f:
        for s in tests:
            f.write(s + '\n')

    outcomputationfile = '{0}{1}'.format(filename,"_time.txt")
    text_file = open(outcomputationfile, 'w')
    text_file.write("Test file used: {}\n".format(filename))
    text_file.write("Start time: {}\n".format(starttime))
    text_file.write("collecting pretests: {}\n".format(endofpretests))
    text_file.write("collecting subtests: {}\n".format(endofsubtests))
    text_file.write("reordering tests: {}\n".format(endofreordertests))
    text_file.write("End time: {}\n".format(endtime))
    text_file.write("No of swaps: {}\n".format(swapcounter))
    text_file.write("Total time taken: {} seconds.\n".format(timetaken))
    text_file.write("Reordering time for every 100 tests in list:\n")
    text_file.write(str(time_now))
    text_file.close()

# ONCE the test and swapping is done the test position in file only shows the
# before positions. Therefore no further sorting in recommended.


if __name__ == '__main__':
    main()
