# Bluetooth Frequency Hopping Simulator
# Giulio & Luca
from random import *

band_num=79
slave_num=7
# 0.5 = meaning 50% of total channel capacity used
# The higher this number the more collisions
channel_usage_ratio=0.5

def isMyTimeToTransmitOrReceive(global_time, slave_id, piconet_size):
    # set active-state based on global_time, slave_id, piconet_size
    # this can be done in distributed way by each slave, independently
    active = (global_time%piconet_size)==(slave_id-1)
    print '         isMyTimeToTransmitOrReceive:', active
    return active

def doIHaveSomethingToTransmitOrReceive(global_time):
    # how full is the channel being used
    if uniform(0., 1.) < channel_usage_ratio:
        print '         doIHaveSomethingToTransmitOrReceive: True'
        return True
    return False

def slave(slave_id, global_time, piconet_size):
    # implement distributed frequency hopping scheme (simplified)
    freq=randint(1, band_num+1)
    if isMyTimeToTransmitOrReceive(global_time, slave_id, piconet_size):
        if doIHaveSomethingToTransmitOrReceive(global_time):
            print '                 gtime:', global_time, 'slave', slave_id, 'freq', freq
            return freq
    return  None

# comm process managed by all masters
def simulate_communication_process(master_num=2, slaves_per_piconet=[4,4,3,5], time_rounds=10):
    txrx_list = []

    # iterate over sumulation time
    for global_time in range(1,time_rounds+1):
        print 'simulating: time step', global_time
        # iterate over piconets
        for piconet in range(1,master_num+1):
            print '  piconet:', piconet
            # iterete over slaves of each piconet
            for slave_id in range(1,slaves_per_piconet[piconet-1]+1):
                print '    slave:', slave_id
                # master tells slaves id,piconet-size,global_time
                freq = slave(slave_id, global_time, slaves_per_piconet[piconet-1])
                if freq:
                    txrx_list.append({'t':global_time, 'piconet':piconet, 'slave':slave_id, 'freq':freq})

    # search for collisions
    txrx_num=0 ; collisions_num=0
    collisions={}
    for txrx in txrx_list:
        txrx_num += 1
        time_freq='time:'+str(txrx['t'])+'|freq:'+str(txrx['freq'])
        pn_and_slave='piconet:'+str(txrx['piconet'])+'|slave_id:'+str(txrx['slave'])
        # print txrx
        str_print = time_freq + ' ' + pn_and_slave
        if time_freq in collisions.keys():
            str_print += ' ==> COLLISION ' + time_freq + ' ' + collisions[time_freq]
            collisions_num += 1
        else:
            collisions[time_freq] = pn_and_slave

        print str_print

    print 'txrx', txrx_num, 'collisions', collisions_num, \
        'collision rate %', float(collisions_num) / float(txrx_num) * 100


if __name__ == "__main__":
    seed(42)

    simulate_communication_process(master_num=6, slaves_per_piconet=[4,4,3,5,2,1], time_rounds=1000)
