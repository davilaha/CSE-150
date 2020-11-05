# Alex Davila
# CSE150/L
# Chen Qian
# Computer Networks
# Final Project -  Implementing a Router 
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
# comparisons in this way. So I use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, I replace <PORT> with the port number the 
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
    # The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # I use these to determine where a packet came from. To figure out where a packet 
    # is going, I use the IP header information.

    #ofp_flow_mod properties from Lab3
    msg = of.ofp_flow_mod() #create packet out message
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 400
    msg.hard_timeout = 400
    msg.data = packet_in

    #packet type boolean
    ip = packet.find('ipv4')
    icmp = packet.find('icmp')
    print('this')
    # if ip is None:
      
      #print 'non-ip, flooded'

    if ip is not None:
      print('ip')
      if switch_id is 1:
        print('1')
        if port_on_switch is 8: 
          msg.actions.append(of.ofp_action_output(port = 1))
          self.connection.send(msg)
        elif port_on_switch is 1: #from s4
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)

      elif switch_id is 2:
        if port_on_switch is 8: #from host 2 
          msg.actions.append(of.ofp_action_output(port = 1))
          self.connection.send(msg)
        elif port_on_switch is 1: #from s4
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)
      
      elif switch_id is 3: 
        print('3')
        if port_on_switch is 8: #from host 3
          msg.actions.append(of.ofp_action_output(port = 1))
          self.connection.send(msg)
        elif port_on_switch is 1: 
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)
      
      elif switch_id is 5:
         if port_on_switch is 8:
            msg.actions.append(of.ofp_action_output(port = 1))
            self.connection.send(msg)
         elif port_on_switch is 1:
            msg.actions.append(of.ofp_action_output(port = 8)) #send to host 5
            self.connection.send(msg)

      elif switch_id is 4:
        if port_on_switch is 8:
          #blocking ICMP traffic from the untrusted host to anywhere internally
          if icmp is not None: 
            print('4')
            if ip.srcip=="123.45.67.89":
              self.connection.send(msg)
            else:
              msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
              self.connection.send(msg)
          else:
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
            

        else:
          msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
          self.connection.send(msg)
    else:
      print('no ip')
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)


    # self.connection.send(msg)
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




