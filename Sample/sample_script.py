import os
import sys
# Ensure the project root is in sys.path for package import
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(script_dir, '..')))

import yaml
from sshcommandstreamer import SSHCommandStreamer

# Load server parameters from YAML file next to this script
yaml_path = os.path.join(script_dir, "server.yaml")

with open(yaml_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

host = config["host"]
user = config["user"]
pwd = config.get("password")
folder = config["folder"]

commands = [
    f"mkdir -p {folder}",
    f"ls -l {folder}",       
    f"!UPLOAD! {script_dir}/upload_test.txt {folder}/upload_test.txt",
    f"cat {folder}/upload_test.txt",
    f"echo 'file modified' >> {folder}/upload_test.txt",
    f"!DOWNLOAD! {folder}/upload_test.txt {script_dir}/download_test.txt",
    f"ls -l {folder}",
    f"cat {folder}/upload_test.txt",
   
   
]

streamer = SSHCommandStreamer(host, user, pwd, abort_on_error=True)
try:
    streamer.connect()
    streamer.execute_commands(commands)
except Exception as e:
    print(f"Execution failed: {e}")
finally:
    streamer.close()
