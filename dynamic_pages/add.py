from google.appengine.ext.webapp import blobstore_handlers

import form


class Add(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
            form.Add(self.request, self.response).post()
