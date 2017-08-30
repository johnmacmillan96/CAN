# This dictionary is specific to the Nissan LEAF 2015
# You can build a similar dictionary for any car wiht a canbus,
# but you will have to fill out the data yourself


# Each 'IDXXX' consists of a list of 8 dictionaries
# Each dictionary corresponds to 1 of 8 hexidecimal bytes

canIds = {
'ID1DB' : [
    {'name':'Battery Current Signal', 'coeff':0.5,'bitLength':11},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'Battery Voltage Signal', 'coeff':0.5,'bitLength':10},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0}
    ],
'ID284' : [
    {'name':'Left Wheel Speed', 'coeff':0.0031068636832491, 'bitLength':16},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'Right Wheel Speed', 'coeff':0.0031068636832491, 'bitLength':16},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'Vehicle Speed', 'coeff':0.0062137273664981, 'bitLength':16},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0}],
'ID5A9' : [
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'Range', 'coeff':0.00775335775336, 'bitLength':16},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0}
    ],
'ID5BC' : [
    {'name':'GIDS', 'coeff':1, 'bitLength':10},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0}
    ],
'ID55B' : [
    {'name':'State of Charge', 'coeff':.1, 'bitLength':10},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0},
    {'name':'NA', 'coeff':0, 'bitLength':0}
    ],
}
