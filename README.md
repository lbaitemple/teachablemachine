# teachablemachine
This is a python basic server that you can curl a model file generated from teachable machine to classify an image
# to add user
```
echo username:password | base64 >> password.txt
```

In your server terminal, you can run
```
python3 pythonserver.py  &> /dev/null &
```

In your client terminal, you can specify three files upload to classify the image in picture field

```
curl -u username:password  -F "picture=@pic2.jpg" -F "model=@keras_model.h5" -F "class=@labels.txt" http://serveraddress:8080

```
