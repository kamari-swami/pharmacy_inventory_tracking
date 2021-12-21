import os

def parse_inputPS1(input_line):
    if line[0] in ['0','1','2','3','4','5','6','7','8','9']:
        head = line.strip().partition('#')
        if ',' not in head[0]:
            return None
        else:
            data = [x.strip() for x in head[0].split(',')]
            return data[0], data[1]

class DrugNode:
    master_Inventory_list = []

    # master_Inventory_list == TOTAL inventory []
    # example of master_Inventory_list  == [[112,4,1],[113,4,3],[113,4,1]]


    def __init__(self, Uid, availCount=0):
        self.Uid = int(Uid)
        self.avCount = int(availCount)
        self.chkoutCtr = 1
        self.left = None
        self.right = None

    def log_write(self,text):
        log = open(os.getcwd()+'\outputPS1.txt', 'a')
        log.write(text+'\n')
        log.close()


    def find_me(self,drugId):
        if len(self.master_Inventory_list) == 0:
            return 0, False
        else:
            int_drugId = int(drugId)
            for pos,row in enumerate(self.master_Inventory_list):
                if int_drugId == int(row[0]):
                    return pos, True
            return 1, False

    def update_masterInventory(self,dId,quantity):
        position, found_flag = self.find_me(dId)
        if found_flag:
            newchkoutCtr = self.master_Inventory_list[position][-1]+1
            if newchkoutCtr%2 == 0:
                #it is a sell order if the counter is even. Stock quantity will be subtracted.
                if self.master_Inventory_list[position][-2]-int(quantity) < 0:
                    self.log_write("Quantity requested for drug id ({0}) is ({1}) is more than available stock ({2})".format(dId,quantity,self.master_Inventory_list[position][-2]))
                    self.log_write("This Sell Order was Skipped. No change in inventory or counter Status was made")
                    #return False
                    pass
                else:
                    self.master_Inventory_list[position] = [int(dId),self.master_Inventory_list[position][-2]-int(quantity),newchkoutCtr]
            else:
                #it is a buy order if counter is Odd. Stock quantity will be added.
                self.master_Inventory_list[position] = [int(dId),self.master_Inventory_list[position][-2]+int(quantity),newchkoutCtr]
        else:
            temp_list = [int(dId), int(quantity),self.chkoutCtr]
            self.master_Inventory_list.append(temp_list)
            
    def parse_promptsPS1(self,promptCmd):
        head = promptCmd.partition(':')
        if promptCmd in ['printDrugInventory']:
            self.printDrugInventory()
        elif promptCmd in ['printStockOut']:
            self.printStockOut()
        elif head[0] in ['updateDrugList','checkDrugStatus','highDemandDrugs','supplyShortage','freqDemand']:
            if head[0] in ['updateDrugList']:
                try:
                    drugId, quantity = head[2].split(',')
                except:
                    self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))
                    pass
                else:
                    if quantity.strip():
                        if drugId.strip():
                            self.updateDrugList(drugId,quantity)
                        else:
                            self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))
                    else:
                        self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))
            elif head[0] in ['checkDrugStatus']:
                try:
                    drugId = int(head[2].strip())
                except:
                    self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))
                    pass
                else:
                    if drugId:
                        self.checkDrugStatus(drugId)
                    else:
                        self.log_write("Invalid promptCommand.. [{0}]".format(promptCmd))
            elif head[0] in ['freqDemand']:
                try:
                    buy_sell, threshHold = head[2].split(',')
                except:
                    self.log_write("Invalid promptCommand-1... [{0}]".format(promptCmd))
                    pass
                else:
                    if buy_sell.strip():
                        if buy_sell.strip() in ['buy', 'sell']:
                            if threshHold.strip():
                                self.highDemandDrugs(buy_sell, threshHold)
                        else:
                            self.log_write("Invalid promptCommand-2... [{0}]".format(promptCmd))
                    else:
                        self.log_write("Invalid promptCommand-3... [{0}]".format(promptCmd))

            else:
                try:
                    queryQuantity = int(head[2].strip())
                except:
                    self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))
                    pass
                else:
                    if queryQuantity:
                        self.supplyShortage(queryQuantity)
                    else:
                        self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))                
        else:
            self.log_write("Invalid promptCommand... [{0}]".format(promptCmd))
            pass
                


    # Insert Node in ADT binary Tree
    def readDrugList(self,Uid):
            if self.Uid:
                if Uid < self.Uid:
                    if self.left is None:
                        self.left = DrugNode(Uid)
                    else:
                        self.left.readDrugList(Uid)
                elif Uid > self.Uid:
                    if self.right is None:
                        self.right = DrugNode(Uid)
                    else:
                        self.right.readDrugList(Uid)
                else:
                    pass
            else:
                self.Uid = Uid

    def printDrugInventory(self):
        self.log_write("------printDrugInventory-------")
        self.log_write("Total number of medicines entered in the inventory : {0}".format(len(self.master_Inventory_list)))
        for item in root.inorderTraversal(root):
            for pos,row in enumerate(self.master_Inventory_list):
                if int(item) == int(row[0]):
                    if int(row[-1])%2 == 0:
                        self.log_write("{0},{1}".format(item,row[-2])) #print(int(item),",",row[-2],row[-1])
                    else:
                        self.log_write("{0},{1}".format(item,row[-2])) #print(int(item),",",row[-2],row[-1])
        self.log_write("-------------------------------")
        #self.log_write(root.inorderTraversal(root))
        #self.log_write(root.master_Inventory_list)

    def updateDrugList(self, Uid, availCount):
        self.log_write("------updateDrugList: {0}, {1}-------".format(Uid,availCount))
        self.readDrugList(int(Uid))
        self.update_masterInventory(int(Uid),int(availCount))
        self.log_write("Stock updated for drug ID: {0} with quantity: {1}".format(Uid,availCount))
        self.log_write("-------------------------------")

    def printStockOut(self):
        self.log_write("------printStockOut-------")
        self.log_write("The following medicines are out of stock:")
        outOfStock_flag = False
        for item in root.inorderTraversal(root):
            for pos,row in enumerate(self.master_Inventory_list):
                if int(item) == int(row[0]):
                    if int(row[-2]) == 0:
                        self.log_write("{0},{1} --> OUT OF STOCK".format(item,row[-2])) #(int(item),",",row[-2],"OUT OF STOCK")
                        outOfStock_flag = True
                    else:
                        pass
                else:
                    pass
        if outOfStock_flag == False:
            self.log_write("NO OUT OF STOCK MEDICINES FOUND !")
        self.log_write("-------------------------------")

    def checkDrugStatus(self, Uid):
        self.log_write("------checkDrugStatus: {0}-------".format(Uid))
        if int(Uid) in root.inorderTraversal(root):
            if self.find_me(int(Uid)):
                for pos,row in enumerate(self.master_Inventory_list):
                    if int(Uid) == int(row[0]):
                        if int(row[-1])%2 == 0:
                            self.log_write("Drug ID :{0}, Entered into system: {1}-times, Stock Availablity :{2}-units, LAST STATUS : SELL".format(Uid,row[-1],row[-2]))
                        else:
                            self.log_write("Drug ID :{0}, Entered into system: {1}-times, Stock Availablity :{2}-units, LAST STATUS : BUY".format(Uid,row[-1],row[-2]))
            else:
                self.log_write("Drug ID not found in master stock list")
        else:
            self.log_write("Drug ID {0} not found in stock".format(Uid))
        self.log_write("-------------------------------")
  
    def supplyShortage(self,minUnits):
        self.log_write("------supplyShortage: {0}-------".format(Uid))
        supplyShortage_flag = False
        self.log_write("Minimum Units <= {0}".format(minUnits))
        self.log_write("Drugs with supply shortage")
        for item in root.inorderTraversal(root):
            for pos,row in enumerate(self.master_Inventory_list):
                if int(item) == int(row[0]):
                    if int(row[-2]) <= int(minUnits):
                        self.log_write("{0},{1}".format(item,row[-2])) #int(item),",",row[-2])
                        supplyShortage_flag = True
        if supplyShortage_flag == False:
            self.log_write("No items on short supply")
        self.log_write("-------------------------------")
    
    def highDemandDrugs(self,status,frequency):
        self.log_write("------freqDemand: {0}, {1}-------".format(status, frequency))
        self.log_write("Drugs with {0} entries more than {1} times are :".format(status,frequency))
        highDemangDrug_flag = False
        for item in root.inorderTraversal(root):
            for row in self.master_Inventory_list:
                if int(item) == int(row[0]):
                    total = int(row[-1]) 
                    sell = total // 2
                    buy = total-sell
                    if 'sell' in status:
                        if sell > int(frequency):
                            self.log_write("Drug ID :{0}, CheckoutCounter :{1}".format(item,total))
                            highDemangDrug_flag = True
                    elif 'buy' in status:
                        if buy > int(frequency):
                            self.log_write("Drug ID :{0}, CheckoutCounter :{1}".format(item,total))
                            highDemangDrug_flag = True
                    else: pass
                else: pass
        if highDemangDrug_flag == False:
            self.log_write("No such drug id present in the system")
        self.log_write("-------------------------------")
    
    # Print the Tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
            #print(self.Uid)
            return self.Uid
        if self.right:
            self.right.PrintTree()

    # Inorder traversal
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.Uid)
            res = res + self.inorderTraversal(root.right)
        return res

class_init_flag = False
output_file = open(os.getcwd()+'/outputPS1.txt', 'w')
input_file = open(os.getcwd()+'/inputPS1.txt','r')
for line in input_file:
    if parse_inputPS1(line) !=  None:
        Uid, quantity = parse_inputPS1(line)
        if class_init_flag == False:
            root = DrugNode(Uid)
            root.update_masterInventory(Uid,quantity)
            class_init_flag = True
        else:
            root.readDrugList(int(Uid))
            root.update_masterInventory(Uid,quantity)

prompt_file = open(os.getcwd()+'/promptsPS2.txt','r')
for line in prompt_file:
    root.parse_promptsPS1(line.strip())
#root.PrintTree()

