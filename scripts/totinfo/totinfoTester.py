import json
import gzip
import subprocess
import random
import os

class TOTINFOTESTER:

    # Constructor for the TCASTESTER class
    def __init__(self) -> None:
        # Path to the tcas directory
        self.path = "../../benchmarks/totinfo/"
        # List to store the coverage data for all testcases
        self.coverageData = []
        # if the coverageData.json file exists, read it and store it in the coverageData list, saves time while debugging
        if(os.path.isfile("coverageData.json")):
            with open("coverageData.json", 'r') as file:
                content = file.read().strip()
                self.coverageData = json.loads(content)
        
     
        self.program = "totinfo"
        self.fileName = "totinfo.c"

        self.testcases = []
        # Create a list to store the testcases from the universe.txt file
        with open(f'{self.path}universe.txt', 'r') as f:
            testcases = f.readlines()
            self.testcases = testcases
            f.close()

       
        
        # List to store the testcases for the statement based random test suite
        self.statementBasedRandomTestSuite = []

        # List to store the testcases for the branch based random test prioritization suite
        self.branchBasedRandomTestSuite = []

        # List to store the testcases for the statement based total test prioritization suite
        self.statementBasedTotalTestSuite = []

        # List to store the testcases for the branch based total test prioritization suite
        self.branchBasedTotalTestSuite = []
        # List to store the testcases for the statement based additional coverage test suite
        self.additionalCoverageBasedTestSuite = []

        self.brachBasedAdditionalCoverageBasedTestSuite = []

        # List to store the testcases for the branch based additional coverage test suite
        
        # These lists are used to store the coverage information for the statement based test suites, used in the fault finding part
        self.statementBasedRandomTestSuiteExtraCoverageInfo = []
        self.statementBasedTotalTestSuiteExtraCoverageInfo = []
        self.statementBasedAdditionalTestSuiteExtraCoverageInfo = []
        self.branchBasedRandomTestSuiteExtraCoverageInfo = []
        self.branchBasedTotalTestSuiteExtraCoverageInfo = []
        self.branchBasedAdditionalTestSuiteExtraCoverageInfo = []
        

        # Fault finding part
        # List to store the faults in the universe.txt file
        self.baseFaults = []

    def cleanUpInputs(self,input):
        input = input.strip().split(" ")
        input[1] = self.path + input[1]
        input = " ".join(input)
        return input


    
    # Function to collect coverage information for all testcases
    # @return coverageData - a list of maps containing the coverage information for each testcase
    def collectCoverageInfoFromBaseForAllTestCases(self):
        print("TCASTESTER: collectCoverageInfoFromBaseForAllTestCases")
        testcases = self.testcases

        # if the coverageData.json file exists, read it and store it in the coverageData list. Return the coverageData list instead of 
        # collecting coverage information again
        if(os.path.isfile("coverageData.json")):
            with open("coverageData.json", 'r') as file:
                content = file.read().strip()
                self.coverageData = json.loads(content)
                file.close()
                return self.coverageData
       
        
    

        # Create a list to store the coverage information for each testcase
        coverage_info = []

        # Loop through each testcase and run it
        for i, testcase in enumerate(testcases):

        
            # Map to store the coverage metadata for the current testcase
            coverageMeta = {}

            # Compile the program with gcov flags
            subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", self.program , self.path + self.fileName])


            # Remove any whitespace from the beginning and end of the testcase
            testcase = testcase.strip()

            # Run the testcase and save the "True" result as indicated in the project description
            testcase = self.cleanUpInputs(testcase)
   
            result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)
      
            
            
            if(i == (0.1*len(testcases)-(0.1*len(testcases))%10)):
                print("Collected 10 percent of the coverage data")
            if(i == (0.2*len(testcases)-(0.2*len(testcases))%10)):
                print("Collected 20 percent of the coverage data")
            if(i == (0.3*len(testcases)-(0.3*len(testcases))%10)):
                print("Collected 30 percent of the coverage data")
            if(i == (0.4*len(testcases)-(0.4*len(testcases))%10)):
                print("Collected 40 percent of the coverage data")
            if(i == (0.5*len(testcases)-(0.5*len(testcases))%10)):
                print("Collected 50 percent of the coverage data")
            if(i == (0.6*len(testcases)-(0.6*len(testcases))%10)):
                print("Collected 60 percent of the coverage data")
            if(i == (0.7*len(testcases)-(0.7*len(testcases))%10)):
                print("Collected 70 percent of the coverage data")
            if(i == (0.8*len(testcases)-(0.8*len(testcases))%10)):
                print("Collected 80 percent of the coverage data")
            if(i == (0.9*len(testcases)-(0.9*len(testcases))%10)):
                print("Collected 90 percent of the coverage data")
        


            # capture the metadata for the current testcase
            coverageMeta["testcaseID"] = i+1
            coverageMeta["testcase"] = testcase
            coverageMeta["TrueResult"] = result.stdout.decode('utf-8').strip()


            # Run gcov on the output binary
            gcovRes = subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)
            # print(gcovRes.stdout.decode('utf-8').strip())


            # Read the gcov output file and parse it into a JSON dictionary
            with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
                json_bytes = f.read()                     
                json_str = json_bytes.decode('utf-8')            
                json_data = json.loads(json_str)     

                # Parse the JSON data to get the coverage information- block coverage, line coverage, and per-function coverage
                coverageInfo = self.parseJsonDataForCoverage(json_data)


                # Add the coverage metadata to the coverage information
                coverageInfo.update(coverageMeta)

                # Add the coverage information for this testcase to the list of coverage information of all testcases
                self.coverageData.append(coverageInfo)
                f.close()
            
            # Remove the gcov output files and the binary
            self.cleanUpBetweenRuns()
        
        print("Collected 100 percent of the coverage data")
        
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
        lnMp = {
            "visited" : [],
            "notVisited" : []
        }

        # to do the branch coverage part
        brMp = {
            "visited" : [],
            "notVisited" : []
        }
        # Counters to store the total number of branches and the number of taken branches
        total_branches = 0
        taken_branches = 0
        # Loop through each line in the JSON data
        for line in lines:
            # If the line was executed, add it to the list of visited lines

            count = line["count"]
            if count > 0:
                lnMp["visited"].append(line["line_number"])
            else:
                # Otherwise, add it to the list of not visited lines
                lnMp["notVisited"].append(line["line_number"])
            
            # If the line has "branches", loop through each branch
            branches = line["branches"]
            if branches:
                for i, branch in enumerate(branches):
                    # Increment the total number of branches
                    total_branches += 1

                    branchCount = branch["count"]
                    # If the branch was executed, add it to the list of visited branches
                    if branchCount > 0:
                        brMp["visited"].append((line["line_number"],i))
                        taken_branches += 1 
                    # Otherwise, add it to the list of not visited branches
                    else:
                        brMp["notVisited"].append((line["line_number"],i))

                    

                        
        # Calculate the branch coverage
        if total_branches > 0:
            branch_coverage = (len(brMp['visited']) / (len(brMp['visited'])+len(brMp['notVisited']))) * 100
        else:
            branch_coverage = 0.0
        # Add the branch coverage to the coverage information
        coverageInfo["lines"] = lnMp
        coverageInfo["branches"] = brMp
        coverageInfo["branchCoverage"] = branch_coverage


        return coverageInfo

    # Function to return the coverage data
    # @return coverageData - the coverage data
    def getCoverageData(self):
        print("TCASTESTER: getCoverageData")
        return self.coverageData
    

    # Function to return the base faults
    # @return baseFaults - the base faults
    def getBaseFaults(self):
        if os.path.exists("baseFaults.json"):
            with open("baseFaults.json") as f:
                faultsDetected = json.load(f)
            return faultsDetected
        Exception("Base Faults not found")


    def getSizeOfBaseTestSuite(self):
        return len(self.testcases)
    
    # Function to dump the coverage data to a JSON file
    # @param coverageData - the coverage data
    # @param filename - the filename to dump the coverage data to
    # @return None
    def dumpCoverageData(self, coverageData, filename):
        if(os.path.isfile("coverageData.json")):
           return
        with open(filename, 'w') as outfile:
            json.dump(coverageData, outfile)

    # Function to build the test suite base on the random test prioritization technique - based on the statement coverage
    def RandomTestPrioritizationStatementBased(self,coverage):
        testcases =  coverage.copy()
        visited_lines = set()  # To keep track of the lines that have been covered

        # Shuffle the testcases randomly
        random.shuffle(testcases)

        # List to store the test suite
        statementBasedRandomTestSuite =[]

        # list to store the extra coverage info of test suite
        statementBasedRandomTestSuiteExtraCoverageInfo = []
        # Iterate through the shuffled testcases
        for testcase in testcases:
            # Get the set of visited lines for the current testcase
            testcase_visited = set(testcase['lines']['visited'])

            # If there is no overlap between the visited lines of the current testcase and the visited lines already covered, add the current testcase to the output
            if not testcase_visited.issubset(visited_lines):
                statementBasedRandomTestSuite.append(testcase['testcase'])
                statementBasedRandomTestSuiteExtraCoverageInfo.append(testcase)
                # Add the visited lines of the current testcase to the set of covered lines
                visited_lines.update(testcase_visited)

        self.statementBasedRandomTestSuite = statementBasedRandomTestSuite
        self.statementBasedRandomTestSuiteExtraCoverageInfo = statementBasedRandomTestSuiteExtraCoverageInfo
        print("\nLength of statementBasedRandomTestSuite: ", len(statementBasedRandomTestSuite))
        return statementBasedRandomTestSuite
    
     # Function to build the test suite base on the random test prioritization technique - based on branch coverage
    def RandomTestPrioritizationBranchBased(self,coverage):
        testcases =  coverage.copy()
        visited_lines = set()  # To keep track of the lines that have been covered

        # Shuffle the testcases randomly
        random.shuffle(testcases)

        # List to store the test suite
        branchBansedRandomTestSuite =[]

        # list to store the extra coverage info of test suite
        branchBansedRandomTestSuiteExtraCoverageInfo = []
        # Iterate through the shuffled testcases
        for testcase in testcases:
            # Get the set of visited branches for the current testcase
            # first: convert the list of list to list of tuple
            tVistedListToTuple = [tuple(sublst) for sublst in testcase['branches']['visited']]

            # second: convert the list of tuple to set of tuple - this allows us to use the set operations like subset and difference
            testcase_visited = set(tVistedListToTuple)

            # If there is no overlap between the visited lines of the current testcase and the visited lines already covered, add the current testcase to the output
            if not testcase_visited.issubset(visited_lines):
                branchBansedRandomTestSuite.append(testcase['testcase'])
                branchBansedRandomTestSuiteExtraCoverageInfo.append(testcase)
                # Add the visited lines of the current testcase to the set of covered lines
                visited_lines.update(testcase_visited)

        self.branchBasedRandomTestSuite = branchBansedRandomTestSuite
        self.branchBasedRandomTestSuiteExtraCoverageInfo = branchBansedRandomTestSuiteExtraCoverageInfo
        print("\nLength of branchBansedRandomTestSuite: ", len(branchBansedRandomTestSuite))
        return branchBansedRandomTestSuite
    
    # # Function to test the iterative coverage algorithm described in the project description, 
    # to show that we iteratively cover more lines with each testcase
    # @param self - the object pointer
    # @return None
    def TestRandomPrioritizationStatementBased(self):
        if len(self.statementBasedRandomTestSuite)==0:
            raise NotImplementedError("This function need to be run after RandomTestPrioritization()")
        visited_lines = set()  # To keep track of the lines that have been covered
        for testcase in self.statementBasedRandomTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", self.program , self.path + self.fileName])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

               
                result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)

                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)

                with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
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
                self.cleanUpBetweenRuns()

    # Function to test the iterative coverage algorithm described in the project description, 
    # to show that we iteratively cover more branches with each testcase
    # @param self - the object pointer
    # @return None
    def TestRandomPrioritizationBranchBased(self):
        if len(self.branchBasedRandomTestSuite)==0:
            raise NotImplementedError("This function need to be run after RandomTestPrioritization()")
        visited_branches = set()  # To keep track of the lines that have been covered
        for testcase in self.branchBasedRandomTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", self.program , self.path + self.fileName])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                # Run the testcase and save the "True" result as indicated in the project description
                result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)

                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)

                with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
                    json_bytes = f.read()                     
                    json_str = json_bytes.decode('utf-8')            
                    json_data = json.loads(json_str)     
                    
                    # Parse the JSON data to get the coverage information- block coverage, line coverage, and per-function coverage
                    coverageInfo = self.parseJsonDataForCoverage(json_data)
                    total_branches = len(coverageInfo['branches']['visited']) + len(coverageInfo['branches']['notVisited'])

                    # Add the coverage information to the list of coverage data
                    testcase_visited = set(coverageInfo['branches']['visited'])
                    if not testcase_visited.issubset(visited_branches):
                        print("Adding the following branches to the visited_branches set: ", testcase_visited.difference(visited_branches))
                        print("Visited branches is currently: ", visited_branches)
                        visited_branches.update(testcase_visited)
                        print("Length of visited branches currently", len(visited_branches))
                        print("total number of branches: ",total_branches)
                        print("Coverage For the suite is currently: ", len(visited_branches)/total_branches)
                        
                        print("\n\n")
                self.cleanUpBetweenRuns()
                        

    # Fuction to sort the list of testcases by length of visited lines
    # @param coverageData - the coverage data
    # @return sorted list of testcases
    def sortTestcasesByVisitedLinesLength(self,coverageData):
        return sorted(coverageData, key=lambda x: len(x['lines']['visited']),reverse=True)
    
     # Fuction to sort the list of testcases by length of visited branches
    # @param coverageData - the coverage data
    # @return sorted list of testcases
    def sortTestcasesByVisitedBranchesLength(self,coverageData):
        return sorted(coverageData, key=lambda x: len(x['branches']['visited']),reverse=True)

    

    # Function to build the test suite using the total coverage prioritization technique - based on statement coverage
    # @param self - the object pointer
    # @return totalCoverageBasedTestSuite - the test suite
    def TotalCoveragePrioritizationStatementBased(self):
        if len(self.coverageData)==0:
            raise NotImplementedError("Please Run the collectCoverageInfoFromBaseForAllTestCases() method first")

        # Sorted test case list based on order
        testcaseList = self.sortTestcasesByVisitedLinesLength(self.coverageData)

        print(testcaseList[0]['testcaseID'])
        # Set of visited lines, start at empty set fill as we go
        visitedLines = set()
        # list to store valid cases for this technique as per project decription
        totalCoverageBasedTestSuite = []

        # list to store the extra coverage info of test suite
        statementBasedTotalTestSuiteExtraCoverageInfo = []

        for test in testcaseList:
            # Get the set of visited lines for the current testcase
            currentlyVisited = set(test["lines"]["visited"])
            # If there is no overlap between the visited lines of the current testcase and the visited lines already covered,
            # add the current testcase to the output
            if not currentlyVisited.issubset(visitedLines):
                # Add the visited lines of the current testcase to the set of covered lines
                totalCoverageBasedTestSuite.append(test['testcase'])
                statementBasedTotalTestSuiteExtraCoverageInfo.append(test)
                # Add the visited lines of the current testcase to the set of covered lines
                visitedLines.update(currentlyVisited)

        # Store the test suite in the object
        self.statementBasedTotalTestSuite = totalCoverageBasedTestSuite
        self.statementBasedTotalTestSuiteExtraCoverageInfo = statementBasedTotalTestSuiteExtraCoverageInfo
        print("\nLength of statementBasedTotalTestSuite: ", len(totalCoverageBasedTestSuite))
        return totalCoverageBasedTestSuite

   # Function to build the test suite using the total coverage prioritization technique - based on branch coverage
    # @param self - the object pointer
    # @return totalCoverageBasedTestSuite - the test suite
    def TotalCoveragePrioritizationBranchBased(self):
        if len(self.coverageData)==0:
            raise NotImplementedError("Please Run the collectCoverageInfoFromBaseForAllTestCases() method first")

        # Sorted test case list based on order
        testcaseList = self.sortTestcasesByVisitedBranchesLength(self.coverageData)

        # Set of visited branches, start at empty set fill as we go
        visitedLines = set()
        # list to store valid cases for this technique as per project decription
        totalCoverageBasedTestSuite = []

        # list to store the extra coverage info of test suite
        branchBasedTotalTestSuiteExtraCoverageInfo = []

        for test in testcaseList:
            # Get the set of visited lines for the current testcase
            # Get the set of visited branches for the current testcase
            # first: convert the list of list to list of tuple
            tVistedListToTuple = [tuple(sublst) for sublst in test['branches']['visited']]

            # second: convert the list of tuple to set of tuple - this allows us to use the set operations like subset and difference
            currentlyVisited = set(tVistedListToTuple)

            # If there is no overlap between the visited lines of the current testcase and the visited lines already covered,
            # add the current testcase to the output
            if not currentlyVisited.issubset(visitedLines):
                # Add the visited lines of the current testcase to the set of covered lines
                totalCoverageBasedTestSuite.append(test['testcase'])
                branchBasedTotalTestSuiteExtraCoverageInfo.append(test)
                # Add the visited lines of the current testcase to the set of covered lines
                visitedLines.update(currentlyVisited)

        # Store the test suite in the object
        self.branchBasedTotalTestSuite = totalCoverageBasedTestSuite
        self.branchBasedTotalTestSuiteExtraCoverageInfo = branchBasedTotalTestSuiteExtraCoverageInfo
        print("\nLength of branchBasedTotalTestSuite: ", len(totalCoverageBasedTestSuite))
        return totalCoverageBasedTestSuite

    # Function to evaluate the incremental coverage of test suite based on the total statement coverage
    # @param self - the object pointer
    # @return None    
    def TestTotalTestPrioritizationStatementBased(self):
        if len(self.statementBasedTotalTestSuite)==0:
            raise NotImplementedError("This function need to be run after RandomTestPrioritization()")
        visited_lines = set()  # To keep track of the lines that have been covered
        for testcase in self.statementBasedTotalTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", self.program , self.path + self.fileName])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                # Run the testcase and save the "True" result as indicated in the project description
                result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)
                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)

                with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
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
                self.cleanUpBetweenRuns()

    # Function to evaluate the incremental coverage of test suite based on the total branch coverage
    # @param self - the object pointer
    # @return None    
    def TestTotalTestPrioritizationBranchBased(self):
        if len(self.branchBasedTotalTestSuite)==0:
            raise NotImplementedError("This function need to be run after RandomTestPrioritization()")
        visited_branch = set()  # To keep track of the branch that have been covered
        for testcase in self.branchBasedTotalTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o",self.program , self.path + self.fileName])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                # Run the testcase and save the "True" result as indicated in the project description
                result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)
                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)

                with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
                    json_bytes = f.read()                     
                    json_str = json_bytes.decode('utf-8')            
                    json_data = json.loads(json_str)     
                    
                    # Parse the JSON data to get the coverage information- block coverage, line coverage, and per-function coverage
                    coverageInfo = self.parseJsonDataForCoverage(json_data)
                    total_branch = len(coverageInfo['branches']['visited']) + len(coverageInfo['branches']['notVisited'])

                    # Add the coverage information to the list of coverage data
                    tVistedListToTuple = [tuple(sublst) for sublst in coverageInfo['branches']['visited']]

                    # second: convert the list of tuple to set of tuple - this allows us to use the set operations like subset and difference
                    testcase_visited = set(tVistedListToTuple)
                    if not testcase_visited.issubset(visited_branch):
                        print("Adding the following branch to the visited_branch set: ", testcase_visited.difference(visited_branch))
                        print("Visited branch is currently: ", visited_branch)
                        visited_branch.update(testcase_visited)
                        print("Length of visited branch currently", len(visited_branch))
                        print("total number of branch: ",total_branch)
                        print("Coverage For the suite is currently: ", len(visited_branch)/total_branch)
                        
                        print("\n\n")
                self.cleanUpBetweenRuns()


    # Function to build a test suite based on Additional Coverage Prioritization - based on statement coverage
    # @param self - the object pointer
    # @return additionalCoverageBasedTestSuite - the test suite
    def AdditionalCoveragePrioritizationStatementBased(self):
        if len(self.coverageData) == 0:
            raise NotImplementedError("Please run the collectCoverageInfoFromBaseForAllTestCases() method first")

        # Create a copy of the coverage data
        remainingTests = self.coverageData.copy()

        # Sort the test cases by length of visited lines
        remainingTests = self.sortTestcasesByVisitedLinesLength(remainingTests)

        # Set of visited lines, start at empty set fill as we go
        visitedLines = set()

        # List to store valid cases for this technique as per project description
        additionalCoverageBasedTestSuite = []

        # List to store the extra coverage info of test suite
        statementBasedAdditionalTestSuiteExtraCoverageInfo = []

        # Iterate until all statements/branches are covered by at least one test case
        # TODO: Experiment with using a queue instead of a list to store the remaining tests, this may improve performance
        while remainingTests:
            bestTest = None
            maxNewLines = 0

            # Find the test case that yields the greatest additional statement/branch coverage
            for test in remainingTests:
                # Get the set of visited lines for the current testcase
                currentlyVisited = set(test["lines"]["visited"])
                # Get the number of new lines covered by this test case
                newLines = len(currentlyVisited - visitedLines)
                # If this test case covers more new lines than any previous test case, select it -  (i) select a 
                # test case that yields the greatest additional statement/branch coverage
                if newLines > maxNewLines:
                    # Update the best test case and the number of new lines covered
                    # (ii) then adjust the coverage information on subsequent test cases to 
                    # indicate their coverage of statements/branches not
                    # yet covered by a test already chosen for the suite
                    maxNewLines = newLines
                    # Store the test case that covers the greatest additional number of lines
                    bestTest = test
            
            # If there are no more test cases that cover new lines, stop - we have found the optimal test suite 
            if bestTest is None:
                break

            # Add the test case that covers the greatest additional number of lines to the output
            additionalCoverageBasedTestSuite.append(bestTest['testcase'])

            # Add the extra coverage info of the test case to the list
            statementBasedAdditionalTestSuiteExtraCoverageInfo.append(bestTest)

            # Add the visited lines of the current testcase to the set of covered lines
            visitedLines.update(set(bestTest["lines"]["visited"]))

            # Remove the selected test case from the remaining tests
            remainingTests.remove(bestTest)

        # Store the test suite in the object
        self.additionalCoverageBasedTestSuite = additionalCoverageBasedTestSuite
        self.statementBasedAdditionalTestSuiteExtraCoverageInfo = statementBasedAdditionalTestSuiteExtraCoverageInfo
        print("\nLength of additionalCoverageBasedTestSuite: ", len(additionalCoverageBasedTestSuite))
        return additionalCoverageBasedTestSuite
    
    # Function to build a test suite based on Additional Coverage Prioritization - based on branch coverage
    # @param self - the object pointer
    # @return additionalCoverageBasedTestSuite - the test suite
    def AdditionalCoveragePrioritizationBranchBased(self):
        if len(self.coverageData) == 0:
            raise NotImplementedError("Please run the collectCoverageInfoFromBaseForAllTestCases() method first")

       
        # Create a copy of the coverage data
        remainingTests = self.coverageData.copy()

        # Sort the test cases by length of visited lines
        remainingTests = self.sortTestcasesByVisitedLinesLength(remainingTests)

        # Set of visited lines, start at empty set fill as we go
        visitedBranches = set()

        # List to store valid cases for this technique as per project description
        additionalCoverageBasedTestSuite = []

        # List to store the extra coverage info of test suite
        branchBasedAdditionalTestSuiteExtraCoverageInfo = []

        # Iterate until all statements/branches are covered by at least one test case
        # TODO: Experiment with using a queue instead of a list to store the remaining tests, this may improve performance
        while remainingTests:
            bestTest = None
            maxNewBranches = 0

            # Find the test case that yields the greatest additional statement/branch coverage
            for test in remainingTests:
                # Get the set of visited Branches for the current testcase
                 # Add the coverage information to the list of coverage data
                tVistedListToTuple = [tuple(sublst) for sublst in test['branches']['visited']]

                # second: convert the list of tuple to set of tuple - this allows us to use the set operations like subset and difference
                currentlyVisited = set(tVistedListToTuple)
                # Get the number of new Branches covered by this test case
                newBranches = len(currentlyVisited - visitedBranches)
                # If this test case covers more new Branches than any previous test case, select it -  (i) select a 
                # test case that yields the greatest additional statement/branch coverage
                if newBranches > maxNewBranches:
                    # Update the best test case and the number of new Branches covered
                    # (ii) then adjust the coverage information on subsequent test cases to 
                    # indicate their coverage of statements/branches not
                    # yet covered by a test already chosen for the suite
                    maxNewBranches = newBranches
                    # Store the test case that covers the greatest additional number of Branches
                    bestTest = test
            
            # If there are no more test cases that cover new lines, stop - we have found the optimal test suite 
            if bestTest is None:
                break

            # Add the test case that covers the greatest additional number of lines to the output
            additionalCoverageBasedTestSuite.append(bestTest['testcase'])

            # Add the extra coverage info of the test case to the list
            branchBasedAdditionalTestSuiteExtraCoverageInfo.append(bestTest)

            bestVistedListToTuple = [tuple(sublst) for sublst in bestTest['branches']['visited']]

                # second: convert the list of tuple to set of tuple - this allows us to use the set operations like subset and difference
            bestTestBranches = set(bestVistedListToTuple)
            # Add the visited lines of the current testcase to the set of covered lines
            visitedBranches.update(bestTestBranches)

            # Remove the selected test case from the remaining tests
            remainingTests.remove(bestTest)

        # Store the test suite in the object
        self.brachBasedAdditionalCoverageBasedTestSuite = additionalCoverageBasedTestSuite
        self.branchBasedAdditionalTestSuiteExtraCoverageInfo = branchBasedAdditionalTestSuiteExtraCoverageInfo
        print("\nLength of additionalCoverageBasedTestSuite: ", len(additionalCoverageBasedTestSuite))
        return additionalCoverageBasedTestSuite
    
    # Function to evaluate the incremental coverage of test suite based on the additional statement coverage
    # @param self - the object pointer
    # @return None    
    def TestAdditionalTestPrioritizationStatementBased(self):
        if len(self.additionalCoverageBasedTestSuite)==0:
            raise NotImplementedError("This function need to be run after AdditionalCoveragePrioritization()")
        visited_lines = set()  # To keep track of the lines that have been covered
        for testcase in self.additionalCoverageBasedTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", self.program , self.path + self.fileName])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                # Run the testcase and save the "True" result as indicated in the project description
                result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)
                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)

                with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
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
                self.cleanUpBetweenRuns()
    
     # Function to evaluate the incremental coverage of test suite based on the additional branch coverage
    # @param self - the object pointer
    # @return None    
    def TestAdditionalTestPrioritizationBranchBased(self):
        if len(self.brachBasedAdditionalCoverageBasedTestSuite)==0:
           raise NotImplementedError("This function need to be run after AdditionalCoveragePrioritization()")
        visited_branches = set()  # To keep track of the branches that have been covered
        for testcase in self.brachBasedAdditionalCoverageBasedTestSuite:
                subprocess.run(["gcc-12", "-Wno-return-type", "-fprofile-arcs", "-ftest-coverage", "-w", "-g", "-o", self.program , self.path + self.fileName])

            

                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                # Run the testcase and save the "True" result as indicated in the project description
                result = subprocess.run(f"./totinfo {testcase}", shell=True,stdout=subprocess.PIPE)
                print(f"Running testcase... ", testcase)
                subprocess.run(["gcov-12","-a","-w","-b","-f", "-j", self.program], stdout=subprocess.PIPE)

                with gzip.open(f'{self.program}.gcov.json.gz', 'rb') as f:
                    json_bytes = f.read()                     
                    json_str = json_bytes.decode('utf-8')            
                    json_data = json.loads(json_str)     
                    
                    # Parse the JSON data to get the coverage information- block coverage, line coverage, and per-function coverage
                    coverageInfo = self.parseJsonDataForCoverage(json_data)
                    total_branches = len(coverageInfo['branches']['visited']) + len(coverageInfo['branches']['notVisited'])

                    # Add the coverage information to the list of coverage data
                    tVistedListToTuple = [tuple(sublst) for sublst in coverageInfo['branches']['visited']]

                        # second: convert the list of tuple to set of tuple - this allows us to use the set operations like subset and difference
                    testcase_visited = set(tVistedListToTuple)
                    if not testcase_visited.issubset(visited_branches):
                        print("Adding the following branches to the visited_branches set: ", testcase_visited.difference(visited_branches))
                        print("Visited branches is currently: ", visited_branches)
                        visited_branches.update(testcase_visited)
                        print("Length of visited branches currently", len(visited_branches))
                        print("total number of branches: ",total_branches)
                        print("Coverage For the suite is currently: ", len(visited_branches)/total_branches)
                        
                        print("\n\n")
                self.cleanUpBetweenRuns()

    # Function that returns a list of all folders in a benchmark programs path location
    # @param self - the object pointer
    # @return sorted list of directories which contain the mutant programs
    def listFolders(self):
        folders = []
        for item in os.listdir(self.path):
            item_path = os.path.join(self.path, item)
            if os.path.isdir(item_path):
                folders.append(item)
        folders.remove("universe")
        folders = sorted(folders, key = lambda x: int(x[1:]))
        return folders

    # Function to evaluate the fault detection capability of a test suite
    # @param self - the object pointer
    # @param testSuite - the test suite to evaluate
    # @return information about the fault detection capability of the test suite in a map
    def evaluateFaultDetectionCapability(self, name):

        # Check if baseFaults.json exists, if it does, load it and return, if not, create it
        if name=="base" and os.path.exists("baseFaults.json"):
            with open("baseFaults.json") as f:
                faultsDetected = json.load(f)
                del faultsDetected["testSuite"]
        
                count = 0
                for mutant in faultsDetected:
                    
                    if len(faultsDetected[mutant])>0:
                        count+=1
                
                mutationScore = count/len(faultsDetected)
                    
                print(f"Mutation Score is {mutationScore} for {name}: it kills {count} out of {len(faultsDetected)} mutants.")
            return faultsDetected

        if name == "RandomTestPrioritizationStatementBased":
            testSuite = self.statementBasedRandomTestSuiteExtraCoverageInfo
        elif name == "TotalCoveragePrioritizationStatementBased":
            testSuite = self.statementBasedTotalTestSuiteExtraCoverageInfo
        elif name == "AdditionalCoveragePrioritizationStatementBased":
            testSuite = self.statementBasedAdditionalTestSuiteExtraCoverageInfo
        elif name == "RandomTestPrioritizationBranchBased":
            testSuite = self.branchBasedRandomTestSuiteExtraCoverageInfo
        elif name == "TotalCoveragePrioritizationBranchBased":
            testSuite = self.branchBasedTotalTestSuiteExtraCoverageInfo
        elif name == "AdditionalCoveragePrioritizationBranchBased":
            testSuite = self.branchBasedAdditionalTestSuiteExtraCoverageInfo
        elif name =="base":
            testSuite = self.coverageData
        else:
            raise ValueError("The name of the test suite is not valid")

        if len(testSuite)==0:
            raise NotImplementedError(f"This function need to be run after the test suite for {name} is generated")
        # Create a map to store the fault detection capability information
        faultsDetected = {}
        faultsDetected["testSuite"] = name
        folders = self.listFolders()

        for folder in folders:
             # compile the mutant program
            subprocess.run(["gcc-12", "-Wno-return-type", "-w", "-g", "-o", self.program , self.path+folder+"/" + self.fileName])
            # Faults in this test
            testFaults = []
            print("Compiling mutant program: ", folder, " for all test cases in the test suite: ", name)
            for test in testSuite:
                testcase = test['testcase']
                # Remove any whitespace from the beginning and end of the testcase
                testcase = testcase.strip()

                

               
                # Run the testcase and save the "True" result as indicated in the project description
                

                # Run the testcase and save the result to compare with the true result
                result = subprocess.run(f"./totinfo {testcase}", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                
                if result.stdout.decode('utf-8').strip() != test["TrueResult"]:
                    faultsForCurrentMutantGivenATestCase = {}
                    faultsForCurrentMutantGivenATestCase["testcaseID"] = test["testcaseID"]
                    faultsForCurrentMutantGivenATestCase["testcase"] = test["testcase"]
                    faultsForCurrentMutantGivenATestCase["TrueResult"] = test["TrueResult"]
                    faultsForCurrentMutantGivenATestCase["MutantResult"] = result.stdout.decode('utf-8').strip()
                    if result.stderr:
                        faultsForCurrentMutantGivenATestCase["error"] = result.stderr.decode('utf-8').strip()
                    testFaults.append(faultsForCurrentMutantGivenATestCase)
                
            # clear binary before running the next mutant   
            subprocess.run(["rm", "-rf", self.program])
            faultsDetected[folder] = testFaults

        # Dump the fault detection capability information to a file
        if name == "base":
            fName = "BaseFaults.json"
        elif name == "RandomTestPrioritizationStatementBased":
           fName = "RandomTestPrioritizationStatementBasedFaults.json"
        elif name == "TotalCoveragePrioritizationStatementBased":
            fName = "TotalCoveragePrioritizationStatementBasedFaults.json"
        elif name == "AdditionalCoveragePrioritizationStatementBased":
            fName = "AdditionalCoveragePrioritizationStatementBasedFaults.json"
        elif name == "RandomTestPrioritizationBranchBased":
            fName = "RandomTestPrioritizationBranchBasedFaults.json"
        elif name == "TotalCoveragePrioritizationBranchBased":
            fName = "TotalCoveragePrioritizationBranchBasedFaults.json"
        elif name == "AdditionalCoveragePrioritizationBranchBased":
            fName = "AdditionalCoveragePrioritizationBranchBasedFaults.json"
        else:
            raise ValueError("The name of the test suite is not valid")
        
        with open(fName, 'w') as outfile:
            json.dump(faultsDetected, outfile, indent=4)
        
        if name == "base":
            self.baseFaults = faultsDetected
        # Return the fault detection capability of the test suite

        del faultsDetected["testSuite"]
        
        count = 0
        for mutant in faultsDetected:
            
            if len(faultsDetected[mutant])>0:
                count+=1
        
        mutationScore = count/len(faultsDetected)
            
        print(f"Mutation Score is {mutationScore} for {name}: it kills {count} out of {len(faultsDetected)} mutants.")
    
        return faultsDetected
        
    def cleanUpBetweenRuns(self):
        subprocess.run(["rm", "-rf", f"{self.program}.gcno"])
        subprocess.run(["rm", "-rf", f"{self.program}"])
        subprocess.run(["rm", "-rf", f"./{self.program}.dSYM"])
        subprocess.run(["rm", "-rf", f"./{self.program}.gcda"])
        subprocess.run(["rm", "-rf", f"{self.program}.gcov.json.gz"])
        

if __name__ == "__main__":
    print("TCASTESTER: main")
    print("Task: For tcas.c and it's associated universe we have to do the following: ")
    print("\t1) Collect coverage information for all testcases - we collect the following coverage information for each testcase: ")
    print("\t\t1.1) it's statement coverage")
    print("\t\t1.2) it's branch coverage")
    print("\t\t1.3) it's true result - the output of the base program when the testcase is run")
    print("\t\t1.4) the lines of code that are executed by the testcase")
    print("\t\t1.5) the lines of code that are not executed by the testcase")
    print("\t\t1.6) the branches of code that are executed by the testcase")
    print("\t\t1.7) the branches of code that are not executed by the testcase")
    print("\t\t1.8) the testcase itself")
    print("\t\t1.9) the testcase ID")
    print("\t2) Based on the collected coverage info we build the following test suites for 2 different coverage criteria: ")
    print("\t\t2.1) Statement Coverage")
    print("\t\t\t2.1.1) Random Test Suite")
    print("\t\t\t2.1.2) Total Coverage Test Suite")
    print("\t\t\t2.1.3) Additional Coverage Test Suite")
    print("\t\t2.2) Branch Coverage")
    print("\t\t\t2.2.1) Random Test Suite")
    print("\t\t\t2.2.2) Total Coverage Test Suite")
    print("\t\t\t2.2.3) Additional Coverage Test Suite")
    print("\t3) For each test suite we calculate the fault detection capability of the test suite")
    print("\t4) We alaso calculate the fault detection capability of the universe of testcases")

    print("\n-------------------------------------------------START OF EXPERIMENT------------------------------------------------\n")
    print("------------------------------------------COLLECTING COVERAGE FOR UNIVERSE------------------------------------------\n")



    
    tester = TOTINFOTESTER()
    # Experiment 1 - Collect coverage information for all testcases
    print("1. Collecting coverage information for all testcases")
    tester.collectCoverageInfoFromBaseForAllTestCases()
    # Test 1 - Print the coverage information, which should be a list of maps containing
    # the coverage information for each testcase
    

    # Test 2 - Dump the coverage information to a file
    tester.dumpCoverageData(tester.getCoverageData(), "coverageData.json")

    print("\n---------------------------1. COLLECTED COVERAGE FOR UNIVERSE AND DUMPED TO coverageData.json--------------------------\n")
    # Experiment 2 - Collect coverage information for the statement-based random test suite
    coverageData = tester.getCoverageData()
    print("\n-----------------------------2. BUILDING RANDOM TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    randomTests = tester.RandomTestPrioritizationStatementBased(coverageData)
 

    #  Experiment 3 - Test Quality of suite for statement coverage of random test suite
    print("\n-----------------------------3. TESTING RANDOM TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    tester.TestRandomPrioritizationStatementBased()
    coverageData = tester.getCoverageData()

    print("\n-----------------------------4. BUILDING TOTAL TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    randomTests = tester.RandomTestPrioritizationBranchBased(coverageData)
 
    print("\n-----------------------------5. TESTING RANDOM TEST SUITE FOR BRANCH COVERAGE--------------------------------------\n")
    # # Experiment 3 - Test Quality of suite for statement coverage of random test suite
    tester.TestRandomPrioritizationBranchBased()


    print("\n-----------------------------6. BUILDING TOTAL TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    # Experiment 4 - Build Total Test Prioritization Suite
    totalTests = tester.TotalCoveragePrioritizationStatementBased()


    # Experiment 5 - Test Quality of suite for statement coverage of total test suite
    print("\n-----------------------------7. TESTING TOTAL TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    tester.TestTotalTestPrioritizationStatementBased() 


    print("\n-----------------------------8. BUILDING TOTAL TEST SUITE FOR BRANCH COVERAGE--------------------------------------\n")
    totalTests = tester.TotalCoveragePrioritizationBranchBased()


    # # Experiment 5 - Test Quality of suite for statement coverage of total test suite
    print("\n-----------------------------9. TESTING TOTAL TEST SUITE FOR BRANCH COVERAGE--------------------------------------\n")
    tester.TestTotalTestPrioritizationBranchBased() 


    print("\n-----------------------------10. BUILDING ADDITIONAL TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    addTests = tester.AdditionalCoveragePrioritizationStatementBased()


    # # Experiment 5 - Test Quality of suite for statement coverage of total test suite
    print("\n-----------------------------11. TESTING ADDITIONAL TEST SUITE FOR STATEMENT COVERAGE--------------------------------------\n")
    tester.TestAdditionalTestPrioritizationStatementBased() 


    print("\n-----------------------------12. BUILDING ADDITIONAL TEST SUITE FOR BRANCH COVERAGE--------------------------------------\n")
    addTests = tester.AdditionalCoveragePrioritizationBranchBased()

    print("\n-----------------------------13. TESTING ADDITIONAL TEST SUITE FOR BRANCH COVERAGE--------------------------------------\n")
    # # Experiment 5 - Test Quality of suite for statement coverage of total test suite
    tester.TestAdditionalTestPrioritizationBranchBased() 

    # Experiment 6 - Evaluate the fault detection capability of the test suite
    # Options as follows:
    #     "base" - the base test suite
    #     "RandomTestPrioritizationStatementBased" - the statement-based random test suite
    #     "TotalCoveragePrioritizationStatementBased" - the statement-based total test suite
    #     "AdditionalCoveragePrioritizationStatementBased" - the statement-based additional test suite
    #     "RandomTestPrioritizationBranchBased" - the branch-based random test suite
    #     "TotalCoveragePrioritizationBranchBased" - the branch-based total test suite
    #     "AdditionalCoveragePrioritizationBranchBased" - the branch-based additional test suite

    testSuiteNames = ["base", "RandomTestPrioritizationStatementBased", "TotalCoveragePrioritizationStatementBased", "AdditionalCoveragePrioritizationStatementBased", "RandomTestPrioritizationBranchBased", "TotalCoveragePrioritizationBranchBased", "AdditionalCoveragePrioritizationBranchBased"]
    print("\n-----------------------------14. EVALUATING FAULT DETECTION CAPABILITY OF ALL TEST SUITES--------------------------------------\n")
    for name in testSuiteNames:
        print("\t\n-------------------EVALUATING FAULT DETECTION CAPABILITY OF " + name.upper() + "-------------------\n")
       
        faultMp = tester.evaluateFaultDetectionCapability(name)

    tester.cleanUpBetweenRuns()

    print("\n----------------END OF EXPERIMENT - Check scripts/tcas for all the dumped coverage info and faults detected per testsuite---------------\n")
