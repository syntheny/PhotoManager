# Photo Collector
* Started July 10, 2023
* Updated July 10, 2023

----

## Summary
The Photo Collector is an application program that searches for photo and video files under specific paths, collects image files, and stores the unique files in a "collections" folder. The Collector function is a part of a "Photo Manager" utility that further processes the collected files. As development of other parts of the PhotoManager evolve, those parts may be incorporated into a single application, but that is yet to be determined.

----

## Background
In my environment, I have photo and video files scattered in various systems and media. Often, that scattering is more of a redistribution of files from one form to another, without deletion of the source files. For example, Files are uploaded from a camera SD card to a PC storage, some files may be duplicated for whatever reason without change and placed in other folders, then folders of files are automatically uploaded to the cloud (Google photo storage or Apple cloud)--later, those cloud files are brought back to earth in another PC folder. Thus, a file can be found on many folders on several PCs.

Another wrinkle in the scattering of photos is that many have been placed into folders named for a date and/or a activity.

----

## Essential Requirements
The goal of this project is to locate the files on PCs. This program is merely a collector--it is not intended for the program to delete any files. Several lists are to be generated which will be used by the next program in the Photo Manager utility:
* A list of all files, with full paths, that are unique. Other critical information regarding the files may be retained in the list.
* A list of all files, with full paths, that are duplicates of unique files.

Other mandatory requirements are:
* By default, JPG, PNG, JPEG, MP4, and MOV files are to be processed. An option should be available to select specific types.
* Files may be found in archives, such as ZIP or 7Z type files.
* Duplication of a file is identified as two or more files having identical content, regardless of containing folder names, file names, or file timestamps.
* Information is to be collected once. Examples:
    - If a file is read to check for duplication, a hash value should be retained so that tha file does not need to be reread to check again for duplication.
    - If EXIF information is required, it is read once, preferrably from the same data block read to obtain hash value, and retained.
* When the program is rerun, the same lists as collected before are updated with newly found files. An option is required to start with a fresh collection.

----

## Development Approach
The development of the Photo Collector program ("COL") will be performed in stages, where each stage generally follows a process listed below. Since only one person is involved, some typical concepts of Agile may not be followed precisely.
* Specification of the stage requirements and detailed design
* Test-driven development
* Implementation of the stage
* Archival of source to github

----

## Requirements Analysis
* Requirements derived from essential requirements
    - The program uses command line options and arguments for operation
    - A single folder is designated as the collection site
    - One or more paths must be specified on the command line as the source of files
    - Source paths may include references to remote file systems, through drive letter mapped to another computer or Universal Naming Convention (UNC)
    - A source path may include a date or activity indication. For examples:
        * C:\Pix\202110_
        * C:\FlashImage\Photos\MiscPhotos.zip\Hillsboro 09

* Presumed requirements and conditions
    - All operations are performed on a PC with a Windows OS. Linux operation is a possibility but not explored at this time.
    - Operations will be fast enough such that Python is adequate for the application.
    - The PC has sufficient memory to support large amount of file information.

----

## Stage 0 -- General Planning
* Each stage of development is expected to take only a few hours or a day, since only one person is doing all work.
* A TDD approach is used in testing stages of development.
* Development of source and tests is in Python
* Python "unittest" is used in test module and test case development
* The expectation is that only one test module is developed for the testing of the PhotoCollector program; each stage adds test cases.
* The test module will setup its testing environment from scratch (i.e., no reliance on previous setup).
* A github repository is used to hold developed sources: https://github.com/syntheny/PhotoManager
* The end of each stage will assure the source and tests are committed to the repository, using the "Stage_number_stage_title" as the branch name.
* Stages as expected at kick-off:
    1. Handling PhotoCollector as both a library and program
    2. Command line parsing for path argument
    3. Finding files
    4. Collecting file information
    5. Identifying duplicate files
