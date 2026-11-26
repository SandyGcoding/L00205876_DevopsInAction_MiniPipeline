#ButtersVegApp

from openpyxl import load_workbook

#Create web application, display HTML Template, receive customer information entered
from flask import Flask, render_template, request
app = Flask(__name__)


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
    #Retain validation even though website will have dropdown. Two customers may try to make a purchase at once
    if BVeg not in vegetable:
        return "This item is not listed.")
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

#TODO: Replace terminal input with Flask request.form when webpage is created
action = input("\nWould you like to Buy or Sell vegetables? Enter Buy, Sell , Exit  >>>  ")

if action.strip().lower() == "buy":
    BVeg = input("\nWhich vegetable would you like to buy? ").strip().capitalize()


        BQuantity = int(input("\nPlease enter quantity: "))

        if BQuantity > available:
            print(f"\nOnly {available} available.")
        else:
            print(f"Thank you for purchasing {BQuantity} {BVeg}.")
            vegetable[BVeg] -= BQuantity
            for row in range(2, sheet.max_row + 1):
                if sheet.cell(row=row, column=1).value == BVeg:
                   sheet.cell(row=row, column=2).value = vegetable[BVeg]
                   workbook.save("Veg.xlsx")
                   print(vegetable)
                   raise SystemExit("Exiting program.")
elif action.strip().lower() == "sell":
    SVeg = input("\nWhich vegetables would you like to sell? ").strip().capitalize()
    if SVeg not in vegetable:
        add_veg = input(f"{SVeg} are not listed. Would you like to add {SVeg}? >>> (y/n) ")
        if add_veg.strip().lower() == "y":
            vegetable[SVeg] = 0
            sheet.append([SVeg, vegetable[SVeg]])
            workbook.save("Veg.xlsx")
            print(f"{SVeg} has been added to the list.")
            SQuantity = int(input("Please enter a quantity: "))
            vegetable[SVeg] += SQuantity
            print(f"{SVeg} in stock is now {vegetable[SVeg]}.")
            sheet.cell(row=sheet.max_row, column=2).value = vegetable[SVeg]
            workbook.save("Veg.xlsx")
            print(vegetable)
            raise SystemExit("Exiting program.")
        else:
            raise SystemExit("Exiting program.")
    elif SVeg in vegetable:
        SQuantity = int(input("Please enter a quantity: "))
        vegetable[SVeg] += SQuantity
        print(f"{SVeg} in stock is now {vegetable[SVeg]}.")
        for row in range(2, sheet.max_row + 1):
            if sheet.cell(row=row, column=1).value == SVeg:
                sheet.cell(row=row, column=2).value = vegetable[SVeg]
                workbook.save("Veg.xlsx")
                print(vegetable)
                raise SystemExit("Exiting program.")
else:
    raise SystemExit("Exiting program.")        
           





