import logging
import asyncio
from playwright.async_api import async_playwright, Playwright, Page, Locator
from mcp.server.fastmcp import FastMCP


# Initialize mcp server and logger
# TODO: Change this argument
mcp = FastMCP("Schenker")
logger = logging.getLogger(__name__)

# Constants
# TODO: Change this var name
DBSCHENKER_SEARCH_URL = "https://www.dbschenker.com/app/tracking-public/?refNumber="


@mcp.tool()
async def get_shipment_info(reference_number: str) -> dict:
    """Get DB Schenker shipment details, shipment history, and individual package history in a formatted string.
    Args:
        reference_number: DB Schenker Reference number for the shipment
    """
    async with async_playwright() as pw:
        # Set up browser tab
        browser = await pw.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        # Perform actions
        await goto_shipment_page(page, reference_number)
        shipment_details = await scrape_shipment_details(page)
        shipment_history = await scrape_shipment_history(page)
        packages_history = await scrape_packages_history(page)

        await browser.close()
        shipment_data = {"details": shipment_details, "shipment_history": shipment_history, "invividual_packages_history": packages_history}
        return shipment_data


async def goto_shipment_page(page: Page, reference_number: str) -> None:
    """Visits shipment page for reference number and removes any cookie pop-ups.
    Args:
        page: The Playwright Page object to use
        reference_number: DB Schenker Reference number for the shipment
    """
    # 1. Visit page, get cookie dialog
    await page.goto(DBSCHENKER_SEARCH_URL+reference_number)

    # 2. Click required cookies and wait for dialog to close
    await page.get_by_role("button", name="Required Cookies").click()
    dialog = page.get_by_role("dialog")
    await dialog.wait_for(state="hidden")


async def scrape_shipment_details(page: Page) -> dict:
    """Returns the information from the 'Shipment Details' area.
    Args:
        page: A Playwright page object that has already gone to a specific DB Schenker shipment's page
    """
    logging.info("Scraping shipment details...")
    
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
    
    logging.info("Shipment details scraped.")
    return results


async def scrape_shipment_history(page: Page) -> list[dict]:
    """Returns the information from the 'Shipment Status History' area.
    Args:
        page: A Playwright page object that has already gone to a specific DB Schenker shipment's page
    """
    logger.info("Scraping shipment history...")
    status_history = []
    await page.get_by_role("button", name="Shipment Status History").click()    # Open drop-down to expose data

    # Locate the html table for shipment event history
    history_table = page.locator("table").filter(has=page.locator('[data-test="shipment_status_history_event_label"]'))
    
    # Locate all rows in said table with CSS selector
    rows = history_table.locator("tbody tr")
    row_count = await rows.count()

    for i in range(row_count):
        row = dict()
        # Select the nth rows data items
        event = page.locator(f'[data-test="shipment_status_history_event_{i}_value"]')
        date = page.locator(f'[data-test="shipment_status_history_date_{i}_value"]')
        location = page.locator(f'[data-test="shipment_status_history_location_{i}_value"]')
        reasons = page.locator(f'[data-test="shipment_status_history_reasons_{i}_value"]')

        row["event"] = await event.inner_text()
        row["date"] = await date.inner_text()
        row["location"] = await location.inner_text()
        row["reasons"] = await reasons.inner_text()

        status_history.append(row)

    logger.info("Shipment history scraped.")

    return status_history

async def scrape_packages_history(page: Page) -> dict[str, list[dict[str, str]]]:
    """Returns a dictionary of package IDs mapping to history info.
    Args:
        page: A Playwright page object that has already gone to a specific DB Schenker shipment's page
    """
    packages_history = dict()
    await page.get_by_role("button", name="Packages").click()   # Open drop-down

    packages = page.locator("[class~='pt-packages-box']") # ~= performs a substring match 
    package_locators = await packages.locator("> div").all()   # Gets immediate children divs
    
    for i, p in enumerate(package_locators):
        await packages.locator(f"[data-test='package_id_{i}_value']").click()   # Expand package history info
        package_id = await packages.locator(f"[data-test='package_id_{i}_value']").inner_text()
        history_table = p.get_by_role("table")
        history = await scrape_package_history(history_table)
        
        packages_history[package_id] = history

    return packages_history

async def scrape_package_history(table: Locator):
    """Extracts and returns the data from the given history table
    Args:
        table: playwright locator for the table containing the package history for a specific package in the 'Packages' region of the DB Schenker shipment page
    """
    history = []
    more_rows = True
    headers = ["Event", "Country", "Place", "Date"]

    paginator = table.locator("xpath=..").locator("mat-paginator")  # Get sibling
    next_page_button = paginator.get_by_label("Next page")

    while more_rows:
        rows = await table.locator("> mat-row").all()

        for row in rows:
            data = dict()
            cells = await row.locator("> mat-cell").all()

            for i, cell in enumerate(cells):
                data[headers[i]] = await cell.inner_text()

            history.append(data)

        if more_rows := await next_page_button.is_enabled():
            await next_page_button.click()

    return history

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

""" for debugging
async def main():
   res = await get_shipment_info("1806290829")
   logger.info(res)

asyncio.run(main())
"""