* The general format of each stage description is as follows (empty sections can be omitted):
    ```
    ## Stage N -- title
    * Stage description/summary points
    ### Stage Preparation
    * Specify any instructions with respect to development, such as
      one-time-only generation of test data which is added to the repository.
    ### Test Setup
    * Itemized list of what needs to be set up for the stage
    * Note that a stage is an addition of test cases to existing
      test cases from previous stages, so setup can be additive.
    ### Test Cases
    * Itemized test cases
        - For each test case, indicate the expected result,
          unless it is obvious
    * Note that Python unittest will reorder test cases, based on name,
      so a test case cannot rely on another test case behaviour.
    ### Test Teardown
    * Clean up interim states
    * But do not remove artifacts from testing that might help in
      diagnosing problems
    ### Test Results
    * Do not actually add test results here, but use this markdown link, keyed to the stage number:
        [Stage N Test Results](TestResults/stageN.md)
    * Create a "stageN.md" text file under TestResults folder to report testing results for stage N
    ### Changes During Implementation
    * Changes to the stage plan required during implementation of SW or test.
    * Highlight any discoveries that affect usage, using the block quote of note or warning, for example:
    
    > **NOTE** text
    ```
* When a test/development stage is complete, create a separate reporting file, with the stage number in the name, under "TestResults" folder in the repository. This file and related files generated during testing should be included when the stage branch is checked in.
* Information to include in the rest results report file are:
    - Report approximate time to develop and test this stage
    - Report any note-worthy results from succcessful testing
    - Keep any test reports of intermittent failure (also report through Jira)

----

## Stage 1 -- Structure of PhotoCollector

### Design
* This stage allows the development of the PhotoCollector (COL) source structure on which all other test cases are based.
* This stage also allows the exploration of how to test COL, including setup of test environment that may be required for each stage.
* The COL module is expected to be both an import as a library and callable as a system program.
* What is expected is that a command line parsing scheme is developed (testing of the parsing is performed in another test stage).

### Test Cases
1. Import PhotoCollector library
2. Import PhotoCollector library and create instance of related object
3. Use Python subprocess call methods to invoke PhotoCollector as an application

----

## Stage 2 -- Common Folder Setup

### Design
* This stage simply creates some folders and copies files into them for subsequent stage tests.
* Two classes are defined: a non-test common class and a test class
    - The common class is to be included in all subsequent test classes and provides the setup of the testing environment
    - The test class validates the construction of the test environment
* The "classSetUp" method of each test class is expected to call a common function to assure the test environment is configured.
* The test source files are found in the "TestData" folder under the program path

### Common Class
* Inherits from unittest.TestCase, allowing all other test classes to base on both this common class and TestCase
* Create folders and copy existing files from testData into folders, as directed below:
    1. Folder C:\Photo\Tests\test_folder0 -- empty
    2. Folder C:\Photo\Tests\test_folder1 -- contains one file with ".txt" extension
    3. Folder C:\Photo\Tests\test_folder2 -- contains one file with ".jpg" suffix
    4. Folder C:\Photo\Tests\test_folder3 -- contains multiple files with all supported extensions
    5. Folder C:\Photo\Tests\test_folder4 -- contains multiple files with all supported extensions; also contains a folder "subfolder" having multiple files of all supported extensions
* A library could be used to create the temporary directory, but that may lose the path characteristics (i.e., Windows file system) that needs to be tested.

### Test Class
* Verify all folders are created
* Verify expected content of folders

----

## Stage 3 -- Finding Files

### Test Design: TestCollection Class
* This stage is not concerned with command line options; instead, it uses the canned paths from the common setup.
* It tests the ability of the program to locate photo files in one or more existing folders, including nested folders.
* This stage is not concerned with file content, only the file extension as it indicates an image or video file.

### SW Design
* This stage requires specification of the "collect" function:
    - Input: one or more input directory paths
    - Output: List of found photo files and their paths
    - Function:
        * Examine each directory path, and any subordinate folders, for photo files
        * Save to an internal dictionary, with file name as the key for each entry, and the full path as the value.
        * Need not filter for duplicates or any other attributes, except the image type

### Test Cases
1. Using collect function, search the empty folder; expect an empty list
2. Search nonphoto folder; expect an empty list
3. Search photo folder; expect a list of one file
4. Search many photo folder; expect a list of multiple entries
5. Search deep folder; expect a list of multiple entries, some with subfolder paths

