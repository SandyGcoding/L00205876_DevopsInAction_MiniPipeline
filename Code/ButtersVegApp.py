#ButtersVegApp

from openpyxl import load_workbook
from threading import Lock

#Create web application, display HTML Template, receive customer information entered
from flask import Flask, render_template, request
app = Flask(__name__)

# Prevent simultaneous stock updates
StockLock = Lock()

#TODO: Replace terminal input with Flask request.form when webpage is created
#action = input("\nWould you like to Buy or Sell vegetables? Enter Buy, Sell , Exit  >>>  ")

#Create Function for retrieval of stock in Veg.xlsx by Flask
def LoadStock():
    workbook = load_workbook ("Veg.xlsx")
    sheet = workbook.active
    
    vegetable = {}
      
    for veg, quantity in sheet.iter_rows(
        min_row=2, min_col=1, max_col=2, values_only=True
    ):
        if veg is not None:
            vegetable[veg] = quantity
            print(f"{veg}:{quantity}")

    workbook.close()
    return vegetable 

#Create seperate function for "Buy"
def BuyVeg(BVeg, BQuantity):
    vegetable = LoadStock()
    
    # Validate quantity before processing the order
    # TODO Add pop-up in HTML for user confirmation if Quantity entered > 30
    if not isinstance(BQuantity, int) or BQuantity <= 0:
        return "Please enter a valid positive whole number."
    
        # Retain server-side validation despite HTML dropdown restrictions
    if BVeg not in vegetable:
        return "This item is not listed."
    else:
        #Recheck stock in case another customer has made a purchase and system has not updated
        available = vegetable[BVeg]
        if BQuantity > available:
            return f"Only {available} available."
        else:
            #print(f"Thank you for purchasing {BQuantity} {BVeg}.")
            vegetable[BVeg] -= BQuantity
            #Deplete Stock quantity in Excel and save
            workbook = load_workbook("Veg.xlsx")
            sheet = workbook.active

            for row in range(2, sheet.max_row + 1):
                if sheet.cell(row=row, column=1).value == BVeg:
                    sheet.cell(row=row, column=2).value = vegetable[BVeg]
                    break
                
            workbook.save("Veg.xlsx")
            workbook.close()
            return f"Thank you for ordering {BQuantity} {BVeg}. \nPlease call us to arrange delivery"
  
#Create seperate function for "Sell"
def SellVeg(SVeg, SQuantity):
    vegetable = LoadStock()
    
    # Validate quantity before updating stock
    # TODO Add pop-up in HTML for user confirmation if Quantity entered > 30
    if not isinstance(SQuantity, int) or SQuantity <= 0:
        return "Please enter a valid positive whole number."


    # The HTML dropdown will include "Item not listed - Add new".
    # Selecting this option will display a text field for the vegetable name and a numeric field for the quantity.
    # Flask will pass these values to SellVeg().
    if SVeg not in vegetable:
        vegetable[SVeg] = SQuantity
        
        # Add new vegetable to Excel
        workbook = load_workbook("Veg.xlsx")
        sheet = workbook.active
        sheet.append([SVeg, SQuantity])
        workbook.save("Veg.xlsx")
        workbook.close()

        return f"Thank you. {SQuantity} {SVeg} added to stock. Please call us to arrange collection."
        
    else:
        # Increase stock quantity for an existing vegetable
        vegetable[SVeg] += SQuantity

        # Update existing vegetable quantity in Excel
        workbook = load_workbook("Veg.xlsx")
        sheet = workbook.active

        for row in range(2, sheet.max_row + 1):
            if sheet.cell(row=row, column=1).value == SVeg:
                sheet.cell(row=row, column=2).value = vegetable[SVeg]
                break

        workbook.save("Veg.xlsx")
        workbook.close()

        return f"Thank you. Stock quantity for {SVeg} has been updated to {vegetable[SVeg]}.\nPlease call us to arrange collection."

