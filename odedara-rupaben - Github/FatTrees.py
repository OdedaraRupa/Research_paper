# sudo mn --custom ./FatTrees.py --topo=FatTrees --mac --arp --controller=remote,ip=127.0.0.1,port=6633 --mac --arp 

from mininet.topo import Topo

mytopo=Topo()

def splitlist(list,startl,endl):
    temp=list[startl:endl]
    return temp

def createnodes(nump):
    k=nump       #no of pods
    score=int((k/2)**2)
    sedge=saggr=int((k**2)/2)
    host=int((k**3)/4)
    hostlist=[]
    sedgelist=[]
    saggrlist=[]
    scorelist=[]
    for h in range (host):   
        hostlist.append(mytopo.addHost('h'+str(h+1)))
    for se in range (sedge):
        dpid = '00000000000000{:02d}'.format(se + 1)        
        sedgelist.append(mytopo.addSwitch('s-e'+str(se+1),dpid=dpid))
    for sa in range (saggr):
        dpid = '00000000000000{:02d}'.format(sa + 1 + sedge)        
        saggrlist.append(mytopo.addSwitch('s-a'+str(sa+1),dpid=dpid))
    for sc in range (score):  
        dpid = '00000000000000{:02d}'.format(sc + 1 + sedge + saggr)      
        scorelist.append(mytopo.addSwitch('s-c'+str(sc+1),dpid=dpid))
    return hostlist,sedgelist,saggrlist,scorelist

def connecthosts():

    fnodes= createnodes(4)
    cpi=0
    for j in fnodes[1]:
        temp=int(4/2)        
        for i in range(cpi,len(fnodes[0])):
            if(temp > 0):
                mytopo.addLink(j,fnodes[0][i])                            
            else:
                cpi=i
                break
            temp = temp -1
    
    edges=fnodes[1]
    aggrs=fnodes[2]
    cores=fnodes[3]
    k=0
    count=2
    for sw in range(k,len(edges)):
        if (sw<count):
            pedges=splitlist(edges,k,k+2)
            paggrs=splitlist(aggrs,k,k+2)
            for j in paggrs:
                    for i in pedges:
                        mytopo.addLink(i,j)
            k=k+2
            count=count+2
    
    for c in range(len(cores)):
        for a in range(len(aggrs)):
            if (a%2==0) and (c<2):
                mytopo.addLink(cores[c],aggrs[a])
            elif(c>=2)and (a%2==1):
                mytopo.addLink(cores[c],aggrs[a])

    return mytopo
    

topos = { 'FatTrees': ( lambda: connecthosts() ) }



