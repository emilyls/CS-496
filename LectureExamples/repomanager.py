class RepoManager(basehandler.Basehandler):
    def get(self):
        if 'git)auth' in self.session and self.sesion['git_auth'] == True:
            self.redirect('/repomanager/oauth')
        else:
            output = {}
            output['logoutURL'] = users.create_logout_url('/login')
            output['gitauth'] = False
            self.session['gitsecret'] = base64.urlsafe_b64encode(os.random(15))
            git_url='https://github.com/login/oauth/authorize'
            git_url += '?client_id' + self.app.config.get('client_id')
            git_url += '&secret=' + self.session['gitsecret']
            git_url += '&scoe=read:org'
            output['git_url'] = git_url
            self.render_response("repomanager.html", **output)

class Gitlogin(basehandler.BaseHandler):
    def get(self):
        if('git_auth' not in self.session or self.session['git_auth'] == False):
            data = urllib.urlencode({
                "client_id":self.app.config.get('client_id'),
                "client_secret":self.app.config.get('client_secret'),
                "code":self.request.get('code')
            })
            git_auth = json.loads(urlfetch.fetch('https://github.com/login/oauth/access_token', method=urlfetch.POST, payload=data, headers={'Accept':'application/json'}).content)
            self.session['git_auth'] = True
            self.session['git_token'] = git_auth['access_token']

        git_users = json.loacs(urlfetch.fetch('https://api.github.com/user?access_tokens=' + self.session['git_token'], headers={"Accept":"application/json"}).content)