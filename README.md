## Defect Detective
##

Raghu Ganapathy |  rgana001@ucr.edu


### Project File Structure
```
root
|___benchmarks - Benchmark programs as universe of
	|			 testcases.
	|___printtokens	
	|___printtokens2
	|___schedule
	|___schedule2
	|___tcas
	|___totinfo	
	|___replace		 
|___scripts - Per-benchmark experiments and generated test
			  suites.
	|___printtokens
		|___printtokensTester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
	|___printtokens2
		|___printtokens2Tester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
	|___schedule
		|___scheduleTester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
	|___schedule2
		|___schedule2Tester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
	|___tcas
		|___tcasTester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
	|___totinfo
		|___totinfoTester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
	|___replace
		|___totinfoTester.py
		|___random-statement-suite.txt
		|___total-statement-suite.txt
		|___additional-statement-suite.txt
		|___random-branch-suite.txt	
		|___total-branch-suite.txt
		|___additional-branch-suite.txt
|___gitignore 
|___name.txt - Names of Project Teammates.
|___README.md	 
```
### Notes on the project file structure - 
1. The test suites are generated and evaluated for each benchmark in it's associated "tester.py", which can be found inside the scripts directory.
2. The test suites generated for each benchmark program are placed in the same directory as the associated "tester" file.
Ex - "Statement Coverage based Total Test Prioritization Test Suite"  for tcas can be found in root/scripts/tcas as file "total-statement-suite.txt"

### Steps to run the tester files - 
 - Clone the repository and cd into the scripts directory 
	```bash
		cd scripts 
	```
 - Cd into the benchmark that you intend to run
	ex - for totinfo
	```bash
		cd totinfo 
	```
 - Run the tester using the following command ```python3 <benchmark>Tester.py```
	```bash
		python3 totinfoTester.py
	```
### General Notes
 - No additional packages are required to run, as the entire project is implemented using only the packages available in standard python library.
 - I have't committed any static files (apart from the required test suites), but the testers create static files to speed subsequent runs. _Please keep these files if the tester is going to be run more than once, as it will help run the tester files faster_. 
 - All the faults found for each test suite get dumped to the same folder as their associated tester, in json format. This is done to help us in generating the report.
