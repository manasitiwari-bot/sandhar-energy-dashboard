import asyncio
from playwright.async_api import async_playwright

async def fetch_quadrical_data():
    async with async_playwright() as p:
        # Launch a completely invisible browser in the cloud
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. Go to the Quadrical AI portal login screen
        await page.goto("https://portal.quadrical.ai/login") # Swap with their exact portal link
        
        # 2. Automatically type your login credentials
        await page.fill("input[type='email']", "YOUR_QUADRICAL_EMAIL")
        await page.fill("input[type='password']", "YOUR_QUADRICAL_PASSWORD")
        await page.click("button[type='submit']")
        
        # 3. Wait for the real-time telemetry dashboard cards to load
        await page.wait_for_selector(".generation-metrics-card") 
        
        # 4. Scrape the live raw values directly off the screen text
        live_generation = await page.locator(".live-generation-value").inner_text()
        active_inverters = await page.locator(".active-inverters-count").inner_text()
        
        await browser.close()
        
        # Return the scraped data directly to your Streamlit dashboard charts
        return {
            "live_generation_kw": float(live_generation.replace(" kW", "")),
            "active_inverters": int(active_inverters)
        }
