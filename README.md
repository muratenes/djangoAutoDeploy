## # Info
Django auto deployment with nginx and gunicorn
## #Prerequisite
 - You should be firstly upload your website to github


#### Install the dependencies for server.
 - Prepare to server for deploy your django project
```sh
sudo apt-get update
sudo  apt-get install nginx python3-pip python3-dev git
sudo  apt-get install virtualenv
```

## # Django Requirements
- you must be create **requiments.txt** on your project folder and it's be contain 
 django requirements ex is below
 ```sh
       django==2.0
       Pillow==2.0
```
or just execute below command on local terminal for create requirements.txt
<pre>
 pip3 freeze -> requirements.txt
</pre>
### Bind Nginx And Gunicorn Config
you must be bind this fields on index.py example is below
 ```sh
      SiteConfig.site_folder_name = "site_folder_name"  # only site folder name ex: autoDeployDjango
    SiteConfig.project_name = "project_name"  # your site project name when created django-admin startproject mysite
    SiteConfig.domain_list = "domain_list"  # nginx domain list its must be string and 1 space each domain ex:"mydomain.com www.mydomain.com"
    SiteConfig.static_files_folder = "static_files_folder"  # django static file folder name ex:"staticfiles"
    SiteConfig.media_files_folder = "media_files_folder"  # django media file folder name ex:"media"
    SiteConfig.virtual_env_name = "virtual_env_name"  # django virtual environment  file folder name ex:"venv"
    SiteConfig.github_repo_url = "github_repo_url " # your web site github repo url  ex : "https://github.com/your_username/your_repo_url.git"
    SiteConfig.requirements_file_name = "requirements_file_name"  # this required for package requirements ex:"requirements.txt"
```

### How to delete old web site configuration on server ?
if you want to delete old nginx,gunicorn and other configuration  files on your server you must be run this command on 
main folder

 ```sh
      python3 manage.py delete-old
```

 
