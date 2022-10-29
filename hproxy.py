import subprocess
import uuid
import os
import time


class HAProxyConfig:
    """
    HAProxyConfig represents an HAProxy configuration file but with special features!
    """
    def __init__(self, config, raise_on_error=True):
        self.config = config
        self.raise_on_error = raise_on_error
        self.path = '/tmp/haproxy-test-{}'.format(str(uuid.uuid4()))  # Configurations are written to a temporary path.

    def test(self):
        """
        Test the configuration by launching the HAProxy executable with -c -f parameters
        """
        with open(self.path, 'w') as fp:
            fp.write(self.config)
        proc = subprocess.Popen(['haproxy', '-c', '-f', self.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.communicate()
        os.remove(self.path)
        
    def __str__(self):
        return self.config

    def __len__(self):
        return len(self.config)

class Templater:


    def __init__(self, use_stats=True, global_section=None, defaults_section=None,
            listen_sections=None, frontend_sections=None, backend_sections=None):

        self.context = dict(sections=list())

    def render(self):
        return HAProxyConfig(self.template.render(**self.context))


class HAProxyProcess:
    """
    Manage an HAProxy Process.
    """

    def __init__(self, daemon=False, work_dir='/tmp/haproxy-python'):
        self.daemon = daemon
        self.running = False
        self.pid_path = None
        self.pid = None
        self.work_dir = work_dir
        if daemon:
            os.makedirs(self.work_dir, exist_ok=True)
            self.pid_path = self.work_dir + '/haproxy.pid'

    def _check_pid(self):
        try:
            with open(self.pid_path, 'r') as fp:
                pid = fp.read().strip('\n')
                if pid:
                    try:
                        os.kill(int(pid), 0)
                    except OSError:
                        self.running = False
                    else:
                        self.running = True
                        self.pid = int(pid)
        except FileNotFoundError:
            self.running = False

    def _start_daemon(self):
        proc = subprocess.Popen(
            ['haproxy', '-f', self.work_dir + '/haproxy.cfg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        proc.communicate()
        self._check_pid()

    def _reload_daemon(self):
        proc = subprocess.Popen(
            ['haproxy', '-f', self.work_dir + '/haproxy.cfg', '-p', str(self.pid_path), '-st', str(self.pid)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        proc.communicate()
        self._check_pid()

    def _stop_daemon(self):
        os.kill(self.pid, 15)
        time.sleep(1)

    def _start_foreground(self):
        pass

    def _write_config(self, config):
        with open(self.work_dir + '/haproxy.cfg', 'w') as fp:
            fp.write(str(config))



    def stop(self):
        if self.daemon:
            self._check_pid()
            self._stop_daemon()