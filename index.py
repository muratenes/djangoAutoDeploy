import sys

from models.configs import SiteConfig, SshConfig, GeneralConfigs
from os import system
import djangoConf
import privateConfigs


def bindSshConfigs():
    SshConfig.ssh_user = privateConfigs.ssh_user  # your server root privileges user ex : "root"
    SshConfig.ssh_ip = privateConfigs.ssh_ip  # your server ip address ex : "192.168.2.1"
    SshConfig.ssh_password = privateConfigs.ssh_password  # your server password ex:"myPassword123"


def bindSiteConfigs():
    SiteConfig.site_folder_name = privateConfigs.site_folder_name  # only site folder name ex: autoDeployDjango
    SiteConfig.project_name = privateConfigs.project_name  # your site project name when created django-admin startproject mysite
    SiteConfig.domain_list = privateConfigs.domain_list  # nginx domain list its must be string and 1 space each domain ex:"mydomain.com www.mydomain.com"
    SiteConfig.static_files_folder = privateConfigs.static_files_folder  # django static file folder name ex:"staticfiles"
    SiteConfig.media_files_folder = privateConfigs.media_files_folder  # django media file folder name ex:"media"
    SiteConfig.virtual_env_name = privateConfigs.virtual_env_name  # django virtual environment  file folder name ex:"venv"
    # SiteConfig.github_repo_url = privateConfigs.github_repo_url  # your web site github repo url  ex : "https://github.com/your_username/your_repo_url.git"
    SiteConfig.requirements_file_name = privateConfigs.requirements_file_name  # this required for package requirements ex:"requirements.txt"
    SiteConfig.github_user_name = privateConfigs.github_user_name
    SiteConfig.github_password = privateConfigs.github_password
    SiteConfig.github_repository_name = privateConfigs.github_repository_name
    print("site config writed")


def bindGeneralConfigs():
    """
    parent folder with all sites ex :"/var/www/vhost/" ex2:"/home/murat/"
    it's must be start with / and must be start with /
    :return:
    """
    GeneralConfigs.sites_container_folder = privateConfigs.sites_container_folder


"""
 bu dosya baştan yazıldığı için  change edilmiyor
"""


def changeScriptFields():
    with open('scripts/djangoDeployScript', 'r') as file:
        data = file.readlines()
        data.clear()
    # now change the 2nd line, note that you have to add a newline
    data.insert(0, 'cd %s \n' % GeneralConfigs.sites_container_folder)
    data.insert(1, 'mkdir %s \n' % SiteConfig.site_folder_name)
    data.insert(2, 'cd %s \n' % SiteConfig.site_folder_name)
    data.insert(3, 'git clone https://%s:%s@github.com/%s/%s.git .\n' % (SiteConfig.github_user_name, SiteConfig.github_password, SiteConfig.github_user_name, SiteConfig.github_repository_name))
    data.insert(4, 'rm -rf %s\n' % SiteConfig.virtual_env_name)
    data.insert(5, 'virtualenv -p python3 %s\n' % SiteConfig.virtual_env_name)
    data.insert(6, 'source %s/bin/activate\n' % SiteConfig.virtual_env_name)
    data.insert(7, 'pip3 install -r %s\n' % SiteConfig.requirements_file_name)
    data.insert(8, 'pip3 install gunicorn\n')
    # data.insert(9, 'sudo ufw allow 8000\n')
    # data.insert(10, 'python3 manage.py runserver 0.0.0.0:8000\n')  # for test localhost
    # data.insert(11, 'sleep 10\n')  # for waiting site test on ip_adres:8000
    data.insert(12, 'sudo lsof -t -i tcp:8000 | xargs kill -9\n')  # for kill port
    data.insert(13, 'deactivate\n')  # for kill port

    with open('scripts/djangoDeployScript', 'w') as file:
        file.writelines(data)
    print("======script file processing===")
    print(data)


def pushScriptToServer():
    print("script pushing to server")
    # system("sudo apt-get install sshpass")
    system("ssh %s@%s 'bash -s' < 'scripts/djangoDeployScript'" % (SshConfig.ssh_user, SshConfig.ssh_ip))


def prepareToServer():
    pass


def index():
    print("""
    ===================================================================
    =                                                                 =
    = Welcome to Django Auto Deployer created by github.com@muratenes 
    = > You should be firstly upload web site to  github
    = > Create requirements.txt and write to project requirements in project folder
    = > You must install server requirements
    =   -sudo apt-get update
    =   -sudo apt-get install nginx python3-pip python3-dev                                   =
    ===================================================================
    """)
    # bindSshConfigs()
    # bindSiteConfigs()
    # bindGeneralConfigs()
    # deleteServerOldConfAndData(SiteConfig, SshConfig, GeneralConfigs)

    djangoConf.setToDefaultScripts()
    prepareToServer()
    changeScriptFields()
    pushScriptToServer()
    djangoConf.createGunicornFile(SiteConfig, SshConfig, GeneralConfigs)
    djangoConf.createNginxFile(SiteConfig, SshConfig, GeneralConfigs)
    djangoConf.pushToNginxGunicornFileToServer(SiteConfig, SshConfig, GeneralConfigs)
    system("ssh %s@%s 'cd /etc/systemd/system/;sudo systemctl restart gunicorn_%s.service'" % (SshConfig.ssh_user, SshConfig.ssh_ip, SiteConfig.site_folder_name))
    system("ssh %s@%s 'cd /etc/systemd/system/;sudo systemctl enable gunicorn_%s.service'" % (SshConfig.ssh_user, SshConfig.ssh_ip, SiteConfig.site_folder_name))
    system("ssh %s@%s 'systemctl restart nginx.service'" % (SshConfig.ssh_user, SshConfig.ssh_ip))
    system("ssh %s@%s 'systemctl daemon-reload'")
    system("ssh %s@%s 'cat /var/log/nginx/error.log'" % (SshConfig.ssh_user, SshConfig.ssh_ip))

    system("ssh %s@%s 'sudo ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled'" % (SshConfig.ssh_user, SshConfig.ssh_ip, SiteConfig.site_folder_name))


def deleteServerOldConfAndData(siteConfig, sshConfig, generalConfig):
    print("====== WARNING : DELETED OLD CONF FILES =======")
    djangoConf.replaceText("scripts/deleteOldDatasScript", "parent_folder", generalConfig.sites_container_folder)
    djangoConf.replaceText("scripts/deleteOldDatasScript", "site_folder", siteConfig.site_folder_name)
    with open('scripts/deleteOldDatasScript', 'r') as file:
        data = file.readlines()
        data.clear()
    system("ssh %s@%s 'bash -s' < 'scripts/deleteOldDatasScript'" % (sshConfig.ssh_user, sshConfig.ssh_ip))
    djangoConf.setToDefaultScripts()


if __name__ == '__main__':
    bindSshConfigs()
    bindSiteConfigs()
    bindGeneralConfigs()
    if int(sys.argv.__len__()) > 1:
        print(sys.argv)
        for i, arg in enumerate(sys.argv):
            if i > 0:
                if str(arg) == "delete-old":
                    deleteServerOldConfAndData(SiteConfig, SshConfig, GeneralConfigs)
            # args = [(sys.argv[1]), (sys.argv[2])]
    else:
        index()

        # index()
