import numpy as np
import math


class Data:
    def __init__(self , data_array):
        self.array = data_array

    def initiziale(self , time , sza , id):
        self.time = time
        self.id = id
        self.sza = sza


def appender(number):
    my_string = ''
    if number // 10 == 0:
        my_string = "00" + str ( number )
    elif number // 100 == 0:
        my_string = "0" + str ( number )
    else:
        my_string = str ( number )
    return my_string


def get_data_from_both_files(array_numberD , array_numberG):
    #final_array_before_return = np.array ( [["Time" , "sza" , "ID-D" , "ID-G" , "I-diff"]] )

    final_array_before_return = None
    counter = 1
    while True:

        if array_numberD.id[counter]>5 and array_numberG.id[counter] > 5 and array_numberD.sza[counter] < 88 and \
                array_numberG.sza[counter] < 88:

            i_diff = array_numberG.id[counter] - array_numberD.id[counter] * math.cos(
                array_numberD.sza[counter] * math.pi / 180 )

            tmp = np.array ( [[array_numberD.time[counter] , array_numberD.sza[counter] , array_numberG.id[counter] ,
                               array_numberD.id[counter] , i_diff]] )

            if final_array_before_return is None:
                final_array_before_return = np.array(tmp)
            else:
                final_array_before_return = np.concatenate ( (final_array_before_return , tmp) , axis=0 )

        counter = counter + 1
        if counter >= array_numberD.array.shape[0] - 1:
            break

    return final_array_before_return


if __name__ == "__main__":

    for x in range ( 1 , 367 ):

        i_diff_ = 0
        i_diff_sum = 0

        if x != 333 and x != 332 and x!=331 and x!=334 and x!=335 and x!=336 and x!= 337 and x!= 338 and x!=339 and x!=366:

            key = appender( x )

            pathD = "DIR11016.dat"
            pathG = "TOT11016.dat"

            with open ( pathD , 'r' ) as D:
                datad = Data ( np.genfromtxt ( D , delimiter='' ) )
                np.set_printoptions ( formatter={'float': '{: 0.3f}'.format} )

                datad.initiziale ( datad.array[: , ][1: , 0] , datad.array[: , ][1: , 1] , datad.array[: , ][1: , 2] )

                # print("We deleted in total " + str(count_errors) + " incorrect or unreliable data")

            with open ( pathG , 'r' ) as G:
                datag = Data ( np.genfromtxt ( G , delimiter='' ) )

                datag.initiziale ( datag.array[: , ][1: , 0] , datag.array[: , ][1: , 1] , datag.array[: , ][1: , 2] )

            final_array = get_data_from_both_files ( datad , datag )

            np.savetxt('final_array.txt', final_array, delimiter=',', fmt='%f %f %f %f %f')

            i_diff_sum = np.sum(final_array, axis=0)

            vima = 0.0167 * (final_array.shape[0]/1440)
            i_diff_ = i_diff_sum[4] * vima

            #head = list(["Time", "sza", "ID-D", "ID-G", "I-diff"])
            #np.savetxt('results.txt', final_array, header='      '.join(head), delimiter=',', fmt='%f %f %f %f %f')

            print(key + "," + str(i_diff_))



