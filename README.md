# pymt

![](/assets/dashboard1.png)

## Python mass-transport.

It is a common fact that many mass transport companies do not have a publicly available `API` for their `telematics`, but offer it in their various websites.
Pymt is a Python module built to `scrape` means of mass transport telematics webpages on will.

It aims to be as modular as possible, and has a different module for each mmt company. The user can then request the specific telematics from it.

## Support

It currently only supports OASTH, a Thessaloniki-based bus company, which the module was initialy built for. We hope to support more in the future with the help of various people that need it. There really is a need for an open source solution for this problem.

## Standard

The goal is to standardize a module, for every one of them to have the same structure and functionality. The goal is to make the system plug-and-play, and for developers to use it effortlessly. 

e.g: `get_stop_arivals()` will return a list of every bus name and arival time corresponds to a bus stop given.