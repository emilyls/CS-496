from google.appengine.ext.webapp import blobstore_handlers

import admin


class AddChannel(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('icon')
        if upload_files != []:
            blob_info = upload_files[0]
            admin.Admin(self.request, self.response).post(icon_key=blob_info.key())
        else:
            admin.Admin(self.request, self.response).post()
