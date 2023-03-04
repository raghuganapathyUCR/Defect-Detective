import os
import json
import csv
import gzip
import time
class TCASTESTER:
    def __init__(self) -> None:
        self.path = "../../benchmarks/tcas/"
    
    # function to read a file line by line
    def readFile(self, fileName):
        print("TCASTESTER: readFile")
        file = open(fileName, "r")
        lines = file.readlines()
        file.close()
        return lines
    

    

    def runForBase(self):
        print("TCASTESTER: runForBase")
        
       
        

        with open(f'{self.path}universe.txt', 'r') as f:
            testcases = f.readlines()

        # Create a list to store the coverage information for each testcase
        coverage_info = []


        # create a CSV
        # with open('coverage_info.csv', 'w', newline='') as csvfile:
        #         writer = csv.writer(csvfile)
        #         writer.writerow(['Testcase', 'Coverage'])

        # Loop through each testcase and run it
        for i, testcase in enumerate(testcases):
          
            if i> 0:
                break

            temp = os.system("gcc-12 -Wno-return-type -fprofile-arcs -ftest-coverage -w -g -o tcas "+ self.path + "tcas.c > /dev/null 2>&1")
            if temp != 0:
                print("TCASTESTER: runForBase: error in compiling")
                return
            print("TCASTESTER: runForBase: compiled")


            # Remove any whitespace from the beginning and end of the testcase
            testcase = testcase.strip()

            print(f"Running testcase {i+1}... ", testcase)
            # Run the testcase and save the coverage information to a file
            os.system(f'./tcas {testcase} > /dev/null 2>&1')

            # Run gcov on the output binary
            os.system(f'gcov-12 -a -w -b -f -j tcas')


            coverageInfo = {}

            # Read the gcov output file
            with gzip.open('tcas.gcov.json.gz', 'rb') as f:
                json_bytes = f.read()                     
                json_str = json_bytes.decode('utf-8')            
                json_data = json.loads(json_str)     


                # For Coverage Ratio - Block Coverage
                lines = json_data['files'][0]['lines']
                covered_lines = [line for line in lines if line['count'] > 0]
                total_lines = len(lines)
                covered_ratio = len(covered_lines) / total_lines

                #
                coverageInfo["blockCoverage"] = covered_ratio

                # To do the additional Coverage part
                mp = {
                    "visited" : [],
                    "notVisited" : []
                }
                total_branches = 0
                taken_branches = 0
                for line in lines:
                    if line["count"] > 0:
                        mp["visited"].append(line["line_number"])
                    else:
                        mp["notVisited"].append(line["line_number"])
                    
                    if "branches" in line:
                        # Loop through each branch in the line
                        for branch in line["branches"]:
                            # Increment the total number of branches
                            total_branches += 1
                            # If the branch was taken, increment the taken branches
                            if branch["count"] > 0:
                                taken_branches += 1
                if total_branches > 0:
                    branch_coverage = (taken_branches / total_branches) * 100
                else:
                    branch_coverage = 0.0

                coverageInfo["lines"] = mp
                print("Branch coverage: {:.2f}%".format(branch_coverage))
                # Per-Function Coverage
                fnMp = {}
                for function in json_data['files'][0]['functions']:

                    fnBlockCoverage = function["blocks_executed"] / function["blocks"] 
                    fnMp[function["name"]] = fnBlockCoverage
                    # print("\t",function)
                coverageInfo["functionData"] = fnMp




                print(coverageInfo)
            os.system(f'rm -rf tcas.gcno')
            os.system(f'rm -rf tcas')
            os.system(f'rm -rf ./tcas.dSYM')
            os.system(f'rm -rf ./tcas.gcda')
            os.system(f'rm -rf tcas.gcov.json.gz') 

                # Append the coverage information to the list
                # coverage_info.append((i+1, covered_ratio))
                
        
        # with open('coverage_info.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerows(coverage_info)
        

if __name__ == "__main__":
    print("TCASTESTER: main")
    tester = TCASTESTER()
    tester.runForBase()