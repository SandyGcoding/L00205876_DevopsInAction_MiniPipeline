# Automated testing for Butters Veg

import pytest
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor
from Code.ButtersVegApp import LoadStock, BuyVeg, SellVeg, app



# Create a temporary Excel workbook for each test
# This protects the original Veg.xlsx from changes
@pytest.fixture(autouse=True)
def TestWorkbook(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    workbook = Workbook()
    sheet = workbook.active

    sheet.append(["Vegetable", "Quantity"])
    sheet.append(["Potatoes", 8])
    sheet.append(["Carrots", 10])
    sheet.append(["Lettuce", 6])
    sheet.append(["Red Peppers", 5])

    workbook.save("Veg.xlsx")
    workbook.close()


# Test retrieval of stock
def test_LoadStock():
    vegetable = LoadStock()
    assert vegetable["Potatoes"] == 8
    assert vegetable["Lettuce"] == 6


# Test successful purchase
def test_BuyVeg():
    message = BuyVeg("Potatoes", 5)

    assert LoadStock()["Potatoes"] == 3
    assert "Thank you for ordering" in message


# Test purchase of all available stock
def test_BuyAllStock():
    BuyVeg("Potatoes", 8)

    assert LoadStock()["Potatoes"] == 0


# Test purchase exceeding available stock
def test_InsufficientStock():
    message = BuyVeg("Potatoes", 9)

    assert LoadStock()["Potatoes"] == 8
    assert "Only 8 available" in message


# Test purchase of an unlisted vegetable
def test_UnlistedVegetable():
    message = BuyVeg("Parsnips", 2)

    assert message == "This item is not listed."


# Test invalid purchase quantities
@pytest.mark.parametrize("Quantity", [0, -5, 2.5, "five"])
def test_InvalidBuyQuantity(Quantity):
    message = BuyVeg("Potatoes", Quantity)

    assert LoadStock()["Potatoes"] == 8
    assert "valid positive whole number" in message


# Test sale of an existing vegetable
def test_SellExistingVeg():
    message = SellVeg("Potatoes", 5)

    assert LoadStock()["Potatoes"] == 13
    assert "updated to 13" in message


# Test sale of a new vegetable
def test_SellNewVeg():
    message = SellVeg("Sweet Potato", 6)

    assert LoadStock()["Sweet Potato"] == 6
    assert "added to stock" in message


# Test standardisation of vegetable names
def test_VegetableNameFormatting():
    SellVeg("  red peppers  ", 3)

    assert LoadStock()["Red Peppers"] == 8


# Test invalid vegetable names
@pytest.mark.parametrize("Name", ["", "123", "Potato!", "   "])
def test_InvalidVegetableName(Name):
    OriginalStock = LoadStock()
    message = SellVeg(Name, 5)

    assert LoadStock() == OriginalStock
    assert "valid vegetable name" in message


# Test invalid sale quantities
@pytest.mark.parametrize("Quantity", [0, -5, 2.5, "five"])
def test_InvalidSellQuantity(Quantity):
    message = SellVeg("Potatoes", Quantity)

    assert LoadStock()["Potatoes"] == 8
    assert "valid positive whole number" in message


# Test two customers attempting to purchase limited stock
def test_ConcurrentPurchases():
    with ThreadPoolExecutor(max_workers=2) as executor:
        Customer1 = executor.submit(BuyVeg, "Potatoes", 5)
        Customer2 = executor.submit(BuyVeg, "Potatoes", 5)

        Results = [Customer1.result(), Customer2.result()]

    assert LoadStock()["Potatoes"] == 3
    assert sum("Thank you for ordering" in r for r in Results) == 1
    assert sum("Only 3 available" in r for r in Results) == 1


# Flask Website Integration Tests

def test_WebsiteHome():
    with app.test_client() as Client:
        Response = Client.get("/")
        assert Response.status_code == 200
        assert b"Potatoes" in Response.data


def test_WebsiteBuyVeg():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Buy",
            "Vegetable": "Potatoes",
            "Quantity": "5"
        })
        assert Response.status_code == 200
        assert b"Thank you for ordering" in Response.data
        assert LoadStock()["Potatoes"] == 3


def test_WebsiteInsufficientStock():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Buy",
            "Vegetable": "Potatoes",
            "Quantity": "10"
        })
        assert Response.status_code == 200
        assert b"Only 8 available" in Response.data
        assert LoadStock()["Potatoes"] == 8


def test_WebsiteSellVeg():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Sell",
            "Vegetable": "Potatoes",
            "Quantity": "5"
        })
        assert Response.status_code == 200
        assert LoadStock()["Potatoes"] == 13


def test_WebsiteAddNewVeg():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Sell",
            "Vegetable": "__NEW__",
            "NewVeg": "Sweet Potato",
            "Quantity": "6"
        })
        assert Response.status_code == 200
        assert LoadStock()["Sweet Potato"] == 6


def test_WebsiteAddExistingVeg():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Sell",
            "Vegetable": "__NEW__",
            "NewVeg": "potatoes",
            "Quantity": "5"
        })
        assert Response.status_code == 200
        assert LoadStock()["Potatoes"] == 13
        assert len(LoadStock()) == 4


def test_WebsiteInvalidQuantity():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Buy",
            "Vegetable": "Potatoes",
            "Quantity": "five"
        })
        assert Response.status_code == 200
        assert b"Please enter a valid positive whole number" in Response.data
        assert LoadStock()["Potatoes"] == 8


def test_WebsiteInvalidAction():
    with app.test_client() as Client:
        Response = Client.post("/", data={
            "Action": "Invalid",
            "Vegetable": "Potatoes",
            "Quantity": "5"
        })
        assert Response.status_code == 200
        assert b"Please select Buy or Sell" in Response.data
        assert LoadStock()["Potatoes"] == 8


def test_WebsiteConcurrentPurchases():
    from concurrent.futures import ThreadPoolExecutor

    def Purchase():
        with app.test_client() as Client:
            Response = Client.post("/", data={
                "Action": "Buy",
                "Vegetable": "Potatoes",
                "Quantity": "5"
            })
            assert Response.status_code == 200
            return Response.data

    with ThreadPoolExecutor(max_workers=2) as Executor:
        Results = list(Executor.map(
            lambda _: Purchase(), range(2)
        ))

    assert sum(b"Thank you for ordering" in R for R in Results) == 1
    assert sum(b"Only 3 available" in R for R in Results) == 1
    assert LoadStock()["Potatoes"] == 3
