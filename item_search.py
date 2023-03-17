from bs4 import BeautifulSoup
import requests
import pandas as pd

class search():
    def __init__(self):
        self.url = "https://www.trolley.co.uk/search/?from=search"
    
    def add_filters(self,store_ids,size):
        if store_ids != None:
                self.store_ids = store_ids
                self.url = f"{self.url}&stores_ids={self.store_ids}"
        if size != None:
            self.size = size
            self.url = f"{self.url}&size={self.size}"

    def find_product(self,item,store_ids=None,size=None,save=False):
        """Function to search for a given products including any user defined filters

        Args:
            item (str): item to search for
            store_ids (str, optional): Filter stores. Don't specify a value to include all stores. Defaults to None.
            size (str, optional): Filter for size of product e.g. "300g" or "2L". Defaults to None.
            save (bool, optional): Set to True if you would like to save as a csv. Defualts to False.

        Returns:
            results (dataframe): dataframe of information about the search results
        """
        results = pd.DataFrame()
        space = "+"
        item = item.replace(" ",space)
        self.url = f"{self.url}&q={item}"
        self.add_filters(store_ids,size)
        print(f"Searching... {self.url}")
        req = requests.get(self.url,)
        source = req.text
        soup = BeautifulSoup(source, 'html.parser')

        results.insert(0,"Brand",[brand.text for brand in soup.find_all('div', attrs={'class':'_brand'})])
        results.insert(1,"Description",[desc.text for desc in soup.find_all('div', attrs={'class':'_desc'})])
        results.insert(2,"Size",[size.text for size in soup.find_all('div', attrs={'class':'_size'})])
        prices = soup.find_all('div', attrs={'class':'_price'})
        links = []
        price = []
        price_per_unit = []
        for i in range(len(results)):
            price.append(prices[i].find(text=True, recursive=False))
            price_per_unit.append(prices[i].find('div', attrs={'class':'_per-item'}).text)
            link = soup.find('a', attrs={"n":i+1})["href"]
            links.append(f"https://www.trolley.co.uk{link}")
        results.insert(3,"Price",price)
        results.insert(4,"Price per unit",price_per_unit)
        results.insert(5,"Link",links)
        if save:
            results.to_csv("results.csv")
        return results

if __name__ == "__main__":
    s = search()
    results = s.find_product(item="chicken",save=True)