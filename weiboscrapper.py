import os
import json
from time import sleep
import random

from weibo import gotbanError, finishError, notFinishError
import weibo as wb
#"1784473157", "1974576991", "1663072851", "2810373291", "3937348351", "6189120710", "2375086267", "1157864602", "3553342022", "7546792313", "7270429057", "2150758415", "5476386628", "1989660417", "1875293522", "1112928761", "2099591797", "1955563285", "1887344341", "1639498782", "2615417307", "1649173367", "5182171545"

user_list = [
    "1663072851", "2810373291", "3937348351", "6189120710", "2375086267", "1157864602", "3553342022", "7546792313", "7270429057", "2150758415", "5476386628", "1989660417", "1875293522", "1112928761", "2099591797", "1955563285", "1887344341", "1639498782", "2615417307", "1649173367", "5182171545",
    "1784473157", "1974576991"
]

#user_list = ["1784473157", "1974576991"]


# extract text information
def pickup_length(wb_file, out_path, thresh=250):
    pickup_file = {'weibo': []}
    with open(wb_file, 'r', encoding='utf-8') as fp:
        json_file = json.load(fp)
        # set ouput file path
        out_file = json_file['user']['screen_name'] + '.json'

        # check weibo content
        for weibo in json_file['weibo']:
            if len(weibo['text']) >= thresh:
                print(weibo['text'])
                pickup_file['weibo'].append(weibo)

    # save json
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    with open(out_path + out_file, 'w', encoding='utf-8') as fp:
        json.dump(pickup_file, fp, ensure_ascii=False)


def go_through_file(root_path):
    # fetch weibos folser
    folder_list = os.listdir(root_path)
    out_folder = './length_limit/'

    for folder in folder_list:
        user_path = root_path + folder + '/'
        if os.path.isdir(user_path):
            weibo_file_list = os.listdir(user_path)
            for weibo_file in weibo_file_list:
                if os.path.splitext(weibo_file)[1] == '.json':
                    #print(out_folder + folder)
                    pickup_length(user_path + weibo_file, out_folder)

    return


def build_crawler(user, start_page=1):
    config = wb.get_config()
    crawler = wb.Weibo([user], config)
    print([user])
    crawler.start_page = start_page
    return crawler


def check(i):
    print(i)
    if i < 10:
        raise notFinishError
    elif i >= 10:
        raise finishError
        print('haiyou ')


for user in user_list:
    done = False
    start_page = 1
    i = 0
    while not done:
        try:
            crawler = build_crawler(user, start_page=start_page)
            print('get user {} page {}'.format(user, start_page))
            crawler.start()
            #check(i)
        except notFinishError:
            i += 1
        except gotbanError:
            start_page = crawler.finished_page + 1
            sleep(random.randint(300, 500))
        except finishError:
            break

        #break

root_path = './weibo/'
go_through_file(root_path)