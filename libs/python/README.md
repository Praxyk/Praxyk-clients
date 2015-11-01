Praxyk Python Library
======================

### Overview
To simplify interaction with the Praxyk API, we have written a python library that wraps around it and is free to use. This library allows one to log into their Praxyk account and perform any actions that they would otherwise be able to perform through either our website or raw call to our API. This document outlines the requirements for installing the python bindings, provides documentation for the various components of the library, and ends with some examples of how to use everything.


### Install

To get the latest stable version of the client libraries, use the following commands.

```sh
git clone http://github.com/jhallard/praxyk-clients.git
cd praxyk-clients
```

To install all of the libraries and client scripts, simply run

```sh
./configure
./install
```

If you only want to install the python library

```sh
cd libs/python
./install
```



### Documenation

Below is the complete documentation for all of the classes in this library. The classes and functions contained below will follow the general design and structure of the API as defined in our API documentation, i.e. `User.get(user_id=4)` performs a request to `api.praxyk.com/users/4`.
