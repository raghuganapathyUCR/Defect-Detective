import os
import random
import subprocess
import json
import gzip
def TestRandomTestPrioritization(statementBasedRandomTestSuite):
       for testcase in statementBasedRandomTestSuite:
            subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", "tcas", self.path + "tcas.c"])


            # Remove any whitespace from the beginning and end of the testcase
            testcase = testcase.strip()
            print(f"Running testcase {i+1}... ", testcase)

            # Run the testcase and save the "True" result as indicated in the project description
            agrsTest = testcase.split()
            result = subprocess.run(["./tcas"] + agrsTest, stdout=subprocess.PIPE)

            subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", "tcas"], stdout=subprocess.PIPE)

def RandomTestPrioritization(coverage):
        testcases =  coverage
        visited_lines = set()  # To keep track of the lines that have been covered

        # Shuffle the testcases randomly
        random.shuffle(testcases)

        statementBasedRandomTestSuite =[]
        # Iterate through the shuffled testcases
        for testcase in testcases:
            # Get the set of visited lines for the current testcase
            testcase_visited = set(testcase['lines']['visited'])

            # If there is no overlap between the visited lines of the current testcase and the visited lines already covered, add the current testcase to the output
            if not testcase_visited.issubset(visited_lines):
                statementBasedRandomTestSuite.append(testcase['testcase'])
                # Add the visited lines of the current testcase to the set of covered lines
                visited_lines.update(testcase_visited)
      
        print(len(visited_lines))
        return statementBasedRandomTestSuite
import json

def calculate_branch_coverage():
    total_branches = 0
    executed_branches = 0
    true_branches = 0
    false_branches = 0
    
    # Parse the JSON data
    # data = dict(json_data)
    with gzip.open('tcas.gcov.json.gz', 'rb') as f:
                json_bytes = f.read()                     
                json_str = json_bytes.decode('utf-8')            
                json_data = json.loads(json_str)
    
    # Loop through each file in the data
    for file_data in json_data['files']:
        # Loop through each line in the file
        for line_data in file_data['lines']:
            # If the line has branches
            if 'branches' in line_data:
                branches = line_data['branches']
              
                # Loop through each branch in the line
                for branch_data in branches:
                    total_branches += 1
                    if len(branch_data)>0 and branch_data['count'] > 0:
                        executed_branches += 1
                   
    print(total_branches)
    # Calculate the branch coverage
    if total_branches > 0:

        branch_coverage = float(executed_branches) / float(total_branches) * 100.0
    else:
        branch_coverage = 100.0
            
    return branch_coverage

def list_folders(path):
    folders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

if __name__ == "__main__":
    

    # a = list(a)
    # b = RandomTestPrioritization(a)
    # print(sorted(list_folders("../../benchmarks/tcas"),key = lambda x: int(x[1:])))
    
    print(calculate_branch_coverage())
    