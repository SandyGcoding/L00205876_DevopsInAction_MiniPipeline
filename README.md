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
