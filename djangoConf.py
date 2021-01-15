#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
from tempfile import mkstemp

from models.configs import SiteConfig, SshConfig, GeneralConfigs
from os import system
import os
from os import fdopen, remove
from shutil import move




def createGunicornFile(siteConfig, sshConfig, generalConfig):
    print("====== configuring to Gunicorn file =======")
    print("created Gunicorn File => /etc/systemd/system/gunicorn_%s.service" % siteConfig.site_folder_name)
    replaceText("scripts/gunicornText", "parent_folder", generalConfig.sites_container_folder)
    replaceText("scripts/gunicornText", "site_folder", siteConfig.site_folder_name)
    replaceText("scripts/gunicornText", "venv_folder", siteConfig.virtual_env_name)
    replaceText("scripts/gunicornText", "project_name", siteConfig.project_name)
    replaceText("scripts/gunicornText", "user_name", sshConfig.ssh_user)
    with open('scripts/gunicornText', 'r') as file:
        data = file.readlines()
        data.clear()


def createNginxFile(siteConfig, sshConfig, generalConfig):
    print("====== configuring to Nginx file =======")
    print("created => /etc/nginx/sites-available/%s" % siteConfig.site_folder_name)
    replaceText("scripts/nginxText", "site_folder", siteConfig.site_folder_name)
    replaceText("scripts/nginxText", "domain_name", siteConfig.domain_list)
    replaceText("scripts/nginxText", "parent_folder", generalConfig.sites_container_folder)
    replaceText("scripts/nginxText", "venv_folder", siteConfig.virtual_env_name)
    replaceText("scripts/nginxText", "project_name", siteConfig.project_name)
    replaceText("scripts/nginxText", "static_file_folder", siteConfig.static_files_folder)
    with open('scripts/nginxText', 'r') as file:
        data = file.readlines()
        data.clear()


def setToDefaultScripts():
    print("====== configuring to Nginx/Gunicorn file default settings =======")
    with open("scripts/defaultScripts/deleteOldDatasScript(Not Edit)") as f:
        lines = f.readlines()
        lines = [l for l in lines]
        with open("scripts/deleteOldDatasScript", "w") as f1:
            f1.writelines(lines)
    with open("scripts/defaultScripts/gunicornText(Not Edit)") as f:
        lines = f.readlines()
        lines = [l for l in lines]
        with open("scripts/gunicornText", "w") as f1:
            f1.writelines(lines)
    with open("scripts/defaultScripts/nginxText(Not edit)") as f:
        lines = f.readlines()
        lines = [l for l in lines]
        with open("scripts/nginxText", "w") as f1:
            f1.writelines(lines)


def pushToNginxGunicornFileToServer(siteConfig, sshConfig, generalConfig):
    system("ssh %s@%s 'bash -s' < 'scripts/gunicornText'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    system("ssh %s@%s 'sudo systemctl start gunicorn_%s.service;sudo systemctl enable gunicorn_%s.service;exit'" % (sshConfig.ssh_user, sshConfig.ssh_ip, siteConfig.site_folder_name, siteConfig.site_folder_name))
    system("ssh %s@%s 'bash -s' < 'scripts/nginxText'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    system("ssh %s@%s 'sudo ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled'" % (SshConfig.ssh_user, SshConfig.ssh_ip, SiteConfig.site_folder_name))
    system("ssh %s@%s 'sudo systemctl restart nginx'" % (sshConfig.ssh_user, sshConfig.ssh_ip))


def replaceText(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
                print("" + pattern + " changed to ", "[", subst, "]")
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)


def index():
    pass


if __name__ == '__main__':
    index()
