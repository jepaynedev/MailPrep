**STATUS (May 2023):**

This project is unfinished and not maintained. After working at the UW Extension Bulk Mail Center, I had many ideas for how a lightweight and user-friendly destop application could assist in organizing the standard processes and files for each mail job. It was an interesting project for which I had relevant knowledge and served as a way to continue to develop Python skills I was not using in my main job at the time. Upon news that the mail center was being permanently closed, and a career change that limited my available time, this project was set aside.

There is no plan to ever finish this project, but I am retaining it as an example for my future reference, specifically regarding the following features:

- Organizing a Python project with multiple packages
- Logical seperation of GUI component using PySide2
- Use of Qt Designer application for visual layout design and a solution for generating files from the \*.ui definitions
- Testing with unittest and tox
- Setuptools for packaging, dependencies and entry points

# MailPrep

Application for University of Wisconsin - Madison Bulk Mail Center to automate processing bulk mailings. This involves properly formatting files, correcting formatting issues, and scripting integration with multiple instances of software provided by third-party vendors.

# Installation

To install, first clone the repository. I recommend creating a virtual environment to install dependencies, but that stop is options. Install locally using `pip install -e .` Then run `mailprep` to call the setuptools configured console script that will launch the GUI application.

# Job Definition File (.mpjob)

## Overview

Each mail job created with MailPrep is defined in a single file configuration file. The name of this file is the name of the mailing job that you enter when creating a new job. The extension is .mpjob (MailPrep job). The file is simply a YAML format configuration file, but instead of the traditional .yaml extension, they are defined with this application specific extension. This represents that the file contents should conform to a standard expected by the application. It additionally allows MailPrep to filter job open dialog windows to search for only \*.mpjob files (instead of any YAML file), and would allow functionality to be added to link the extension to the MailPrep application, allowing a job to be opened simply by double-clicking the .mpjob file on Windows operating systems.

The rational for moving job information to a flat file was to avoid using any complicated database storage. YAML format was picked as it is more human-readable and easier to modify than other considered options. This allows users to simply edit the .mpjob file by hand if desired instead of having to work through the application. As the official document specifications can be relatively dense, for more information on YAML and how to format it if manually editing, the [Wikipedia article on YAML](https://en.wikipedia.org/wiki/YAML) is a good overview containing basic information and examples.

When a new job is created, a new directory should be made to store all relevant documents. This job definition file **must** be located at the root level of this folder. All information, including required files, is defined in this document. Related files (e.g. input/output files, reports, images, etc) are located by default with relative paths originating from the location of this .mpjob file. If this file is not at the root level of the job directory, the application will not know where to find necessary documents to process the job.

## Format Definition

Will continue to be updated as the format is extended

```yaml
--- # Three dashes indicate the start of a new YAML document in the file
```
