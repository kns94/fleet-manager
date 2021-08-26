# Fleet Manager
## Birds eye view to manage fleets

### User stories 
- Fleet managers can visualize in realtime where their respective vehicles are
- Fleet managers can get information if vehicles come near the home base

## Tech

- Fleet Manager was built using Pyton Flask, Leaflet and JQuery
- The product underwent several tradeoffs and the other alternative could have been to write code in Django, but I felt that the learning curve was a bit too much for this exercise
- I wanted to use a database initially, but felt that it would be an overkill and the same objective could be achieved with a csv file
- The entire end to end project required a lot of learning for me. Things like Flask, Leaflet, Javascript, Threading, Samsara API were not so familiar to me and I had to keep things simple to come up with a MVP

## Installation

Fleet Manager requires Python 3

Run virtual environment and start the server.

```sh
source venv/bin/activate
pip install -r requirements.txt
python __init__.py
```
Visit localhost:5000 to view and manage your fleets
