# teachablemachine
This is a python basic server that you can curl a model file generated from teachable machine to classify an image

On your server
### install python3 and python3 libraries
```
git clone https://github.com/lbaitemple/teachablemachine
cd teachablemachine
sudo apt install python3-dev
sudo bash ./linux_install.sh
```
### to add user
```
echo username:password | base64 >> password.txt
```

### run the server
```
python3 pythonserver.py  &> /dev/null &
```

On your client terminal, you can specify three files upload to classify the image in picture field

```
curl -u username:password  -F "picture=@pic2.jpg" -F "model=@keras_model.h5" -F "class=@labels.txt" http://serveraddress:8080

```
