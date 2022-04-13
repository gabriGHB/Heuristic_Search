#!/bin/bash
#first test, we will use the data provided by the statement.
#We will also change the extension, to demostrate that it works
#independently of the extension
python CSPStowage.py ./CSP-tests map1.ght containers1.ght

#now, we will provide a smaller map with fewer containers, but yet
#more cells than containers. Only one solution
python CSPStowage.py ./CSP-tests map2.txt containers2.txt

#situation with more containers than cells. Error expected
python CSPStowage.py ./CSP-tests map3.txt containers3.txt

#big map with lots of containers. Slower???...
python CSPStowage.py ./CSP-tests map4.txt containers4.txt

#map with R containers but without E cells. Error expected
python CSPStowage.py ./CSP-tests map5.txt containers5.txt

#only containers going to port 2. Good
python CSPStowage.py ./CSP-tests map6.txt containers6.txt

#only containers going to port 1. Good
python CSPStowage.py ./CSP-tests map7.txt containers7.txt

#X cells in the middle. should not work. it works...
python CSPStowage.py ./CSP-tests map8.txt containers8.txt

#force port 1 go behind. Should give not solution. it works fine
python CSPStowage.py ./CSP-tests map9.txt containers9.txt

#X cells on the first row. Should give 0 solutions. It gives 2
python CSPStowage.py ./CSP-tests map10.txt containers10.txt
