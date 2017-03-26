import fbchat
import threading
#subclass fbchat.Client and override required methods
idarrayset = []
class EchoBot(fbchat.Client):

    def __init__(self,email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
    def create_account(self, creditcard):
        import http.client
        import json

        info = {"id": "871a79ef8082ee4538025e07513c9c5f","type": "Credit Card","nick_name": creditcard,"_rewards": "0","_balance": "0"}
        
        js = json.dumps(info)

        headers = {"Content-type": "application/json", "Accept": "application/json"}
        client = http.client.HTTPConnection('api.reimaginebanking.com')
        client.request("POST", "/customers?key=871a79ef8082ee4538025e07513c9c5f",body=js,headers=headers)
        r = client.getresponse()
        return (str(r.status) + " " + str(r.reason))

    def createcustomer(self, firstname, lastname, streetnum, streetname, city, state, zipcode):
        import http.client
        import json
        s = {"first_name": firstname,"last_name": lastname,"address": {"street_number": streetnum,"street_name": streetname,"city": city,"state": state,"zip": zipcode}}

        js = json.dumps(s)
                
        headers = {"Content-type": "application/json", "Accept": "application/json"}
     
        client = http.client.HTTPConnection('api.reimaginebanking.com')
        client.request("POST", "/customers?key=871a79ef8082ee4538025e07513c9c5f",body=js,headers=headers)
        r = client.getresponse()
        return (str(r.status) + " " + str(r.reason)) 
        
    def createmerchant(self, name, category):
        import http.client
        import json
        s = {"name": name, "category": category}

        js = json.dumps(s)

        headers = {"Content-type": "application/json", "Accept": "application/json"}
    
        client = http.client.HTTPConnection('api.reimaginebanking.com')
        client.request("POST", "/merchants?key=871a79ef8082ee4538025e07513c9c5f",body=js,headers=headers)
        r = client.getresponse()
        return (str(r.status) + " " + str(r.reason))
    def purchase(self, merchant, medium, amount):
        import http.client
        import json
        info = {"merchant_id": merchant, "medium": medium, "amount":amount}
        js = json.dumps(info)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        client = http.client.HTTPConnection('api.reimaginebanking.com')
        client.request("POST", "/purchases?key=871a79ef8082ee4538025e07513c9c5f",body=js,headers=headers)
        r = client.getresponse()
        return (str(r.status) + " " + str(r.reason))
    def createloan(self, type, status, credit_score, monthly_payment, amount):
        import http.client
        import json
        s = {"type": type, "status": status, "credit_score": credit_score, "monthly_payment": monthly_payment, "amount": amount}

        js = json.dumps(s)

        headers = {"Content-type": "application/json", "Accept": "application/json"}

        client = http.client.HTTPConnection('api.reimaginebanking.com')
        client.request("POST", "/loans?key=871a79ef8082ee4538025e07513c9c5f",body=js,headers=headers)
        r = client.getresponse()
        return (str(r.status) + " " + str(r.reason))

    def inp(self, author_id, s, metadata):
        self.send(author_id, s)
        import time
        time.sleep(0.5)
        last_messages = self.getThreadInfo(author_id, 0)
        while last_messages[0].body[0:4].lower().rstrip() == "what" or last_messages[0].body[0:6].lower().rstrip() == "please":
            last_messages = self.getThreadInfo(author_id, 0)

        return last_messages

    def on_message(self, mid, author_id, author_name, message, metadata):
        global idarrayset
        if author_id in idarrayset:
            return 1
        idarrayset.append(author_id) 
        self.markAsDelivered(author_id, mid) #mark delivered
        self.markAsRead(author_id) #mark read

        if not author_id or str(author_id) != str(self.uid) and "start" in message.lower():
            firstname = self.inp(author_id, "What is your first name?", metadata)[0].body
            lastname = self.inp(author_id, "What is your last name?", metadata)[0].body
            addr = self.inp(author_id, "What is your street address? (Just street number and street name)", metadata)[0].body.split()
            address = [x for x in addr]
            city = self.inp(author_id, "What city do you live in?", metadata)[0].body
            state = self.inp(author_id, "What state do you live in?", metadata)[0].body
            z = self.inp(author_id, "What is your zip code?", metadata)[0].body
            creditlevel = self.inp(author_id, "What credit score category would you identify as?\n\t1) Rebuilding\n\t2) Average\n\t3) Excellent", metadata)[0].body
            self.send(author_id, "We have successfully created your accounts. Now I will help you identify the best credit card, savings account, investment account, or home loan for you. Ask me if you have any questions!")
            import time
            time.sleep(0.5)
            last_messages = self.getThreadInfo(author_id, 0)
            while last_messages[0].body[0:7].lower().rstrip() == "we have":
                last_messages = self.getThreadInfo(author_id, 0)
                s = last_messages[0].body
            if "credit" in last_messages[0].body.lower() and "card" in last_messages[0].body.lower():
                n = self.inp(author_id, "What is your highest priority when looking for a credit card?\n\n\t1) Lowest % APR(Interest Rate) \n\t2) Lowest Annual Fee\n\t3) Highest Loyalty Points/Rewards\n\t4) Maximum Instant Cashback\n\t5) Minimum Repayment\n\t6) Largest Credit Line\n\t7) Lowest Transfer Fee\nTell me the corresponding number for what you would like in your ideal credit card.", metadata)
                array = []
                isany = []
                apr = self.inp(author_id, "What type of % APR would you be most interested in?\n\t1) Low\n\t2) Medium\n\t3) High\n\t4) Any", metadata)[0].body
                annualfee = self.inp(author_id, "What type of annual fee would you be most interested in?\n\t1) None\n\t2) Low\n\t3) High\n\t4) Any", metadata)[0].body
                loyalty = self.inp(author_id, "What amount of loyalty points/rewards would you be most interested in?\n\t1) Low\n\t2) High\n\t3) Any", metadata)[0].body
                cashback = self.inp(author_id, "What amount of cash back would you be most interested in?\n\t1) Low\n\t2) High\n\t3) Any", metadata)[0].body
                repayment = self.inp(author_id, "What amount of minimum monthly repayment would you be most interested in?\n\t1) Low\n\t2) High\n\t3) Any", metadata)[0].body
                credline = self.inp(author_id, "What credit line size would you most prefer?\n\t1) Small\n\t2) Medium\n\t3) Large\n\t4) Any", metadata)[0].body
                transfee = self.inp(author_id, "What type of transfer fee would you most prefer?\n\t1) None\n\t2) Low\n\t3) High\n\t4) Any", metadata)[0].body 
                distances = []
                creditcards = []
                array.append(apr)
                array.append(annualfee)
                array.append(loyalty)
                array.append(cashback)
                array.append(repayment)
                array.append(credline)
                array.append(transfee)
                array.append(creditlevel)
                if apr == 4:
                    isany.append(True)
                else:
                    isany.append(False)
                if annualfee == 4:
                    isany.append(True)
                else:
                    isany.append(False)
                if loyalty == 3:
                    isany.append(True)
                else:
                    isany.append(False)
                if cashback == 3:
                    isany.append(True)
                else:
                    isany.append(False)
                if repayment == 3:  
                    isany.append(True)
                else:
                    isany.append(False)
                if credline == 4:
                    isany.append(True)
                else:
                    isany.append(False)
                if transfee == 4:
                    isany.append(True)
                else:
                    isany.append(False)
                isany.append(False)
                creditcards.append(["Venture Rewards", 2, 2, 2, 1, None, None, 1, 3])
                creditcards.append(["Quicksilver Rewards", 2, 1, 2, 2, None, None, 3, 3])
                creditcards.append(["VentureOne Rewards", 1, 1, 2, 1, None, None, 1, 3])
                creditcards.append(["Premier Dining Rewards", 2, 1, 2, 2, None, None, 1, 3])
                creditcards.append(["QuicksilverOne Rewards", 3, 2, 2, 2, None, None, 1, 2])
                creditcards.append(["Platinum", 3, 1, 1, 1, None, None, 1, 2])
                creditcards.append(["Journey Student Rewards", 2, 1, 1, 1, None, None, 1, 2])
                creditcards.append(["Secured MasterCard", 3, 1, 1, 1, None, None, 1, 1])
                creditcards.append(["Spark Cash for Business", 1, 2, 2, 2, None, None, 1, 3])
                creditcards.append(["Spark Cash Select", 1, 2, 2, 2, None, None, 1, 3])
                creditcards.append(["Spark Miles Select for Business", 1, 1, 2, 2, None, None, 1, 3])
                creditcards.append(["Spark Classic for Business", 3, 1, 1, 2, None, None, 1, 2])
                averages = []
                count = 0
                for card in creditcards:
                    count = 1
                    for anycheck, preferrednum, cardnum in zip(isany, array, card[1:]):
                        print(str(preferrednum) + " "+ str(cardnum))
                        if not cardnum:
                            count += 1
                            continue
                        if anycheck:
                            distances.append(0)
                        else:
                            if count == 8:
                                distances.append(4*(int(preferrednum)-int(cardnum)))
                                count += 1
                                break
                            if count < 5:
                                if count == n:
                                    distances.append(2*(int(preferrednum)-int(cardnum)))
                                    count += 1
                                    break
                            if count >= 7:
                                if count == n:
                                    distances.append(2*(int(preferrednum)-int(cardnum)))
                                    count += 1
                                    break
                            distances.append(int(preferrednum)-int(cardnum))
                        count += 1
                    sumd = 0.0
                    print(' '.join([str(x) for x in distances]))
                    for i in distances:
                        sumd += i*i
                    avg = sumd/float(len(distances))
                    averages.append(str(avg))
                    distances = []
                index = averages.index(min(averages))
                thegreatcard = creditcards[index][0]
                self.send(author_id, "The best card for you based on the preferences you indicated is: "+thegreatcard+"\n\n" + "Find more information about your card at: https://www.capitalone.com/credit-cards/")

                self.create_account(thegreatcard)
                me = self.createmerchant("Wenxi", "Cheese")
                trans = self.inp(author_id, "What can you help with you next? Now that you have a credit card, we can help you make a transaction. Please enter an amount.", metadata)[0].body
                self.purchase("58d7b4e41756fc834d909c0d", "balance", trans)
                self.send(author_id,"New balance: " + "-"+trans)
            elif "loan" in last_messages[0].body.lower():
                a = self.inp(author_id, "What kind of loan are you looking for?\n\t 1) Home loans\n\t 2) Auto loans\n\t 3) Small Business Loans", metadata)[0].body
                l = self.inp(author_id, "Please enter a loan amount.", metadata)[0].body
                cs = self.inp(author_id, "Please enter your credit score.", metadata)[0].body
                if a == 1:
                    self.createloan("home", "pending", cs, int(l)/12, l)  
                elif a == 2:
                    self.createloan("auto", "pending", cs, int(l)/12, l)
                else:
                    self.createloan("small business", "pending", cs, int(l)/12, l)
                self.send(author_id, "Your loan application has been submitted and you will be notified of the decision as soon as possible. Thanks!")

bot1 = EchoBot("Days.Hacktj", "DAYSHackTJ")
bot1.listen()
