
#(name:[0age,[i0date,i1time,i2tickets]]

movie_lst={'spectre':[[20,'6:00',5],[20,'8:30',8]],
           'baahubali':[[21,'5:30',7]]}

age_lst={'spectre':18,
         'baahubali':12}

def talk():
    """
    This function is the one which converses with the user.
    Although this isn't technically Q&A system it still stores proper information about the user and responds properly
    """
    #0name,1date,2time,3tickets,4age       
    lst=['',0,'0:00',0,0]
    flag=True
    flag2=True
    flag_dat=False
    flag_tim=False
    while(flag):
        inp=raw_input("Welcome. Please enter the details of your movie")
        inp=inp.lower()
        for i in movie_lst.keys():
            if i in inp:
                lst[0]=i
        if lst[0]=='':
            print("Sorry but that movie is not being aired try another one")
            continue
        lst[4]=int(raw_input("Please enter your correct age in numbers"))
        print lst
        if age_lst[lst[0]]>lst[4]:
            print("Sorry you are underage please select another movie")
            continue
        num1=inp.find('on')#date
        num2=inp.find('at')#time
        num3=inp.find('ticket')#ticket
        #Depending on whether the user has given any info regarding the three we appropriately ask questions
        if num1==-1:
            inp1=raw_input("Please enter the date you want to go in numbers")
            lst[1]=int(inp1[0:2])
        else:
            lst[1]=int(inp[num1+3:num1+5])
        if num2==-1:
            inp2=raw_input("Please enter the time you want to go")
            if len(inp2)==1:
                lst[2]=inp2+":00"
            else:
                lst[2]=inp1[0]+":"+inp2[2]+inp2[3]
        else:
            if inp[num2+4]=='.' or inp[num2+4]==':':
                lst[2]=inp[num2+3]+":"+inp[num2+5]+inp[num2+6]
            else:
                lst[2]=inp[num2+3]+":00"
        if num3==-1:
            inp3=raw_input("Please enter the number of tickets")
            lst[3]=int(inp3[0])
        else:
            lst[3]=int(inp[num3-2])   
        det=movie_lst[lst[0]]
        for j in det:
            if j[0]==lst[1]:
                flag_dat=True
        if flag_dat!=True:
            print ("There is no show on "+str(lst[1])+" .Try other date")
            continue
        for j in det:
            if j[2]>=lst[3]:
                flag_tim=True
        if flag_tim!=True:
            print ("There is no show at "+lst[2]+" .Try other time")
            continue
        for j in det:
            if j[2]<lst[3]:
                print "Sorry only "+str(j[2])+" tickets are available"
                break
            
            elif j[0]==lst[1] and j[1]>=lst[2]:
                print str(lst[3])+" tickets are available for "+lst[0]+" on "+str(lst[1])+ " at "+j[1]
                print "Thank You for booking"
                j[2]-=lst[3]
                flag2=False
                break
        if (flag2!=False):
            print ("There is no show at that combination of time and date")
        continue    
                
            
           
            
        
    
    
        
    
