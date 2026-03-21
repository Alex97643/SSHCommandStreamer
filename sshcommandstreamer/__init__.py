
import paramiko
from typing import List, Optional
import os
import re

# Dynamically extract version from pyproject.toml
def _get_version():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pyproject_path = os.path.join(root, "pyproject.toml")
    try:
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "unknown"

__version__ = _get_version()


class SSHCommandStreamer:
    """
    SSHCommandStreamer allows executing multiple commands on a remote server via SSH,
    streaming output in real-time and handling sequential execution.
    """
    def __init__(self, hostname: str, username: str, password: Optional[str] = None, port: int = 22, abort_on_error: bool = False):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.abort_on_error = abort_on_error
        self.client: Optional[paramiko.SSHClient] = None
        print(f"SSHCommandStreamer version {__version__} initialized (abort_on_error={self.abort_on_error})")

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect_kwargs = {
            'hostname': self.hostname,
            'port': self.port,
            'username': self.username,
        }
        if self.password is not None:
            connect_kwargs['password'] = self.password
        # Allow agent and key-based authentication if password is None
        self.client.connect(**connect_kwargs, allow_agent=True, look_for_keys=True)

    def execute_commands(self, commands: List[str]):
        if not self.client:
            raise RuntimeError("SSH client not connected. Call connect() first.")
        for command in commands:
            print(f"\n####################################")
            print(f"[Running] {command}")
            print(f"#####################################")
            if command.startswith("!UPLOAD!"):
                # Parse upload command: !UPLOAD! [local file path] [remote path]
                parts = command.split(maxsplit=2)
                if len(parts) != 3:
                    print(f"[UPLOAD ERROR] Invalid syntax: {command}")
                    if self.abort_on_error:
                        print("[ABORT] Aborting due to error.")
                        break
                    continue
                local_path, remote_path = parts[1], parts[2]
                print(f"\n[Uploading] {local_path} -> {remote_path}")
                try:
                    self.upload_file(local_path, remote_path)
                    print(f"[Upload Success] {local_path} -> {remote_path}")
                except Exception as e:
                    print(f"[Upload Failed] {e}")
                    if self.abort_on_error:
                        print("[ABORT] Aborting due to error.")
                        break
                continue

            stdin, stdout, stderr = self.client.exec_command(command)
            # Stream stdout in real-time
            for line in iter(stdout.readline, ""):
                print(line, end="")
            # Stream stderr as well
            for line in iter(stderr.readline, ""):
                print(line, end="")
            exit_status = stdout.channel.recv_exit_status()
            print(f"[Exit status] {exit_status}")
            if exit_status != 0 and self.abort_on_error:
                print("[ABORT] Aborting due to error.")
                break

    def upload_file(self, local_path: str, remote_path: str):
        if not self.client:
            raise RuntimeError("SSH client not connected. Call connect() first.")
        sftp = self.client.open_sftp()
        try:
            # Expand ~ to remote home directory if present
            if remote_path == "~":
                remote_path = sftp.normalize("~")
            elif remote_path.startswith("~/"):
                home = sftp.normalize("~")
                rest = remote_path[2:]
                remote_path = home.rstrip("/") + "/" + rest.lstrip("/")
            # Remove any accidental double slashes
            while "//" in remote_path:
                remote_path = remote_path.replace("//", "/")
            print(f"[DEBUG] Final remote_path for upload: {remote_path}")
            sftp.put(local_path, remote_path)
        finally:
            sftp.close()

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
