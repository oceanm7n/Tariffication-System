# Если тебя начнут спрашивать на паре, как ты это сделал, а ты ничего
# не сможешь внятно объяснить - очевидно проебёшься. Я тебе расписал в вк
# как и что здесь работает, если есть ещё вопросы - feel free to ask

# P.S. переводы непонятных слов на английском гугли сам, а то стыд совсем


import math

# EVENT ID's
EVENT_TOPUP = 1  # topup (sum)
EVENT_INCALL = 2  # incall (phone number, seconds)
EVENT_OUTCALL = 3  # outcall (phone number, seconds)
EVENT_INSMS = 4  # insms (phone number,seconds)
EVENT_OUTSMS = 5  # outsms (phone number,seconds)
EVENT_INTERNET = 6  # internet (MB)
EVENT_ROAMING_ENTER = 7  # no args
EVENT_ROAMING_EXIT = 8  # no args

# PRICE CONSTANTS
HOME_OUTCALL_PRICE = 2
HOME_INCALL_PRICE = 8
ROAM_OUTCALL_PRICE = 20
HOME_SMS_PRICE = 1
ROAM_SMS_PRICE = 5
HOME_INTERNET_PRICE = 0.2
ROAM_INTERNET_PRICE = 5


def process_data(data):
    roaming = False  # by default, phone user was in home internet
    for event in data:  # events which are not dependent on the roaming
        if event[1] == EVENT_TOPUP:  # EVENT_TOPUP
            processed_data[event[0]]['recharge'] += event[2]
        elif event[1] == EVENT_INSMS:  # EVENT_INSMS doesn't depend on roaming condition
            processed_data[event[0]]['insms'][0] += 1   # +1 incoming sms count
        elif event[1] == EVENT_ROAMING_ENTER:
            roaming = True   # entered roaming
        elif event[1] == EVENT_ROAMING_EXIT:
            roaming = False  # exited roaming
        else:  # process events, which ARE dependent on roaming condition"
            if not roaming:  # home net
                if event[1] == EVENT_INCALL:
                    processed_data[event[0]]['incall_home'][0] += 1  # +1 count
                    processed_data[event[0]]['incall_home'][1] += \
                        math.ceil(event[3]/60)
                    processed_data[event[0]]['incall_home'][2] += 0
                if event[1] == EVENT_OUTCALL:
                    processed_data[event[0]]['outcall_home'][0] += 1  # +1
                    processed_data[event[0]]['outcall_home'][1] += \
                        math.ceil(event[3]/60)
                    if event[3] > 3:
                        processed_data[event[0]]['outcall_home'][2] += \
                            math.ceil(event[3]/60)*HOME_OUTCALL_PRICE
                        processed_data[event[0]]['expenses'] += \
                            math.ceil(event[3]/60)*HOME_OUTCALL_PRICE
                if event[1] == EVENT_OUTSMS:
                    processed_data[event[0]]['outsms_home'][0] += 1
                    processed_data[event[0]]['outsms_home'][1] += \
                        math.ceil(len(event[3])/70*HOME_SMS_PRICE)
                    processed_data[event[0]]['expenses'] += \
                        math.ceil(len(event[3])/70*HOME_SMS_PRICE)
                if event[1] == EVENT_INTERNET:
                    processed_data[event[0]]['internet_home'][0] += event[2]
                    processed_data[event[0]]['internet_home'][1] += \
                        math.ceil(event[2]*HOME_INTERNET_PRICE)
                    processed_data[event[0]]['expenses'] += \
                        math.ceil(event[2]*HOME_INTERNET_PRICE)

            else:  # roaming internet
                if event[1] == EVENT_INCALL:
                    processed_data[event[0]]['incall_roam'][0] += 1  # +1 count
                    processed_data[event[0]]['incall_roam'][1] += \
                        math.ceil(event[3]/60)
                    processed_data[event[0]]['incall_roam'][2] += \
                        math.ceil(event[3]/60)*HOME_INCALL_PRICE
                    processed_data[event[0]]['expenses'] += \
                        math.ceil(event[3]/60)*HOME_INCALL_PRICE
                if event[1] == EVENT_OUTCALL:
                    processed_data[event[0]]['outcall_roam'][0] += 1
                    processed_data[event[0]]['outcall_roam'][1] += \
                        math.ceil(event[3]/60)
                    if event[3] > 3:
                        processed_data[event[0]]['outcall_roam'][2] += \
                            math.ceil(event[3]/60)*ROAM_OUTCALL_PRICE
                        processed_data[event[0]]['expenses'] += \
                            math.ceil(event[3]/60)*ROAM_OUTCALL_PRICE
                if event[1] == EVENT_OUTSMS:
                    processed_data[event[0]]['outsms_roam'][0] += 1
                    processed_data[event[0]]['outsms_roam'][1] += \
                        math.ceil(len(event[3])/70)*ROAM_SMS_PRICE
                    processed_data[event[0]]['expenses'] += \
                        math.ceil(len(event[3])/70)*ROAM_SMS_PRICE
                if event[1] == EVENT_INTERNET:
                    processed_data[event[0]]['internet_roam'][0] += event[2]
                    processed_data[event[0]]['internet_roam'][1] += \
                        math.ceil(event[2]*ROAM_INTERNET_PRICE)
                    processed_data[event[0]]['expenses'] += \
                        math.ceil(event[2]*ROAM_INTERNET_PRICE)


