# -*- coding: utf-8 -*-
'''
Created on 29.02.2012

@author: stransky
'''
import datajongleur
import time
import morphjongleur.io.swc
from morphjongleur.orm.datajongleur.morphology import *

session = datajongleur.get_session()

def import_swcs(swcs):
    for swc in swcs:
        import_swc(swc)

def import_swc(swc):
    m_swc   = Morphology.specify(Morphology.swc_parse(swc))

    print("uploading data according to '%s'." %(swc)) ,
    start_time = time.time()
    m_swc.save()
    end_time = time.time()
    print("in %s seconds." %(end_time-start_time))
    
    print m_swc.morphology_key
    uuid = m_swc.uuid
    m_swc2 = InfoQuantity.load(uuid)
    print( m_swc2 )

    return m_swc


if __name__ == '__main__':
    import sqlalchemy
    print sqlalchemy.__version__
    #root_dir = '/home/philipp/Repositories/G-Node/mitsubachi/'
    root_dir = '/home/stransky/git/mitsubachi/'
    #root_dir = '../../../'
    import_swcs([
         root_dir + 'data/H060602DB_10_2_zentai_.swc', 
         root_dir + 'data/H060602VB_10_2_zentai_.swc', 
         root_dir + 'data/H060607DB_10_2(zentai).swc', 
         root_dir + 'data/H060607VB_10_2(zentai).swc'
    ])
