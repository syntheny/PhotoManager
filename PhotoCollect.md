# Photo Collector
* Started July 10, 2023
* Updated July 10, 2023

## Summary
The Photo Collector is an application program that searches for photo and video files under specific paths, collects image files, and stores the unique files in a "collections" folder. The Collector function is a part of a "Photo Manager" utility that further processes the collected files. As development of other parts of the PhotoManager evolve, those parts may be incorporated into a single application, but that is yet to be determined. 
## Background
In my environment, I have photo and video files scattered in various systems and media. Often, that scattering is more of a redistribution of files from one form to another, without deletion of the source files. For example, Files are uploaded from a camera SD card to a PC storage, some files may be duplicated for whatever reason without change and placed in other folders, then folders of files are automatically uploaded to the cloud (Google photo storage or Apple cloud)--later, those cloud files are brought back to earth in another PC folder. Thus, a file can be found on many folders on several PCs.

Another wrinkle in the scattering of photos is that many have been placed into folders named for a date and/or a activity. 

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

## Development Approach
The development of the Photo Collector program ("COL") will be performed in stages, where each stage generally follows a process listed below. Since only one person is involved, some typical concepts of Agile may not be followed precisely.
* Specification of the stage requirements and detailed design
* Test-driven development
* Implementation of the stage
* Archival of source to github

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
        * Report approximate time to develop and test this stage
        * Report any note-worthy results from succcessful testing
        * Keep any test reports of intermittent failure (also report through Jira)
```

## Stage 1 -- Structure of PhotoCollector
* This stage allows the development of the PhotoCollector (COL) source structure on which all other test cases are based.
* This stage also allows the exploration of how to test COL, including setup of test environment that may be required for each stage.
* The COL module is expected to be both an import as a library and callable as a system program.
* What is expected is that a command line parsing scheme is developed (testing of the parsing is performed in another test stage).

### Test Cases
1. Import PhotoCollector library
2. Import PhotoCollector library and create instance of related object
3. Use Python subprocess call methods to invoke PhotoCollector as an application

### Test Results
* Elapsed time: 30 minutes
* Created a class for this specific stage. Multiple test classes are envisioned to handle each stage.
* A common class "CommonTest" will inherit unittest.TestCase, and all other test classes will inherit CommonTest. This will permit definition of a common setUp method.
* Test run results:
```
        test_collector_import_class (__main__.TestCollectStructure.test_collector_import_class) ... ok
        test_collector_library (__main__.TestCollectStructure.test_collector_library) ... ok
        test_collector_program (__main__.TestCollectStructure.test_collector_program) ... ok
```

## Stage 2 -- Command line 
* This stage is not concerned with command line options, except one or more arguments to specify folder paths. 
* It tests the ability of the program to locate photo files in one or more existing folders, including nested folders. 
* This stage is not concerned with file content, only the file extension as it indicates an image or video file.

### Test Setup
* Create folders and copy existing files into folders, as directed below:
    1. Folder C:\Photo\Tests\test_folder0 -- empty
    2. Folder C:\Photo\Tests\test_folder1 -- contains one file with ".txt" extension
    3. Folder C:\Photo\Tests\test_folder2 -- contains one file with ".jpg" suffix
    4. Folder C:\Photo\Tests\test_folder3 -- contains multiple files with all supported extensions
    5. Folder C:\Photo\Tests\test_folder4 -- contains multiple files with all supported extensions; also contains a folder "subfolder" having multiple files of all supported extensions
* Each test case simulates the invocation of the PhotoCollector program by importing 
### Test Cases
* Command line: no arguments
    - expect in-and-out, no failure
* Command line: one valid folder path
* Command line: one invalid folder path
* Command line: one valid file path for existing file
* Command line: one invalid file path (non-existent file)
* Command line: multiple valid folder paths
* Command line: multiple valid folder and file paths
 
## Stage 3 -- Finding Files
### TDD Design
* This stage is not concerned with command line options, except one or more arguments to specify folder paths. 
* It tests the ability of the program to locate photo files in one or more existing folders, including nested folders. 
* This stage is not concerned with file content, only the file extension as it indicates an image or video file.
#### Test Setup
* Create folders and copy existing files into folders, as directed below:
    1. Folder C:\Photo\Tests\test_folder0 -- empty
    2. Folder C:\Photo\Tests\test_folder1 -- contains one file with ".txt" extension
    3. Folder C:\Photo\Tests\test_folder2 -- contains one file with ".jpg" suffix
    4. Folder C:\Photo\Tests\test_folder3 -- contains multiple files with all supported extensions
    5. Folder C:\Photo\Tests\test_folder4 -- contains multiple files with all supported extensions; also contains a folder "subfolder" having multiple files of all supported extensions

#### Test Cases
* Command line: no arguments
    - expect in-and-out, no failure
* Command line: one valid folder path
* Command line: one invalid folder path
* Command line: one valid file path for existing file
* Command line: one invalid file path (non-existent file)
* Command line: multiple valid folder paths
* Command line: multiple valid folder and file paths



