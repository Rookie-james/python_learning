"""
    function: this script used to update offline image by sftp
    auth: wz
    time: 2019-8-5 14:32:00
    version: v1.0.0
"""

import paramiko
import os
from stat import S_ISDIR as isdir

def get_ssh(host, port, user_name, passwd):
    """
        function: this interface used to login server by user name and passwd
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user_name, passwd)

    return ssh

def sftp_connect(username, password, host, port=22):
    """
        function: this interface used to create conn of sftp
        parameter:
            username
            password
            host
            port
        return:
            client
            sftp
    """
    client = None
    sftp = None
    try:
        client = paramiko.Transport(host, port)
    except Exception as error:
        print(error)
    else:
        try:
            client.connect(username=username, password=password)
        except Exception as error:
            print(error)
        else:
            sftp = paramiko.SFTPClient.from_transport(client)
    return client, sftp


def disconnect(client):
    """
        function: close the conn of sftp
        parameter:
            client
        return: True or false
    """
    try:
        client.close()
        return True
    except Exception as error:
        print(error)
        return False


def _check_local(local):
    """
        function: this interface used to check file or folder is exists at local ,if not ,create
        parameter: local  local path
    """
    if not os.path.exists(local):
        try:
            os.mkdir(local)
        except IOError as err:
            print(err)


def get(sftp, remote, local):
    """
        function: download file or folder from server
        param:
            sftp
            remote
            local
    """
    try:
        result = sftp.stat(remote)
    except IOError as err:
        error = '[ERROR %s] %s: %s' %(err.errno,os.path.basename(os.path.normpath(remote)),err.strerror)
        print(error)
    else:
        if isdir(result.st_mode):
            dirname = os.path.basename(os.path.normpath(remote))
            local = os.path.join(local, dirname)
            _check_local(local)
            for file in sftp.listdir(remote):
                sub_remote = os.path.join(remote, file)
                sub_remote = sub_remote.replace('\\', '/')
                get(sftp, sub_remote, local)
        else:
            if os.path.isdir(local):
                local = os.path.join(local, os.path.basename(remote))
            try:
                sftp.get(remote, local)
            except IOError as err:
                print(err)
            else:
                print('[get]', local, '<==', remote)


def put(sftp, local, remote):
    """
        function : upload file or folder to server
        param:
            sftp:
            local:
            remote:
    """

    def _is_exists(path, function):
        path = path.replace('\\', '/')
        try:
            function(path)
        except Exception as error:
            return False
        else:
            return True

    def _copy(sftp, local, remote):
        if _is_exists(remote, function=sftp.chdir):
            filename = os.path.basename(os.path.normpath(local))
            remote = os.path.join(remote, filename).replace('\\', '/')

        if os.path.isdir(local):
            _is_exists(remote, function=sftp.mkdir)
            for file in os.listdir(local):
                localfile = os.path.join(local, file).replace('\\', '/')
                _copy(sftp=sftp, local=localfile, remote=remote)

        if os.path.isfile(local):
            try:
                sftp.put(local, remote)
            except Exception as error:
                print(error)
                print('[put]', local, '==>', remote, 'FAILED')
            else:
                print('[put]', local, '==>', remote, 'SUCCESSED')

    if not _is_exists(local, function=os.stat):
        print("'" + local+"': No such file or directory in local")
        return False

    remote_parent = os.path.dirname(os.path.normpath(remote))
    if not _is_exists(remote_parent, function=sftp.chdir):
        print("'"+remote+"': No such file or directory in remote")
        return False
    _copy(sftp=sftp, local=local, remote=remote)


def main():
    # client, sftp = sftp_connect(username="root", password="root", host="192.168.1.251", port=22)

    # get(sftp, "/mnt/adasUserData/", "D:\\")
    # put(sftp, "D:/test.txt", "/mnt/adasUserData/")
    # disconnect(client)
    pass


if __name__ == "__main__":
    main()
