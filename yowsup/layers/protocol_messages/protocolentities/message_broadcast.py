from .message import MessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
import time


class BroadcastMessageProtocolEntity(ImageDownloadableMediaMessageProtocolEntity):
    def __init__(self, jids, _type):
        # Provide a temporary 'to' field for the init
        broadcastTime = int(time.time() * 1000)
        super(BroadcastMessageProtocolEntity, self).__init__(
            _type,
            to="%s@broadcast" % broadcastTime)
        self.setBroadcastProps(jids)

    def setBroadcastProps(self, jids):
        assert type(jids) is list, \
            "jids must be a list, got %s instead." % type(jids)
        self.jids = jids

    def isBroadcast(self):
        return True

    def toProtocolTreeNode(self):
        node = super(BroadcastMessageProtocolEntity, self).toProtocolTreeNode()
        toNodes = [ProtocolTreeNode("to", {"jid": jid}) for jid in self.jids]
        broadcastNode = ProtocolTreeNode("broadcast", children=toNodes)
        node.addChild(broadcastNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = BroadcastMessageProtocolEntity
        jids = [toNode.getAttributeValue("jid") for toNode in
                node.getChild("broadcast").getAllChildren()]
        entity.setBroadcastProps(jids)
        return entity
