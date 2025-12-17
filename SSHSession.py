import paramiko
import os
import posixpath
from stat import S_ISDIR

class SSHSession:
    def __init__(self, host, port, username, password, key_path=None, passphrase=None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        pkey = None
        if key_path:
            try:
                pkey = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            except paramiko.ssh_exception.PasswordRequiredException:
                raise ValueError("Private key requires a passphrase")
            except paramiko.ssh_exception.SSHException:
                raise ValueError("Unsupported key type or invalid key file")

        self.client.connect(hostname=host, port=port, username=username, password=password, pkey=pkey)
        self.sftp = self.client.open_sftp()

    def sftp_walk(self, remotepath):
        """Generator to walk through remote directories recursively"""
        files = []
        folders = []
        for f in self.sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        if files:
            yield remotepath, files
        for folder in folders:
            new_path = posixpath.join(remotepath, folder)
            for x in self.sftp_walk(new_path):
                yield x

    def put(self, localfile, remotefile):
        """Upload a single file"""
        self.sftp.put(localfile, remotefile)

    def put_all(self, localpath, remotepath):
        """Upload a directory recursively"""
        for root, dirs, files in os.walk(localpath):
            rel_root = os.path.relpath(root, localpath)
            remote_root = posixpath.join(remotepath, rel_root) if rel_root != "." else remotepath

            try:
                self.sftp.mkdir(remote_root)
            except IOError:
                pass  # directory may already exist

            for file in files:
                local_file = os.path.join(root, file)
                remote_file = posixpath.join(remote_root, file)
                self.put(local_file, remote_file)

    def get(self, remotefile, localfile):
        """Download a single file"""
        self.sftp.get(remotefile, localfile)

    def get_all(self, remotepath, localpath):
        """Download a remote directory recursively"""
        os.makedirs(localpath, exist_ok=True)

        for remote_dir, files in self.sftp_walk(remotepath):
            rel_dir = posixpath.relpath(remote_dir, remotepath)
            local_dir = os.path.join(localpath, rel_dir) if rel_dir != "." else localpath

            try:
                os.makedirs(local_dir, exist_ok=True)
            except Exception as e:
                print("Error:", e)
                continue

            for file in files:
                remote_file = posixpath.join(remote_dir, file)
                local_file = os.path.join(local_dir, file)
                try:
                    self.sftp.get(remote_file, local_file)
                except FileNotFoundError:
                    print(f"Remote file not found: {remote_file}")
                except Exception as e:
                    print(f"Failed to download {remote_file}: {e}")

    def executeCommand(self, command, sudo=False):
        """Execute a command on the remote server"""
        feed_password = False
        if sudo and self.username != "root":
            command = f"sudo -S -p '' {command}"
            feed_password = self.password is not None and len(self.password) > 0

        stdin, stdout, stderr = self.client.exec_command(command)

        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()

        return stdout.readlines()

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
