# pharmacy_inventory_tracking
Problem Statement:
Pharmacy store requires your assistance in implementing a medicine inventory tracker system.  The objective is to keep a track of each product and also determine which ones to order if they are  less than a specific quantity. In order to maintain this information, each drug has a unique identification  number  and  a  counter  to  keep  a  track  of  its  available  quantity  in  the  system.  Whenever  a  product  moves in/out of the inventory its unique drug ID is recorded.  When a medicine is added to the inventory for the first time, the checkout counter is set to 1 and is  considered a buy order. From then onwards, the counter is incremented for each subsequent entry of  the same product is a buy and sell order. If the counter is odd, it means a buy order and if the counter  is even, it means a sell order.  Every time when ‘x’ units of a drug/medicine are added into the inventory, its available count increases  by ‘x’ value. On the other hand, when ‘x’ units of a medicine are ordered by customers, its available  count reduces by ‘x’ in the inventory.  In addition to this a list of medicines less than a specific quantity ‘a’ and ordered at least once by the  customers is prepared to determine by how many units these medicines have a supply shortage and  needs to be ordered by the store.  The planning team uses the above system to answer the below questions:
1. List of distinct medicines added into the inventory and their currently available quantity.
2. List of medicines which are stocked out (all available quantities sold) 
3. Determine the latest status of a particular medicine.
4. List of medicines that have moved in/out of the inventory more than ’z’ number of times.
5. List of all the medicines that have a supply shortage and by what quantity.

Implement the above problem statement in Python >= 3.7 using BINARY TREE ADT. 