### Changes During Implementation
1. Discovered that the Common Class is not so common. Each test class has a new instantiation of the common. Will need to use an external instance for the common, and the class setup for a test class will perform a deep copy of the common class members.
2. Tests run under PyCharm, Windows CMD shell, and WSL bash shell. Some fix-ups were required for WSL shell.
3. Running under bash shell may require using *sudo* since file attributes are being changed and the files are set to root ownership. A particular WSL configuration may not be configured to permit non-root access (I have not found a successful solution, yet).

> **WARNING** Under WSL, **sudo** may be required to run the test program and the collection program if the user does not have root-level file write permission.

----

## Stage 4 -- Shared Python library files
* Some source files used in the project are library modules managed under other repositories, specifically the "tools.py" module is maintained in the Tools repo.
* However, the tools.py file also needs to be included into this project repository so that its current state can be committed to the project repository.
* git provides a submodule concept, but during development with frequent and numerous changes to all sources, including the tools.py file, using git is problematic and error-prone.
* An alterative is to add the Tools repo path to the PYTHONPATH environment variable so that the Tools.py file can be found in the original Tools repo. But that still presents the problem of tools.py not being included in the project repository when committed.
* The change is within tools.py itself--no other module needs to be modified to handle the tools.py update and synchronization. When the tools module is imported, it will immediately import a "sync_modules" module.
* The sync_modules is small and only has the purpose of synchronizing modules associated with tools.py.
* A class called "Sync" in the sync_modules performs these steps during instantiation on both tools.py and sync_modules.py (itself):
    - Get size and modification dates from the module source file in both repos
    - If not a mismatch, the Sync instantiation ends with no other action
    - The newer file is copied to the other repo
    - The module is deleted from sys.modules to allow a new version to be re-imported
* There is no test case for this stage since it is tested through the importing of test.py.

----
## Stage 5 -- Extract Zip Files

### Test Design: TestZipExtraction
* Most image files are bound up in zip files (7zip, zip, and other formats)
* The test cases will use zip files, found in the TestData folder
* Each zip is passed to the collect function which is expected to recognize the file type and perform the zip extraction
* The files are extracted to a temporary folder, with path specified by the test facility
* Testing will examine the temp folder(s) and compare to the extracted image files names
* To prepare:
    - Copy some existing image files and non-image files in TestData and rename them to avoid naming conflicts
    - Add those files to a 7zip (7z) archive file, leaving in the TestData folder
    - Rename the files again to other unique names
    - Add those files to a zip file using a different encoding, leaving in the TestData folder
    - Repeat renaming files and add to a gzip file (using gzip in Linux)
* A Python script is created to methodically perform the creation of the zip files.
* These test cases should be developed with unique test case methods as separate steps in the test case specification below.

### SW Design
1. The "collect" function interface is expanded to handle zip files
2. A collected file is marked as being found in a particular archive file

### Test Cases
1. Search TestData for zip files
2. Invoke the collect function using a specific archive file, with these steps:
    - Specify the archive file, such as 7zip file
    - Specify the test output folder as the extraction target
    - Specify the a file extension, such as non-image
    - After the collect call, examine the output folder for expected files
3. Repeat step 2 with all image file types
4. Repeat step 2 with a file type that is known not to be present; expect no file in collection list
5. Repeat steps 2-4 with a zip file
6. Repeat steps 2-4 with other archive files
7. Invoke the collect against the TestData source folder to search for image files and zip files, with the expectation that all image files are found, including those held by archives.

----
## Stage 5 -- Explore Disk Volume

### Test Design: TestExploreVolumes
* The presumed volume is C:, but searching for image files over a volume of 1M+ files would be time-consuming; a limited set of folders will be specified which will still have many thousands of files to browse.
* This test phase needs to examine the time element. If too long to scan for image files, an alternate method may be needed; on the other hand, the collection may be slow, but acceptable.

----

## Stage X -- Command line
* Command line work is delayed until the functional portions of the program are completed so that options may be determined then.
* There may be the need to a "run command" file (i.e., a run-time configuration file which provides non-explicit options).
