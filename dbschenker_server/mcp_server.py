import logging
import asyncio
from playwright.async_api import async_playwright, Playwright, Page
from mcp.server.fastmcp import FastMCP

# TODO: Add function for getting to known state of website, i.e check for cookie popups and get through them etc. Pass around the page object in the different functions.

# Initialize mcp server 
# TODO: Change this argument
mcp = FastMCP("Schenker")

# Constants
# TODO: Change this var name
DBSCHENKER_BASE = "https://www.dbschenker.com/app/tracking-public/?refNumber="



@mcp.tool()
async def get_shipment_info(reference_number: str) -> str:
    """Get formatted shipment info.
Includes: sender and receiver names and addresses, package details (weight, dimensions, piece count, etc.), complete tracking history for the shipment as a whole, and individual tracking history for every package.
Args:
    reference_number: DB Schenker Reference number for the shipment
"""

async def scrape_shipment_tracking_history(reference_number: str) -> list[dict]:
    """"""
"""
async def scrape_package_details(reference_number: str) -> dict:
   
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(DBSCHENKER_BASE+reference_number)
        await page.screenshot(path="screenshot.png")
        await browser.close()
"""

async def goto_shipment_page(page: Page, reference_number: str) -> None:
    """Visits shipment page for reference number and removes any cookie pop-ups.
Args:
    page: The Playwright Page object to use
    reference_number: DB Schenker Reference number for the shipment
"""
    # 1. Visit page, get cookie dialog
    await page.goto(DBSCHENKER_BASE+reference_number)
    await page.screenshot(path="screenshots/cookie-dialog.png")

    # 2. Click required cookies and wait for dialog to close
    await page.get_by_role("button", name="Required Cookies").click()
    dialog = page.get_by_role("dialog")
    await dialog.wait_for(state="hidden")
    await page.screenshot(path="screenshots/cookie-accept.png")

async def read_shipment_info(page: Page) -> dict:
    """Takes a DB Schenker shipment page and returns the information from the 'Shipment Details' area.
Args:
    page: A Playwright page object that has already gone to a specific DB Schenker shipment's page"""
    
    data_points = [
        "shipper_place_value",
        "consignee_place_value",
        "collect_from_value",
        "schenker_dispatching_office_value",
        "deliver_to_value",
        "shipment_eta_value",
        "estimated_delivery_date_value",
        "agreed_delivery_date_value",
        "total_weight_value",
        "total_volume_value",
        "loading_meters_value",
        "number_of_pieces_value"
    ]

    results = dict()

    for point in data_points:
        # Locates the element with attribute data-test=point 
        # Inner text is what you would get if you tried to copy the element in your browser.
        value = await page.locator(f'[data-test="{point}"]').inner_text()
        results[point] = value
    
    await page.screenshot(path="screenshots/ship-page.png")

    return results

async def read_shipment_history(page: Page) -> list[dict]:
    """Takes a DB Schenker shipment page and returns the information from the 'Shipment Status History' area.
Args:
    page: A Playwright page object that has already gone to a specific DB Schenker shipment's page"""

    # history_table = page.locator("table").filter(has=page.locator('[data-test="shipment_status_history_event_label"]'))
    # rows = specific_table.locator("tr")
    # then go through the rows to find each event and its data
    shipment_statuses = []
    

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await goto_shipment_page(page, "1806203236")
        await browser.close()

asyncio.run(main())