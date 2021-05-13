import ipaddress

#import file
with open('arista_tmp', 'r') as aristatemp:
    template = aristatemp.read()

#ip validation
def inputIpAddress(ipName):
    while True:
        try:
            inputIpAddr = input(ipName+' IP:')
            ipaddress.ip_address(inputIpAddr)
        except ValueError:
            print('IP Error')
        else:
            break
    return inputIpAddr

# create trunk interface
def trunkMode():
    trunkVlans = ''
    trunkInterface = input('Trunk interface:')
    trunkVlanCount = input('Trunk vlan count:')
    trunkDescription = input('Description:')
    for i in range(1, int(trunkVlanCount)+1):
        vlan = input(str(i)+'. VLAN:')
        trunkVlans = trunkVlans+vlan+','
    trunkMTU = input('TrunkMTU:')
    trunkTemplate = 'interface '+trunkInterface+'\n'+'description '+trunkDescription + \
        '\n switchport mode trunk\n switchport trunk allowed vlan ' + \
        trunkVlans+'\n mtu '+trunkMTU+'\n'
    return trunkTemplate

# odpf builder
def ospfBuild(areaId,vrfEnable,loopbackIp):
    routerOspf = 'router ospf '+areaId
    if vrfEnable == True:
        routerOspf = routerOspf+' vrf area'+areaId
    routerOspf = routerOspf+'\n router-id '+loopbackIp+'\n redistribute connected route-map ospf-out\n redistribute static route-map ospf-out\n area 0.0.0.'+areaId+' nssa no-summary\n network '+loopbackIp+'/32 area 0.0.0.'+areaId+'\n'
    ospfNetworkNumber = input('How many network without Lo?:')
    for _ in range(int(ospfNetworkNumber)):
        ospfNetwork = input('Network address:')
        ospfNetworkMask = input('Network mask:')
        routerOspf = routerOspf+' network '+ospfNetwork+'/'+ospfNetworkMask+' area 0.0.0.'+areaId+'\n'
    routerOspf = routerOspf+'max-lsa 40000 90 warning-only\n'
    return(routerOspf)

# replace $routerHostname in template
routerHostname = input('Hostname:')
#routerHostname = 'Sad'
template = template.replace('$routerHostname', routerHostname)

# replace $routerSNMPSLoc in template
routerSNMPSLoc = input('Location:')
#routerSNMPSLoc = 'Sad'
template = template.replace('$routerSNMPSLoc', routerSNMPSLoc)

# replace $routerLoIp in template
routerLoIp = inputIpAddress('Loopback')
#routerLoIp = '192.168.0.1'
template = template.replace('$routerLoIp', routerLoIp)

# replace $routerBrIp in template
routerBrIp = inputIpAddress('Bridge')
#routerBrIp = '192.168.10.1'
template = template.replace('$routerBrIp', routerBrIp)

# replace $routerArea in template
routerArea = input('Area number:')
#routerArea = '168'
template = template.replace('$routerArea', routerArea)

# replace $routerGateway in template
routerGateway = inputIpAddress('Default Gateway')
#routerGateway = '192.168.1.1'
template = template.replace('$routerGateway', routerGateway)

# Build Native Ospf
routerNativeOspf = ospfBuild(routerArea,False,routerLoIp)
template = template.replace('$routerNativeOspf', routerNativeOspf)

# Gateway mode
routerGatewayMode = input('Gateway interface mode (Trunk/Routed):')
if str(routerGatewayMode) == 'Trunk' or 'trunk':
    template = template.replace('$defaultGatewayConfig', trunkMode())

#

# print config
print(template)
# make config txt
outputFile = open(routerHostname+'.txt', 'x')
outputFile.write(template)
