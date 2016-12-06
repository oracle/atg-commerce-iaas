# The MIT License (MIT)
#
# Copyright (c) 2016 Oracle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import StringIO
import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pprint import pprint
import shutil
from subprocess import Popen, PIPE, STDOUT, CalledProcessError
import sys
import tempfile
import urllib2


log = logging.getLogger(__name__)
DEFAULT_LOG_FILE = '/var/log/bmc-init/opc-solaris-init.log'

base_os_url = "http://169.254.169.254/opc/v1/instance/metadata/script"

MARKER_FILE = os.path.expanduser("~/.opc_installer_executed")
 
_NO_DEFAULT = object()


def setup_logger():
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)

    # create the log directory if it does not exist
    log_dir = os.path.dirname(DEFAULT_LOG_FILE)
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    # create a rotating file handler. rotate log file every 10MB
    file_handler = RotatingFileHandler(DEFAULT_LOG_FILE, maxBytes=(10 * 1024 * 1024), backupCount=10)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s'))
    root_logger.addHandler(file_handler)
    log.info("Established file logger to '%s'", DEFAULT_LOG_FILE)

def needs_to_run():
    # hostname = hostname.strip()
    if os.path.exists(MARKER_FILE):
        log.info("does not need to run")
        return False

    log.info("Writing marker file: %s", MARKER_FILE)
    with open(MARKER_FILE, 'w') as f:
        f.write(str(datetime.datetime.now()))

    return True
    
def run_and_wait(command, fail_on_error=False, **kwargs):
    """
    Run a shell command and wait for it to finish.

    Stdout and stderr are captured together.
    TODO: look into capturing stdout and stderr separately.

    DOES NOT SUPPORT stdinput.

    :param command: A string or list of strings indicating the command to run. In the same style as subprocess.
    :param fail_on_error: Boolean, if true, a CalledProcessError will be raised if the return code is not 0.
    :returns: A shell_cmd.Result object containing the original command, its return code, and output
    """

    # cast all command elements to str
    if isinstance(command, list):
        command = [str(a) for a in command]

    log.info("Executing %s fail_on_error=%s additional subprocess args %s", command, fail_on_error, kwargs)

    # a string buffer with better performance than simply appending strings
    output_buffer = StringIO.StringIO()
    # start the process
    try:
        proc = Popen(command, stdin=open(os.devnull), stdout=PIPE, stderr=STDOUT, **kwargs)

        # while lines are avilable on stdout, add them to the buffer
        for line in iter(proc.stdout.readline, ''):
            output_buffer.write(line)

        # wait for process termination
        proc.wait()

        log.info("Execution finished.")

        # if the fail on error flag was set, and the result was not ok, raise it
        if fail_on_error and proc.returncode != 0:
            log.error("Execution failed. Return code %d != 0. Raising exception. Output: %s",
                      proc.returncode, output_buffer.getvalue())
            raise CalledProcessError(proc.returncode, command)

        # return encapsulated content
        return Result(command, proc.returncode, output_buffer.getvalue())
    except OSError as e:
        # An OSError will be raised if shell=False and the executable (the first arg) cannot be found
        if not fail_on_error:
            return Result(command, 127, "command not found: %r" % command[0])
        log.error("Reraising OSError: %s" % e)
        raise


class Result(object):
    """
    A simple structure for accessing results of a shell command run.
    """

    def __init__(self, command, return_code, output):
        self.command = command
        self.return_code = return_code
        self.output = output

    @property
    def failed(self):
        return self.return_code != 0

    @property
    def succeeded(self):
        return not self.failed

    def reraise(self):
        if self.succeeded:
            log.warn("Execution succeeded, not reraising anything.")
            return
        log.error("Execution failed. Return code %d != 0. Raising exception. Output: %s", self.return_code, self.output)
        raise CalledProcessError(self.return_code, self.command)
    
def _get(path):
    try:
        return urllib2.urlopen(path).read().strip()
    except urllib2.HTTPError as e:
        if e.code == 404:
            return
        raise

def exec_boot_script(script_to_exec):
    # store the script in a temporary file, and then execute it
    temp_dir = tempfile.mkdtemp()
    try:
        script_file_name = os.path.join(temp_dir, "script.sh")
        with open(script_file_name, "w") as script_file:
            script_file.write(script_to_exec)
        log.info("Wrote script file in folder %s.", temp_dir)
        os.chmod(script_file_name, 0o700)
        log.info("Executing %s", script_file_name)
        try:
            r = run_and_wait(script_file_name, shell=True, fail_on_error=False)
            if r.succeeded:
                log.info("Script ran successfully. Output: %s", r.output.strip())
            else:
                log.error("Script failed with code %s but ignoring error due to faileonerror=False. Output: %s",
                         r.return_code, r.output.strip())
        except CalledProcessError as e:
            sys.exit(e.returncode)
    finally:
        shutil.rmtree(temp_dir)                    

setup_logger()

try:            
    data = _get(base_os_url)
    if data:
        if needs_to_run():
            exec_boot_script(data)
except:
    log.error("unable to get script data")    

