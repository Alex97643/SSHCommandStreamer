# SSH Command Streamer

**Version:** 1.0.1

This project is a simple SSH command streamer that allows you to execute commands on a remote server and stream the output in real-time, waiting for each command to finish before sending the next. It is built using Python and the Paramiko library.

## Features
- Execute commands on a remote server via SSH
- Stream the output of the commands in real-time
- Handle multiple commands sequentially
- Ability to specify the remote server, username, and password
- Upload files to the remote server using a special command

## Error Handling

You can configure SSHCommandStreamer to abort execution if any command fails by setting the `abort_on_error` flag when creating the instance:

```python
streamer = SSHCommandStreamer(host, user, pwd, abort_on_error=True)
```

If `abort_on_error` is True, the command sequence will stop at the first error and no further commands will be executed.

**Default:** `abort_on_error=False` (continues on error)

## Usage

### Basic Example
```python
from SSHCommandStreamer import SSHCommandStreamer

host = "<remote_host>"
user = "<username>"
pwd = "<password>"  # or None for key-based auth
commands = [
    "!UPLOAD! local_file.txt ~/remote_file.txt",  # Upload a file
    "echo 'Hello from remote!'",
    "uname -a",
    "whoami",
    "ls -l ~"
]

streamer = SSHCommandStreamer(host, user, pwd)
try:
    streamer.connect()
    streamer.execute_commands(commands)
finally:
    streamer.close()
```

### Special Commands
- To upload a file, add a command in the form:
  - `!UPLOAD! <local_file_path> <remote_file_path>`
  - Example: `!UPLOAD! sample_upload.txt ~/sample_upload.txt`
- The `~` in the remote path will be expanded to the remote user's home directory.

## API

### SSHCommandStreamer
#### Constructor
```python
SSHCommandStreamer(hostname: str, username: str, password: Optional[str] = None, port: int = 22)
```
- `hostname`: Remote server address
- `username`: SSH username
- `password`: SSH password (or None for key-based authentication)
- `port`: SSH port (default 22)

#### Methods
- `connect()`: Establishes the SSH connection.
- `execute_commands(commands: List[str])`: Executes a list of commands sequentially. Handles `!UPLOAD!` commands for file upload.
- `close()`: Closes the SSH connection.
- `upload_file(local_path: str, remote_path: str)`: Uploads a file to the remote server. Expands `~` in the remote path to the user's home directory.

## Requirements
- Python 3.7+
- paramiko

## Installation
```
pip install paramiko
```

## License
MIT License

