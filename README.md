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
