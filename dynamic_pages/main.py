import webapp2

config = {'default-group':'base-data'}

app = webapp2.WSGIApplication([
    ('/', 'form.Add'),
    ('/edit', 'edit.Edit'),
    ('/view', 'view.View'),
], debug=True, config=config)
