import requests
import numpy as np
#exhausive gathering the data from 1st id to limit
def exhaustive_gather(n_iter,start_id = 1):
    '''
    this function will gather the data from start_id to n_iter th id.
    input: positive integer n_iter
    Output: array of id
    '''
    id_arr = np.array([],dtype='int64') #define array without limit (as we want to append value to it) as int64 type (since id might not excess int64 upper bound)
    id_ = start_id
    headers = {'Authorization': 'token <token>', } #add token
    while(True):
        try:
        #100 return/request, the limit is 5000/hr so we should be able to get 500000 id/hr.
            response = requests.get('https://api.github.com/users?since='+str(id_)+'&per_page=100',headers=headers) 
            data = response.json() #100 returns, as json list
            for i in range(100):
                id_arr = np.concatenate((id_arr,np.array([data[i]['id']])))
            if id_arr[-1] >= n_iter:
                break
            id_ = id_arr[-1]
        except:
            continue #this will run even though the limit was reached. when the cooldown finish, it will gather again.
    id_arr = np.delete(id_arr, np.where(id_arr > n_iter))
    return id_arr #id_arr[0] is garbage value. Hence, we will ignore it or process it afterward
def testing(m,l):
    '''
    This function will use to test on real data evaluation
    '''
    #first part: divide the space into N_L spaces in which N_L = S/l
    #the latest account id is 79378199 so assume that S = 79378199 [Data at 2/21/2020]
    S = 79378199
    N_L = S//l
    #second part: figure out which sample to sample
    sample_bucket = np.random.choice(np.arange(1,N_L), m, replace=False)
    #define an array for X[i] (think of it as X^L_i) where i, in this case is m (we randomly pick m buckets)
    X = np.zeros((m,),dtype=int)
    #third part : sample
    i = 0
    for bucket_id in sample_bucket:
        #get id_list from nth bucket 
        id_list = exhaustive_gather(l*bucket_id ,start_id = l*(bucket_id - 1))
        X[i] = len(id_list)
        i = i + 1
    estimate = np.sum(X)//(m*(1/N_L))
    return int(estimate)
