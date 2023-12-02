## Internet programming

The project presents an electronic library that allows simple management of a collection of books and viewing operations 
performed by specific users using a special administrator account.

### RUN

This project is base on booting through Docker containerization.

1. You have to fill **config.ini.example** and change it name to **config.ini**
2. To run app use command blow:
```shell
docker-compose up 
```

### DEBUGGING ( DEVELOPERS )

If you want to run debug mode, it is recommended to run database and flask app separately.

1. Change **host** in **[mongo]** section from **mongo** to **localhost**
2. You can also enable debug mode in **[app]** section by change False to True.
3. Comment flask section in **docker-compose.yml** and run only MongoDB containers by command docker-compose up
   ( if you previously ran production version, please rebuild compose image )/
4. Navigate to Library directory and run below command:
```shell
python app.py
```

