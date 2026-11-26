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

    