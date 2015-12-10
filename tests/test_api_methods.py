#!/usr/bin/env python3
#global
import tempfile
import os
import unittest
import logging

# Setup module level logging.
logging.basicConfig(level=logging.DEBUG)

from qualysapi import qcache, config, exceptions
from qualysapi import api_actions

class TestAPIMethods(unittest.TestCase):
    '''
    APICache unittest class

    @Params
    tf = tempfile
    test_username -- stored if there is a need to use a temporary config during
    the testing process.
    test_password -- also stored if there is a need to use a temporary config
    during testing.
    tfDestroy -- set IFF the config file is a temp file that should be cleaned
    up during tearDown.
    '''

    # set up configuration arguments for later use by config
    tf = None
    test_username = None
    test_password = None
    tfDestroy = False
    def setUp(self):
        '''
        Sets up a unittest api config file if one doesn't exist already
        '''
        #test from relative...

        #check if we have the required test data for unit tests
        self.tcfilename = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'test_data')
        self.tcfilename = os.path.join( self.tcfilename, 'integration-config.cfg')

        # logger.debug('Test Case Config File is ' + self.tcfilename)
        # logger.debug(os.path.isfile(self.tcfilename))

        # if we don't have a unittest configuration file make a temporary
        # file for our unit tests
        if not os.path.isfile(self.tcfilename):
            import getpass

            # right so go ahead up-front for the test and collect a
            # username and password
            self.test_username = input('QualysGuard Username: ')
            self.test_password = getpass.getpass('QualysGuard Password: ')

            # now create a temporary file and save the user/pass for the tests...
            self.tf = tempfile.NamedTemporaryFile(delete=False)
            self.tcfilename = tf.name
            self.tf.close()
            self.tfDestroy = True

        qconf = config.QualysConnectConfig(
                use_ini=True,
                filename=self.tcfilename,
                username=self.test_username,
                password=self.test_password,
                remember_me=True)
        self.cache_instance = qcache.APICacheInstance(qconf)


    def tearDown(self):
        '''Remove the temporary file'''
        if self.tfDestroy: os.remove(os.path.abspath(self.tcfilename))

    def test_api_init(self):
        ''' Pulls a list of maps '''
        with self.assertRaises(exceptions.NoConnectionError):
            actions = api_actions.QGActions()



    def test_map_list(self):
        ''' Pulls a list of maps '''
        actions = api_actions.QGActions(cache_connection =
                self.cache_instance)
        scans = actions.listScans(state='Finished')
        self.assertGreaterEqual(len(scans),1)
        for counter,scan in enumerate(scans):
            logging.debug('%02d:\r%s' % (counter, scan))


#stand-alone test execution
if __name__ == '__main__':
    logging.info('Beginning nose2 unit tests...')
    import nose2
    nose2.main()
    logging.info('Tests completed...')
