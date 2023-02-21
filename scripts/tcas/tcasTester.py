import os
import json
import csv
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
        
        temp = os.system("gcc-12 -Wno-return-type -fprofile-arcs -ftest-coverage -w -g -o tcas "+ self.path + "tcas.c")
        if temp != 0:
            print("TCASTESTER: runForBase: error in compiling")
            return
        print("TCASTESTER: runForBase: compiled")

        

        with open(f'{self.path}universe.txt', 'r') as f:
            testcases = f.readlines()

        # Create a list to store the coverage information for each testcase
        coverage_info = []

        # Loop through each testcase and run it
        for i, testcase in enumerate(testcases):
            # Remove any whitespace from the beginning and end of the testcase
            testcase = testcase.strip()

            print(f"Running testcase {i+1}... ", testcase)
            # Run the testcase and save the coverage information to a file
            os.system(f'./tcas {testcase} > outputs/output{i}.txt')
        #     os.system('gcov -j tcas.c')

        #     # Open the coverage file and extract the coverage information
        #     with open('tcas.c.gcov.json', 'r') as cov_file:
        #         coverage = cov_file.read()
        #         # Parse the JSON and extract the relevant coverage information
        #         json_data = json.loads(coverage)
        #         lines = json_data['files'][0]['lines']
        #         covered_lines = [line for line in lines if line['count'] > 0]
        #         total_lines = len(lines)
        #         covered_ratio = len(covered_lines) / total_lines
        #         # Append the coverage information to the list
        #         coverage_info.append((i+1, covered_ratio))

        # # Write the coverage information to a CSV file
        # with open('coverage_info.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['Testcase', 'Coverage'])
        #     writer.writerows(coverage_info)


if __name__ == "__main__":
    print("TCASTESTER: main")
    tester = TCASTESTER()
    tester.runForBase()