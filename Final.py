from fileinput import filename

import customtkinter as ctk
import asyncio
import threading
from playwright.async_api import async_playwright
import pandas as pd
import sys
import os
if getattr(sys, 'frozen', False):
    os.environ['PLAYWRIGHT_BROWSER_PATH'] = '0'
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fiverr pro Lead Scraper 2026")
        self.geometry("600x500")
        self.label = ctk.CTkLabel(self , text="AI Lead Generation Engine",font=("Arial", 22, "bold"))
        self.label.pack(pady=30)
        self.nieche_entry= ctk.CTkEntry(self,placeholder_text="Enter Niche(e.g. Dentist)",width=350, height=40)
        self.nieche_entry.pack(pady=10)
        self.loc_entry = ctk.CTkEntry(self, placeholder_text="Enter Location (e.g. New York)",width=350, height=40)
        self.loc_entry.pack(pady=10)
        self.start_btn = ctk.CTkButton(self, text="Start Scraping",command=self.start_thread, height=45, font=("Arial", 16, "bold"))
        self.start_btn.pack(pady=30)
        self.status_label = ctk.CTkLabel(self,text="Status: Ready", text_color="green", font=("Arial", 14 ))
        self.status_label.pack(pady=10)
    def start_thread(self):
        niche= self.nieche_entry.get()
        location = self.loc_entry.get()
        if not niche or not location:
            self.status_label.configure(text="Please enter Niche and Location", text_color="red")
            return
        threading.Thread(target=self.run_async_task, args=(niche,location),daemon=True).start()
    def run_async_task(self,niche,location):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.scrap_logic (niche, location))
    async def scrap_logic(self,niche,location):
        self.status_label.configure(text="Status: launching Browser...", text_color="yellow")
        try:
            os.system("python -m playwrught install chromium")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False, channel="chrome")
                page = await browser.new_page()
                search_query = f"{niche} in {location}"
                await page.goto(f"https://www.google.com/maps/search/{search_query.replace(' ','+')}")
                self.status_label.configure(text="Status: Scraping Data...", text_color="Orange")
                await page.wait_for_timeout(20000)
                leads=[]
                results = await page.query_selector_all("div.Nv2Y8b")
                if not results:
                    results = await page.query_selector_all("a.hfpxzc")
                leads = []
                for res in results[:15]:
                    try:
                        name = await res.get_attribute('aria-label')
                        if not name:
                            name = await res.inner_text()
                        if name:
                            leads.append({"Name": name.split('\n')[0], "Location": location})
                    except: continue
                if leads:
                    df = pd.DataFrame(leads)
                    filename = f"{niche}_{location}.xlsx".replace(" ","_")
                    df.to_excel(filename,index=False)
                    self.status_label.configure(text=f"Status: {len(leads)}) Leads Saved!", text_color="green")
                else:
                    self.status_label.configure(text= "Status: No Leads found! Try Scrolling.", text_color="red")
                await browser.close()
        except Exception as e:
            self.status_label.configure(text=f"Status: Error" - {str(e)[:20]}, text_color="red")
if __name__ == "__main__":
    app = App( )
    app.mainloop()