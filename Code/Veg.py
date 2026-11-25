#Test Python

from openpyxl import load_workbook

workbook = load_workbook ("Veg.xlsx")

sheet = workbook.active

for row in sheet.iter_rows(min_col=1, max_col=2, values_only=True):
   
    vegetable = {}

    for veg, quantity in sheet.iter_rows(
        min_row=2, min_col=1, max_col=2, values_only=True
        ):
        if vegetable is not None:
            vegetable[veg] = quantity
print(vegetable)   

action = input("\nWould you like to Buy or Sell vegetables? > Enter Buy, Sell , Exit  >>>  ")

if action.strip().lower() == "buy":
    BVeg = input("\nWhich vegetable would you like to buy? ").strip().capitalize()

    if BVeg not in vegetable:
        print("\nThis item is not listed.")
    else:
        available = vegetable[BVeg]
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
           





