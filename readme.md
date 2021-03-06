## Project Name & Summary
*Flask webserver and http client*  

A flask webserver application was designed and is now
running on pythonanywhere.  The app serves as proof of
concept on how to send and receive json data over secure
servers via http.  This framework will be built upon
in subsequent apps.

## Usage
### Python Client
Run `python client_v01.py` to create various web requests
for the flask server running remotely on pythonanywhere.

The python client can send and receive json data that is stored in a cloud database.

### Web Browser
A web browser can be used to make a simple get request of the flask server.
Use the python client if you wish to make a POST or send receive json data.

https://ez066144.pythonanywhere.com/parse_request?variable1=value1&variable2=value2 
where you replace the text following the ? with your data of interest.

For example:  
[https://ez066144.pythonanywhere.com/parse_request?username=SteveHolt&showname=ArrestedDevelopment](https://ez066144.pythonanywhere.com/parse_request?username=SteveHolt&show=ArrestedDevelopment)

## Results
View the html files in [server_responses](server_responses)
for example http requests and results.

## License

Distributed under the *** License.  
See `*** License Info ***` for more information.

## Contact

Tony Held - tony.held@gmail.com  
Project Link: [https://github.com/TonySelfStudy/flask_webserver_v01](https://github.com/TonySelfStudy/flask_webserver_v01)
