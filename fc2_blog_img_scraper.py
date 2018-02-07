# coding:utf-8
from selenium import webdriver # conda install -c conda-forge selenium
import os, requests, time
from time import sleep

def downloadImg(url,name,path_dir):
    try:
        print(name + 'の画像をダウンロード中{}...'.format(url))
        res = requests.get(url)
        res.raise_for_status()
        os.makedirs(path_dir, exist_ok=True)
        img_name = name
        image_file = open(os.path.join(path_dir, img_name), 'wb')
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()
    except:
        print("can not download img")

# https://fc2.com/login.php?ref=blog
# https://admin.blog.fc2.com/control.php?mode=control&process=backup&type=file&ext=pict&page=1
if __name__ == '__main__':

    user = "USER_ID"
    password = "PASSWORD"

    ### 目的のURL
    url = "https://fc2.com/login.php?ref=blog"

    ### 画像の保存先
    dir_name = 'dl-img'

    ### 保存先のフォルダを作成
    os.makedirs(dir_name, exist_ok=True)
    file_name = dir_name + "/sc.png"

    ### ヘッドレスブラウザの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # chromeブラウザのパスを追加
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)

    # ブラウザのウィンドウサイズの設定
    driver.set_window_size(1920, 1080)

    # サイトの取得
    driver.get(url)
        
    input_email = driver.find_element_by_id("id")
    
    input_password = driver.find_element_by_id("pass")
    
    submit_login = driver.find_element_by_class_name("sh_login_ja")
    submit_login = submit_login.find_element_by_tag_name("a")
    
    input_email.send_keys(user)
    input_password.send_keys(password)
    submit_login.click()

    # driver.save_screenshot(file_name)

    for i in range(120):
        paged = i + 1
        paged = str(paged)
        target = "https://admin.blog.fc2.com/control.php?mode=control&process=backup&type=file&ext=pict&page=" + paged
        # print(target)
        driver.get(target)
        images = driver.find_elements_by_tag_name("img")
        
        for image in images:
            img_src = image.get_attribute("src")
            img_name = image.get_attribute("alt")

            # print(img_src, img_name)
            if img_src != "https://static.fc2.com/share/fc2parts/image/sh_help_icon.gif":
                downloadImg(img_src, img_name, dir_name)
                sleep(1)
        sleep(1)
        

    # # スクリーンショットの保存
    # # driver.save_screenshot(file_name)

    # page_html = driver.page_source

    driver.quit()
    # print(page_html)

