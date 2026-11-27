# L00205876_DevopsInAction_MiniPipeline
Demo Pipeline for Task3


This repo will be used to demonstrate a small DevOps Pipeline.

I have written a Python Script which reads and Excel File.
The Excel File lists vegetables and their quanties.

The python file lists the items and their quantities.
It asks users if they would like to buy or sell veg.
When a user buys a vegetable, the quantity is depleted and the excel workbook is updated.

When a user sells a vegetable, they can add a vegetable not listed.
A default value of 0 is created and the excel workbook is updated with the new item and 0.
When the user enters a quantity, the workbook is updated.
If a user chooses to sell an item already listed, the workbook is updated.

I have manually tested the contingencies.

I now need to create a java app which I have not done before, before I can run the build in Maven.

My overall goal is to deploy the code to website where users can buy and sell vegetables based on the quantity in stock.
Prior to this I would have manually created everything in AWS, hoped it worked.

Code - Build - Test - Release > Python, Java - Maven - JUnit, JaCoCo, SonarCube, Docker, AWS ECR
Having worked through the individual steps I realised I could not deploy my original python script and excel to an ec2 instance with the Java application so I needed to go back and change my Java app.
This was after I allowed my workflows to access the ECR using using AWS IAM and OIDC authentication.
As I has missed my assignment deadline, I took a less panicked approach to testing and got JaCoCo and SonarCube working - although security and code coverage could be improved. I did demonstrate some small improvements in coverage

The beauty of the pipeline is that it is easy to work back. I checked my docker file and double checked my AWS stacks did not reference the old java app.
I could have not re-named the app but I think re-naming it was a good way showing dependencies.
I also added a git ignore as I had not realised that every time I ran a Maven build locally, it updated the files in the target folder which are not needed for future builds.

This experience demonstrated that successful individual pipeline stages do not necessarily guarantee that the overall application is ready for deployment. It also highlighted the value of version control, automated testing and repeatable builds when changes are required.

I sucessfully deployed a Cloudformations stack using Infrasture as code and I demonstrated the instance stopped after 23:59.
Unfortunately the Java is not displaying what I want,
Then, possibly because it is late, my VS Code glitched and I messed up my branch commits with an onerous git ignore.
I use my Google Drive for my college work and laptop is old but a Google tip suggested I pause syncing when using GitHub. I suspect there may be a clash between GitHub changes and Google Drive searcging for changes even when it is not syncing.

I was unable to automate Deploymnent to EC2 using this pipeline structure. I have decided to restart with my original python code and look at more suitable tools. Trying to convert it to Java just to use Maven was not a good idea.

I created a new Pipeline in Jenkins and configured this repository. I added a test script to see if Jenkins could read the JenkinsFile.

BUILD:
I installed Flask for Python on my local machine.
This will enable to users to ineract with the Butters Veg application through a web browser.
I added a requirements file which shows application Python dependencies. This will suppor consistent, reproducible builds across environments.


CODE:
After installing Flask, I modified my original code to allow user interaction on the web page.
I used PyTest to test bugs and coverage and I saved the results in the evidence folder. I also recorded an MP4 of the website working as expected on my local browser.
    1. A user can buy a vegetable listed and select a quantity
        A user cannot order more than the maximum quatity listed
        Zero quantity items show in stock but are not available to the user in the dropdown
        If a user orders more than 30units a prompt appears for the action to be confirmed or they can go back
    2. A user can sell a vegetable listed and add a quantity
        A user can add quantity they choose but they will be asked to confirm quantity if they add over 30units
    3. A user can sell an item not listed by selecting "Item not listed - Add new"
         Current Stock list will update with the new vegetable and quantity
         If a user adds an existing vegetable, the quantity in stock will increase but the Vegetable will not duplicate
         If a user tries to add symbols or numbers to the vegetable name they will be unable to add a quantity and complete their entry.
         If a user adds a decimal value to quantity they will be prompted to add a value greater than or equal to 1
            Letters are not permitted in this field.

BUILD:
I added the tests from PyTest to requirements and updated my JenkinsFile.
When I ran the build in Jenkins the Debugging test ran as per VSCode  the was 100%. As I had added Flash to the Python file for the HTML integration the test coverage had depleted as expected.
    
