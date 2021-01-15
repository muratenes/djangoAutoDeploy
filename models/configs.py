class SshConfig():
    ssh_user = None
    ssh_password = None
    ssh_ip = None
    ssh_port = None

    def print(self):
        print("""
        ======= SSH Configs =========
        ssh User  = %s
        ssh_password = %s
        ssh_ip =  %s
        ssh_port =  %s
        """)


class SiteConfig():
    site_folder_name = None
    project_name = None  # such as CMS
    domain_list = None  # arasında 1 boşluk bırakarak yazınız
    static_files_folder = None
    media_files_folder = None
    virtual_env_name = None
    requirements_file_name = None
    github_repo_url = None
    github_user_name = None
    github_password = None
    github_repository_name = None


class GeneralConfigs():
    sites_container_folder = None
