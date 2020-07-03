# Age of Menor - Autonomous Buyer  
This little script allows you to automatically buy items from the Age of Menor itemshop based on provided information.  
<br>
**Disclaimer**
<br>
Use this tool on your own risk. Little to no coding knowhow is necessary to understand that this script does not log your credentials.
  
## How it works
This tool accepts two ways to specify the desired item.<br>
You can either provide the `--itemid` directly or specifying an `--itemname`.<br>
In case you provide the `--itemid` the tool perfoms `POST shop.ageofmenor.cc/mall/purchases/itemid`.<br>
If you just provide an `--itemname` a list of all Hotdeals is collected and searched for the given `--itemname`.<br>
The search itself extracts the itemshop entry titel and checks whether it contains the provided `--itemname`.<br>
If it finds a match the id is extracted and `POST shop.ageofmenor.cc/mall/purchases/itemid` performed.<br>

## Installation  
1. Navigate into `.../aom-buyer`
2. Install dependencies using `pip3 install -r requirements.txt` 

## Usage
### Provide itemid directly
`python3 -m src.main --username "USERNAME" --password "PASSWORD" --itemid ITEMID --desired-time "13:54:01"`

### Search Hotdeals for itemname
`python3 -m src.main --username "USERNAME" --password "PASSWORD" --itemname "Shining" --desired-time "13:54:01"`

## Potential bugs
- If you are on a Unix system provide arguments containing a special character using single quotes.