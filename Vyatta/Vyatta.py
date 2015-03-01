#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takech9203'

import re
import urllib
import requests
requests.packages.urllib3.disable_warnings()    # Surpress "InsecureRequestWarning" warning
import Vyatta
import vyuser

class VyattaControl(object):
    """
    Provides methods to show and modify Vyatta status and configurations.
    """

    def __init__(self, urlBase, user, passwd):

        self.urlBase = urlBase
        self.urlConfBase = urlBase + 'rest/conf'
        self.urlOpBase = urlBase + 'rest/op'
        self.user = user
        self.passwd = passwd


    def getOpId(self, urlOpId):
        """
        Get the operation id, which is substring of the Location header in HTTP response.

        :param urlOpPost:
        :return:
        """

        rop = requests.post(urlOpId, auth=(self.user, self.passwd), verify=False)   # Request to get operation id
        return rop.headers['Location'].split('/')[2]    # Get Location header


    def getConfId(self):
        """
        Get the configuration id, which is substring of the Location header in HTTP response.

        :return:
        """

        rconf = requests.post(self.urlConfBase, auth=(self.user, self.passwd), verify=False)
        return rconf.headers['Location'].split('/')[2]


    def deleteConfId(self, confId):
        """
        Delete existing Vyatta configuration session

        :param confId: Configuration ID to be deleted
        :return: HTTP status code for DELETE request
        """

        urlConfDelete = self.urlConfBase + '/' + confId
        rdel = requests.delete(urlConfDelete, auth=(self.user, self.passwd), verify=False)
        return rdel.status_code


    def commandOperational(self, opCommandFileName):
        """
        Call Vyatta operational mode commands from opCommandFileName file.

        :param opCommandFileName: Input file for Vyatta operational mode commands
        :return:
        """

        with open(opCommandFileName, encoding='utf-8') as opCommandFile:
            for line in opCommandFile:

                urlOpCommand = self.urlOpBase + '/' + '/'.join(line.split(None))
                ropResult = requests.get(self.urlOpBase + '/' + self.getOpId(urlOpCommand),
                                         auth=(self.user, self.passwd),
                                         verify=False)    # Request to get the results
                print('$ ' + line)
                print(ropResult.text)


    def createEncodedUrl(self, confId, string):
        """
        URLencode every configuration words and form proper URL for REST API requests.

        :param confId: Configuration session ID
        :param string: One line Vyatta configuration commands and parameters
        :return: Encoded URL for Vyatta REST API

        TODO: Fix wrong encoding when spaces in description "" in Vyatta configuration is used.
              ex. description "IPSEC to HQ". In the meantime, avoid using "" in Vyatta configuration.
        """

        encodedWord = []
        for word in string.split():
            encodedWord.append(urllib.parse.quote(word, safe=""))   # Encode each words, then make a list of words

        encodedUrl = self.urlConfBase + '/' + confId + '/' \
                     + '/'.join(' '.join(encodedWord).split(None))

        return encodedUrl


    def editConfig(self, confFileName):
        """
        Read configurations from a file and send requests to Vyatta via REST API,
        then actually modify Vyatta configuration and commit configuration changes.

        :param confFileName: A file which has the configurations to apply
        :return: HTTP status code for deleteConfId()
        """

        # Set configurations
        with open(confFileName, encoding='utf-8') as confFile:

            confId = self.getConfId()   # Get configuration ID

            for line in confFile:
                if not (re.compile("^#").match(line)
                        or re.compile("^$").match(line)):      # Skip line matches with "^#" or "^$"
                    urlConfPut = self.createEncodedUrl(confId, line)

                    rconf = requests.put(urlConfPut,
                                         auth=(self.user, self.passwd),
                                         verify=False)   # Request for configuration commands

                    print("%s : %s" % (urlConfPut, rconf.status_code))

        # Commit configurations
        self.commitConfig(confId)

        # Delete conf-id and return HTTP status code
        return self.deleteConfId(confId)


    def commitConfig(self, confId):
        """
        Commit configuration changes

        :param confId: Configuration session ID
        :return: HTTP status code
        """

        urlConfCommit = self.urlConfBase + '/' + confId + '/commit'
        rconf = requests.post(urlConfCommit, auth=(self.user, self.passwd), verify=False)   # Request for commit
        print("%s : %s" % (urlConfCommit, rconf.status_code))
        return rconf.status_code


    def saveConfig(self, confId):
        """
        To be implemented

        :param confId:
        :return:
        """

        pass


    def revertConfig(self, confId):
        """
        To be implemented

        :param confId:
        :return:
        """

        pass


if __name__ == "__main__":

    # Test code
    user = vyuser.VYUSER
    passwd = vyuser.VYPASSWD
    urlBase = vyuser.URLBASE

    vy = Vyatta.VyattaControl(urlBase, user, passwd)

    #print(vy.urlOpBase)
    #print(vy.deleteConfId(vy.getConfId()))

    vy.editConfig('vy_configuration.conf')
    vy.commandOperational('vy_op_command.conf')