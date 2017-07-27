# movie-catalog-app

This catalog web app allows users to create, read, update and delete items. To be more specific, users can log in with their Google account, add movies in a specific category to the database, edit the information of the movies and can also delete the movie they added. Users can only modify the movies which are created by themselves. 

**This project makes use of the Linux-based virtual machine (VM), you'll need VirtualBox, Vagrant installed in advance.**

## Start Guide:
* Put all files into a folder "catalog" inside vagrant subdirectory
* From your terminal, inside the vagrant subdirectory, run the command vagrant up
* When vagrant up is finished running, run vagrant ssh to log in to your Linux VM
* Inside the VM, change directory to \vagrant (cd \vagrant), and then cd catalog
* Download and run command python catalog_init.py to populate database with movies
* Run command python application.py
* Open a browser and enter localhost:8000


![screen shot 2017-07-23 at 11 09 17 am](https://user-images.githubusercontent.com/20274213/28572278-4be766d4-7114-11e7-8df7-3a2ed7b68c7e.png)
![screen shot 2017-07-26 at 8 38 35 am](https://user-images.githubusercontent.com/20274213/28670069-019099e2-72a5-11e7-9ff5-a55cb687a4bf.png)
![screen shot 2017-07-26 at 8 39 47 am](https://user-images.githubusercontent.com/20274213/28670081-12fc455a-72a5-11e7-8562-a1b210a15309.png)
![screen shot 2017-07-26 at 8 35 41 am](https://user-images.githubusercontent.com/20274213/28670096-22736dce-72a5-11e7-8273-b856bdd547bf.png)
![screen shot 2017-07-26 at 8 40 01 am](https://user-images.githubusercontent.com/20274213/28670109-2e459b68-72a5-11e7-8752-e3509806ca59.png)
![screen shot 2017-07-26 at 8 40 36 am](https://user-images.githubusercontent.com/20274213/28670116-3a78e6ec-72a5-11e7-82a1-24d95ca21e2e.png)
