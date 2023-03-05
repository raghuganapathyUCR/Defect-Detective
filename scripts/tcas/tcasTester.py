import copy
import json
import gzip
import subprocess
import random

import os

class TCASTESTER:
    # Constructor for the TCASTESTER class
    def __init__(self) -> None:
        # Path to the tcas directory
        self.path = "../../benchmarks/tcas/"
        # List to store the coverage data for all testcases
        self.coverageData = []
        if(os.path.isfile("coverageData.json")):
            with open("coverageData.json", 'r') as file:
                content = file.read().strip()
                self.coverageData = json.loads(content)
                
           
        self.statementBasedRandomTestSuite = []
 
    
    # function to read a file line by line
    # @param fileName - the name of the file to read
    def readFile(self, fileName):
        print("TCASTESTER: readFile")
        file = open(fileName, "r")
        lines = file.readlines()
        file.close()
        return lines
    

    
    # Function to collect coverage information for all testcases
    # @return coverageData - a list of maps containing the coverage information for each testcase
    def collectCoverageInfoFromBaseForAllTestCases(self):
        print("TCASTESTER: collectCoverageInfoFromBaseForAllTestCases")
        if(os.path.isfile("coverageData.json")):
            with open("coverageData.json", 'r') as file:
                content = file.read().strip()
                self.coverageData = json.loads(content)

                return self.coverageData
       
        

        with open(f'{self.path}universe.txt', 'r') as f:
            testcases = f.readlines()

        # Create a list to store the coverage information for each testcase
        coverage_info = []

        # Loop through each testcase and run it
        for i, testcase in enumerate(testcases):
        
            # Map to store the coverage metadata for the current testcase
            coverageMeta = {}

            # Compile the program with gcov flags
            subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", "tcas", self.path + "tcas.c"])


            # Remove any whitespace from the beginning and end of the testcase
            testcase = testcase.strip()
            print(f"Running testcase {i+1}... ", testcase)

            # Run the testcase and save the "True" result as indicated in the project description
            agrsTest = testcase.split()
            result = subprocess.run(["./tcas"] + agrsTest, stdout=subprocess.PIPE)

            # capture the metadata for the current testcase
            coverageMeta["testcaseID"] = i+1
            coverageMeta["testcase"] = testcase
            coverageMeta["TrueResult"] = result.stdout.decode('utf-8').strip()


            # Run gcov on the output binary
            gcovRes = subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", "tcas"], stdout=subprocess.PIPE)


            # Read the gcov output file and parse it into a JSON dictionary
            with gzip.open('tcas.gcov.json.gz', 'rb') as f:
                json_bytes = f.read()                     
                json_str = json_bytes.decode('utf-8')            
                json_data = json.loads(json_str)     

                # Parse the JSON data to get the coverage information- block coverage, line coverage, and per-function coverage
                coverageInfo = self.parseJsonDataForCoverage(json_data)


                # Add the coverage metadata to the coverage information
                coverageInfo.update(coverageMeta)

                # Add the coverage information for this testcase to the list of coverage information of all testcases
                self.coverageData.append(coverageInfo)
            
            # Remove the gcov output files and the binary
            subprocess.run(["rm", "-rf", "tcas.gcno"])
            subprocess.run(["rm", "-rf", "tcas"])
            subprocess.run(["rm", "-rf", "./tcas.dSYM"])
            subprocess.run(["rm", "-rf", "./tcas.gcda"])
            subprocess.run(["rm", "-rf", "tcas.gcov.json.gz"])
        
        return self.coverageData



        
    # Function to parse the JSON data from gcov for coverage information
    # @param json_data - the JSON data from gcov
    # @return coverageInfo - a map containing the coverage information
    def parseJsonDataForCoverage(self, json_data):
        # Map to store the coverage information
        coverageInfo = {}
        # Read line coverage information from the JSON data
        lines = json_data['files'][0]['lines']

        # store the covered lines and total lines count
        covered_lines = [line for line in lines if line['count'] > 0]
        total_lines = len(lines)

        # Calculate the block coverage
        covered_ratio = len(covered_lines) / total_lines

        # Add the block coverage to the coverage information
        coverageInfo["blockCoverage"] = covered_ratio

        # To do the additional Coverage part
        # Map to store the line coverage information
        mp = {
            "visited" : [],
            "notVisited" : []
        }
        # Counters to store the total number of branches and the number of taken branches
        total_branches = 0
        taken_branches = 0
        # Loop through each line in the JSON data
        for line in lines:
            # If the line was executed, add it to the list of visited lines
            if line["count"] > 0:
                mp["visited"].append(line["line_number"])
            else:
                # Otherwise, add it to the list of not visited lines
                mp["notVisited"].append(line["line_number"])
            
            # If the line has "branches", loop through each branch
            if "branches" in line:
                # Loop through each branch in the line
                for branch in line["branches"]:
                    # Increment the total number of branches
                    total_branches += 1
                    # If the branch was taken, increment the taken branches
                    if branch["count"] > 0:
                        taken_branches += 1
        # Calculate the branch coverage
        if total_branches > 0:
            branch_coverage = (taken_branches / total_branches) * 100
        else:
            branch_coverage = 0.0

        # Add the branch coverage to the coverage information
        coverageInfo["lines"] = mp


        # Per-Function Coverage - May not be needed, but added for completeness of report   
        fnMp = {}
        for function in json_data['files'][0]['functions']:

            fnBlockCoverage = function["blocks_executed"] / function["blocks"] 
            fnMp[function["name"]] = fnBlockCoverage
            # print("\t",function)
        coverageInfo["functionData"] = fnMp

        return coverageInfo

    # Function to return the coverage data
    # @return coverageData - the coverage data
    def getCoverageData(self):
        print("TCASTESTER: getCoverageData")
        return self.coverageData
    

    def RandomTestPrioritization(self,coverage):
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

        self.statementBasedRandomTestSuite = statementBasedRandomTestSuite
        print("\nLength of statementBasedRandomTestSuite: ", len(statementBasedRandomTestSuite))
        return statementBasedRandomTestSuite
    

    # Function to dump the coverage data to a JSON file
    # @param coverageData - the coverage data
    # @param filename - the filename to dump the coverage data to
    # @return None
    def dumpCoverageData(self, coverageData, filename):
        if(os.path.isfile("coverageData.json")):
           return
        with open(filename, 'w') as outfile:
            json.dump(coverageData, outfile)

    
    # Function to dump the test suite to a file
    # @param self - the object pointer
    # @return None
    def TestRandomTestPrioritization(self):
        if len(self.statementBasedRandomTestSuite)==0:
            NotImplementedError("This function need to be run after RandomTestPrioritization()")
        visited_lines = set()  # To keep track of the lines that have been covered
        for testcase in self.statementBasedRandomTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", "tcas", self.path + "tcas.c"])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                # Run the testcase and save the "True" result as indicated in the project description
                agrsTest = testcase.split()
                result = subprocess.run(["./tcas"] + agrsTest, stdout=subprocess.PIPE)
                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", "tcas"], stdout=subprocess.PIPE)

                with gzip.open('tcas.gcov.json.gz', 'rb') as f:
                    json_bytes = f.read()                     
                    json_str = json_bytes.decode('utf-8')            
                    json_data = json.loads(json_str)     
                    
                    # Parse the JSON data to get the coverage information- block coverage, line coverage, and per-function coverage
                    coverageInfo = self.parseJsonDataForCoverage(json_data)
                    total_lines = len(coverageInfo['lines']['visited']) + len(coverageInfo['lines']['notVisited'])

                    # Add the coverage information to the list of coverage data
                    testcase_visited = set(coverageInfo['lines']['visited'])
                    if not testcase_visited.issubset(visited_lines):
                        print("Adding the following lines to the visited_lines set: ", testcase_visited.difference(visited_lines))
                        print("Visited Lines is currently: ", visited_lines)
                        visited_lines.update(testcase_visited)
                        print("Length of visited lines currently", len(visited_lines))
                        print("total number of lines: ",total_lines)
                        print("Coverage For the suite is currently: ", len(visited_lines)/total_lines)
                        
                        print("\n\n")
                subprocess.run(["rm", "-rf", "tcas.gcno"])
                subprocess.run(["rm", "-rf", "tcas"])
                subprocess.run(["rm", "-rf", "./tcas.dSYM"])
                subprocess.run(["rm", "-rf", "./tcas.gcda"])
                subprocess.run(["rm", "-rf", "tcas.gcov.json.gz"])
                        


if __name__ == "__main__":
    print("TCASTESTER: main")
    tester = TCASTESTER()
    # Experiment 1 - Collect coverage information for all testcases
    tester.collectCoverageInfoFromBaseForAllTestCases()
    # Test 1 - Print the coverage information, which should be a list of maps containing
    # the coverage information for each testcase
    print(tester.getCoverageData())


    # Test 2 - Dump the coverage information to a file
    tester.dumpCoverageData(tester.getCoverageData(), "coverageData.json")

    # Experiment 2 - Collect coverage information for the statement-based random test suite
    coverageData = tester.getCoverageData()
    randomTests = tester.RandomTestPrioritization(coverageData)
    print(randomTests)

    # Experiment 3 - Test Quality of suite for statement coverage
    tester.TestRandomTestPrioritization()