Tests:
In VSCode I added additional tests to the file test_Code_ButtersVegApp.py and ran the PyTests again. Coverage increased to 95%.

Security:
Static Code Analysis with SonarQube
I want to use SonarQube to identify code quality issues and potential security vulnerabilities.
    In SonarQube I created a local project called ButtersVeg and generated a project-specific analysis token
    In Jenkins I installed the SonarQube plugin to integrate the two tools
    I stored the SonarQube token as a secret text in Jenkins Credentials - no exposure in GitHub or Google Drive
    In Jenkins I configured http://localhost:9000 for the SonarQube Server connection and the automatic installation of the SonarQube Scanner latest version 8.5.0.16571

Security and Automated Pipeline Integration

SonarQube was successfully integrated into the Jenkins pipeline following the automated build and testing stages.
A `sonar-project.properties` configuration file was created to define the application source code, test directory, coverage report location and Quality Gate requirements.
Jenkins automatically executes the SonarQube Scanner, uploads the analysis results to the SonarQube server and waits for the Quality Gate result before allowing the pipeline to progress.

    Initial Static Analysis Results
    | Metric | Result |
    |---|---|
    | Jenkins execution | SUCCESS |
    | Quality Gate | PASSED |
    | Code coverage | 98.8% |
    | Code duplication | 0.0% |
    | Reliability | A |
    | Maintainability | A |
    | Security | D |
    | Security issues | 1 – High severity |
    | Security hotspots | 0 |

Security Issue Identified
 - SonarQube identified a high-severity security issue relating to Cross-Site Request Forgery (CSRF) protection within the Flask application.
 - This demonstrates the value of incorporating automated static analysis into the CI/CD pipeline, as the application passed all 30 automated tests but still contained a      potential security weakness.
 - The Quality Gate passed despite the identified security issue. This highlights the importance of reviewing Quality Gate conditions rather than relying solely on a         successful pipeline execution.

Analysis Warning
 - SonarQube issued a warning relating to Python version compatibility. The default analysis covers Python versions 3.10 to 3.14, whereas the current Jenkins build            environment uses Python 3.15.2.
 - The warning did not prevent successful analysis. Explicit Python version configuration will be considered once scanner compatibility has been confirmed.

Further Security Improvements
- Implement CSRF protection.
- Update automated integration tests to accommodate CSRF protection.
- Review and strengthen Quality Gate conditions.
- Introduce dependency vulnerability scanning.
- Demonstrate that security failures prevent further pipeline progression.

Screenshots of the successful Jenkins execution, SonarQube analysis results and identified security issue are retained in the Evidence directory.

Security Remediation – CSRF Protection

The initial SonarQube analysis identified a high-severity security issue relating to Cross-Site Request Forgery (CSRF), resulting in a security rating of D.
The following corrective measures were implemented:
- I integrated Flask-WTF to enable CSRF protection.
- Then added a CSRF token to the website transaction form.
- I generated a secure secret key and stored it within Jenkins Credentials rather than hardcoding it in the application or committing it to GitHub.
- I Restricted access to the secret key to the automated testing stage, following the principle of least privilege.
- I Updated the existing integration tests to accommodate CSRF protection.
- Then added three automated security tests to verify that missing and invalid tokens are rejected without modifying stock and that valid transactions are accepted.

Results – 27 November 2026
| Metric | Result |
|---|---|
| Automated tests | 33/33 passed |
| Test execution time | 3.57 seconds |
| Pytest statement coverage | 99% |
| SonarQube overall coverage | 98.9% |
| New code coverage | 100% |
| Security rating | Improved from D to A |
| Reliability rating | A |
| Maintainability rating | A |
| Open issues | 0 |
| Code duplication | 0.0% |
| Security hotspots | 0 |

The subsequent SonarQube analysis confirmed that the identified security issue had been resolved. All existing functional tests and the additional security tests passed, demonstrating successful remediation without introducing functional regressions.

Further demonstrates the importance of integrating static analysis, security remediation and automated regression testing into the CI/CD pipeline.

TODO: Invetsigate dependency vulmerability with Python Version
