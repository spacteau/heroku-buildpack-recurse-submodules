# Git submodules importation buildpack (Heroku-like style)

Heroku buildpack containing a 'bin' directory with scripts enabling to recursively clone Git submodules defined 
in a .gitmodules file. This 'bin' folder is to be saved in an independent public Git repository in order to be able to 
configure its remote access from Heroku server.