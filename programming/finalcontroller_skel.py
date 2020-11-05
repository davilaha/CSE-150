# Final Skeleton
#
# 
#
# To check the source and destination of an IP packet, I use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. SO I use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, I do the following, replace <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, I simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # TThe following modifications have 
    # been made:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # These can be used to determine where a packet came from. To figure out where a packet 
    # is going, I use the IP header information.

    #ofp_flow_mod properties from Lab3
    msg = of.ofp_flow_mod() #create packet out message
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 240
    msg.hard_timeout = 241
    msg.data = packet_in

    #packet type boolean
    ip = packet.find('ipv4')
    icmp = packet.find('icmp')

    if ip is None:
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      #print 'non-ip, flooded'

    else: #packet is ip packet
      if switch_id is 1:
        if port_on_switch is 8: #from host 1
          msg.actions.append(of.ofp_action_output(port = 1))
        elif port_on_switch is 1 #from s4
          msg.actions.append(of.ofp_action_output(port = 8))

      elif switch_id is 2:
        if port_on_switch is 8: #from host 2 
          msg.action.append(of.ofp_action_output(port = 1))
        elif port_on_switch is 1 #from s4
          msg.action.append(of.ofp_action_output(port = 8))
      
      elif switch_id is 3: 
        if port_on_swtich is 8: #from host 3
          msg.ation.append(of.ofp_action_output(port = 1))
        elif port_on_switch is 1: 
            msg.action.append(of.ofp_action_output(port = 8))
      
      elif switch_id is 5:
         if port_on_switch is 8:
            msg.action.append(of.ofp_action_output(port = 1))
         elif port_on_switch is 1:
            msg.action.append(of.ofp_action_output(port = 8)) #send to host 5

      elif switch_id is 4:
        if port_on_switch is 8:
          #blocking ICMP traffic from the untrusted host to anywhere internally
          if icmp is not None: 
            self.connection.send(msg)
            return
          #untrusted Host cannot send any IP traffic to the server
          elif ip.dst == '10.5.5.50': 
            self.connection.send(msg) #drop ip packet to host 5
            return
          elif ip.dstip == '10.1.1.10': #forward to host 1
            msg.action.append(of.ofp_action_output(port  = 1))
          elif ip.dstip == '10.2.2.20' : #forward to host 2
            msg.action.append(of.ofp_action_output(port = 2))
          elif ip.dstip == '10.3.3.30': #forward to host 3
            msg.action.append(of.ofp_action_output(port = 3))

        #if port on the switch is not 8 (from the untrusted host) allow traffic flow    
        else:  
          if ip.dstip == '123.45.67.89': #forward to h4
    				msgAction = of.ofp_action_output(port = 1)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 4'
    			elif ip.dstip == '10.1.1.10': #forward to h1
    				msgAction = of.ofp_action_output(port = 2)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 1'
    			elif ip.dstip == '10.2.2.20': #forward to h2
    				msgAction = of.ofp_action_output(port = 3)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 2'
    			elif ip.dstip == '10.3.3.30': #forward to h3
    				msgAction = of.ofp_action_output(port = 4)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 3'
    			elif ip.dstip == '10.5.5.50': #forward to h5
    				msgAction = of.ofp_action_output(port = 5)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 5'

   self.connection.send(msg)
   return

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
#code didnt work

            # return
          # #untrusted Host cannot send any IP traffic to the server
          # elif ip.dstip == '10.5.5.50': 
          #   self.connection.send(msg) #drop ip packet to host 5
          #   return
          # elif ip.dstip == '10.1.1.10': #forward to host 1
          #   msg.actions.append(of.ofp_action_output(port  = 1))
          #   self.connection.send(msg)
          # elif ip.dstip == '10.2.2.20' : #forward to host 2
          #   msg.actions.append(of.ofp_action_output(port = 2))
          #   self.connection.send(msg)
          # elif ip.dstip == '10.3.3.30': #forward to host 3
          #   msg.actions.append(of.ofp_action_output(port = 3))
          #   self.connection.send(msg)



    #if port on the switch is not 8 (from the untrusted host) allow traffic flow    
    ''' elif:  
      if ip.dstip == '123.45.67.89': #forward to h4
        msg.action.append(of.ofp_action_output(port  = 1))
				#print 'sent o host 4'
    	elif ip.dstip == '10.1.1.10': #forward to h1
        msg.action.append(of.ofp_action_output(port  = 2))
				#print 'sent o host 1'
    	elif ip.dstip == '10.2.2.20': #forward to h2
        msg.action.append(of.ofp_action_output(port  = 3))
    		#print 'sent o host 2'
    	elif ip.dstip == '10.3.3.30': #forward to h3
    		msg.action.append(of.ofp_action_output(port  = 4))
        #print 'sent o host 3'
    	elif ip.dstip == '10.5.5.50': #forward to h5
    		msg.action.append(of.ofp_action_output(port  = 5))
    		#print 'sent o host 5' '''