def display_info(data_dictionary):  # argument - dictionary
    print("Total recharge:", data_dictionary['recharge'], "RUB")
    print("Total expenses:", data_dictionary['expenses'], "RUB")
    print("Detalization:")
    print("Incoming calls (home net):", data_dictionary['incall_home'][0],
        ", total length:", data_dictionary['incall_home'][1],
        "min, charged:", data_dictionary['incall_home'][2], "RUB")
    print("Incoming calls (roaming):", data_dictionary['incall_roam'][0],
        ", total length:", data_dictionary['incall_roam'][1],
        "min, charged:", data_dictionary['incall_roam'][2], "RUB")
    print("Outgoing calls (home net):", data_dictionary['outcall_home'][0],
        ", total length:", data_dictionary['outcall_home'][1],
        "min, charged:", data_dictionary['outcall_home'][2], "RUB")
    print("Outgoing calls (roaming):", data_dictionary['outcall_roam'][0],
        ", total length:", data_dictionary['outcall_roam'][1],
        "min, charged:", data_dictionary['outcall_roam'][2], "RUB")
    print("Outgoing SMS (home net):", data_dictionary['outsms_home'][0],", charged:", data_dictionary['outsms_home'][1],"RUB")
    print("Outgoing SMS (roaming):", data_dictionary['outsms_roam'][0],", charged:", data_dictionary['outsms_roam'][1],"RUB")
    print("Mobile internet (home net):",data_dictionary["internet_home"][0],"Mb,","charged:",data_dictionary["internet_home"][1],"RUB")
    print("Mobile internet (roaming):",data_dictionary["internet_roam"][0],"Mb,","charged:",data_dictionary["internet_roam"][1],"RUB\n")


# data object format: [
#     ["mm.yyyy",EVENT,..event args],
#     ["mm.yyyy",EVENT,..event args],
#     ...
# ]

data = [
    ["12.2018", EVENT_TOPUP, 400],
    ["12.2018", EVENT_INCALL, "+79258545485", 345],
    ["12.2018", EVENT_OUTSMS, "+79623549656",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit!"],
    ["12.2018", EVENT_OUTCALL, "+71293829189", 89],
    ["12.2018", EVENT_ROAMING_ENTER],
    ["12.2018", EVENT_INCALL, "+79187271671", 87],
    ["12.2018", EVENT_INSMS, "+79166726171",
        "I am working on my hometask right now"],
    ["12.2018", EVENT_INTERNET, 120],
    ["12.2018", EVENT_OUTCALL, "+79281726462", 289],
    ["12.2018", EVENT_INTERNET, 76],
    ["01.2019", EVENT_OUTSMS, "+79128192819",
        "Saskdas aslkdj ad ljasdiasj dlasijdasil j! aljasildjasl LJ!Ljij2"],
    ["01.2019", EVENT_ROAMING_EXIT],
    ["01.2019", EVENT_INCALL, "+79182926563", 246],
    ["01.2019", EVENT_TOPUP, 250],
    ["01.2019",EVENT_INTERNET, 123],
    ["01.2019",EVENT_OUTSMS, "+79192828181",
        "123123ASIODJAISD ahdmA odhqo1902u ajldad"]
]


# map all possible months a user can choose
dates = []
for x in data:
    if not (x[0] in dates):
        dates.append(x[0])


# processed_data format:
# {
#     "mm.yyyy":{
#         "incall_home":[count,minutes,RUB]
#         .
#         .
#         .
#     }
#     "mm.yyyy":{
#         .
#         .
#         .
#     }
# }


processed_data = {}
for month in dates:
    processed_data[month] = {"recharge": 0,
     "expenses": 0,
     "incall_home": [0, 0, 0],
     "incall_roam": [0, 0, 0],
     "outcall_home": [0, 0, 0],
     "outcall_roam": [0, 0, 0],
     "insms": [0, 0],
     "outsms_home": [0, 0],
     "outsms_roam": [0, 0],
     "internet_home": [0, 0],
     "internet_roam": [0, 0]
     }

# processing data
process_data(data)

# input handling
while True:
    input_date = input("Enter month and date (mm.yyyy) [ENTER to finish]:")
    if input_date:
        try:
            if (0 <= int(input_date.split(".")[0]) <= 12):
                if (input_date in dates):
                    display_info(processed_data[input_date])
                else:
                    print("No data found")
            else:
                print("Wrong month")
        except Exception:
            print("Wrong format")
    else:
        break
