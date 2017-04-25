from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import \
        BroadcastMessageProtocolEntity
from yowsup.common.tools import Jid
import threading
import logging
logger = logging.getLogger(__name__)

from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_media.protocolentities import \
        ImageDownloadableMediaMessageProtocolEntity as ImageEntity
from yowsup.layers.protocol_media.protocolentities import \
        RequestUploadIqProtocolEntity


class BroadcastLayer(YowInterfaceLayer):

    # This message is going to be replaced by the @param message in
    # YowsupSendStack construction
    # i.e. list of (phone_list, media, caption) tuples
    PROP_MESSAGE = "org.openwhatsapp.yowsup.prop.broadcastclient.message"

    def __init__(self):
        super(BroadcastLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()
        self.initial_jid = None

    # Call back function when there is a successful connection to whatsapp
    # server
    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        phones, self.file_path, self.caption = self.getProp(self.__class__.PROP_MESSAGE)
        self.jids = [Jid.normalize(phone) for phone in phones]
        self.request_image_upload(self.jids[0], self.file_path)


    # after receiving the message from the target number, target number will
    # send a ack to sender(us)
    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        # if the id match the id in ackQueue, then pop the id of the message
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            self.lock.release()
            print("Message sent")
            raise KeyboardInterrupt()

        self.lock.release()

    def request_image_upload(self, jid, file_path):
        entity = RequestUploadIqProtocolEntity("image", filePath=file_path)
        self._sendIq(entity, self.on_upload_request_result,
            self.on_upload_request_error)

    def on_upload_request_result(self, result, entity):

        self.upload_url = result.getUrl()

        if result.isDuplicate():
            self.send_media()
            return

        mediaUploader = MediaUploader(
                self.jids[0],
                self.getOwnJid(),
                self.file_path,
                self.upload_url,
                result.getResumeOffset(),
                self.on_upload_success,
                self.on_upload_error,
                self.on_upload_progress)
        mediaUploader.start()

    def on_upload_request_error(self, error, entity):
        print("Error requesting upload url")

    def on_upload_success(self, *args, **kwargs):
        self.send_media()

    def send_media(self):
        message = BroadcastMessageProtocolEntity.fromFilePath(
            self.file_path,
            self.upload_url,
            None,
            self.jids[-1],
            caption=self.caption)
        # Horrible hack because of static methods instead of class methods.
        message.__class__ = BroadcastMessageProtocolEntity
        message.setBroadcastProps(self.jids)
        self.ackQueue.append(message.getId())
        self.toLower(message)

    def on_upload_error(self, *args, **kwargs):
        print("Upload file failed!")

    def on_upload_progress(self, filePath, jid, url, progress):
        pass
