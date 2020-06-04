import paramiko
import os
from stat import S_ISDIR

#Code taken from  https://gist.githubusercontent.com/johnfink8/2190472/raw/1e42f1caf3f4e0be16b712df7192a2475f5d4f48/ssh.py
class SSHSession(object):
	def __init__(self, host, port, username, password, key=None, passphrase=None):
		self.username = username
		self.password = password
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.client.connect(host, port, username=username, password=password, pkey=key)
		self.sftp = self.client.open_sftp()

	def sftp_walk(self, remotepath):
		path=remotepath
		files=[]
		folders=[]
		for f in self.sftp.listdir_attr(remotepath):
			if S_ISDIR(f.st_mode):
				folders.append(f.filename)
			else:
				files.append(f.filename)
		if files:
			yield path, files
		for folder in folders:
			new_path=os.path.join(remotepath,folder)
			for x in self.sftp_walk(new_path):
				yield x

	def put(self,localfile,remotefile):
		self.sftp.put(localfile,remotefile)

	def put_all(self,localpath,remotepath):
		#os.chdir(os.path.split(localpath)[0]) //not working so remove it
		parent=os.path.split(localpath)[1]
		for walker in os.walk(parent):
			try:
				self.sftp.mkdir(os.path.join(remotepath,walker[0]))
			except:
				pass
			for file in walker[2]:
				self.put(os.path.join(walker[0],file),os.path.join(remotepath,walker[0],file))

	def get(self,remotefile, localfile):
		self.sftp.get(remotefile,localfile)

	def get_all(self, remotepath, localpath):
		self.sftp.chdir(os.path.split(remotepath)[0])
		parent=os.path.split(remotepath)[1]
		try:
			os.makedirs(localpath)
		except:
			pass
		for walker in self.sftp_walk(parent):
			try:
				os.makedirs(os.path.join(localpath,walker[0]))
			except:
				pass
			for file in walker[1]:
				try:
					self.sftp.get(os.path.join(walker[0],file),os.path.join(localpath,walker[0],file))
				except:
					raise

	def close(self):
		if self.client is not None:
			self.client.close()
			self.client = None

	def executeCommand(self, command, sudo=False):
		feed_password = False
		if sudo and self.username != "root":
			command = "sudo -S -p '' %s" % command
			feed_password = self.password is not None and len(self.password) > 0
		stdin, stdout, stderr = self.client.exec_command(command)
		if feed_password:
			stdin.write(self.password + "\n")
			stdin.flush()
		'''return {'out': stdout.readlines(), 
				'err': stderr.readlines(),
				'retval': stdout.channel.recv_exit_status()}'''
		return stdout.readlines()