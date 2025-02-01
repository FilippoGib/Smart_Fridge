# Vision
Food waste is a pressing global issue, with approximately 1.3 billion tons of food wasted annually, according to the United Nations Food and Agriculture Organization (FAO).   
This amounts to roughly one-third of all food produced for human consumption, while nearly 690 million people suffer from hunger worldwide.   
Food waste occurs at various stages, including production, retail, and consumption, with developed countries contributing significantly to household waste.   
The environmental impact is severe, as wasted food generates 8-10% of global greenhouse gas emissions, exacerbating climate change.   
Addressing this issue requires systemic changes, including improved supply chain efficiency, consumer awareness, and policy interventions to reduce waste and ensure food security.

**Smart Fridge aims to make fighting food wasting as easy as opening you refrigerator.**

# How does it work?

The aim is to create a **DIGITAL TWIN** of the fridge in order to monitor the products that are about to expire.  
In case a product in the fridge is about to expire the app sends a notification to the person asking them if they want to give the product to charity.  
If the answer is affermative the person will be added to the list of donors stored in the server, once a day the server solves the traveller salesman problem and tells the operator the shortest route to follow in order to go and collect all the products from the donors.  
Once the products are collected they are given to local charity community kitchens.

The frigde is equipped with a internal monitor unit and an external monitor unit.  
The internal monitor unit has display and a termometer that is used to monitor the temperature of the fridge every minute.
The external fridge monitor has a movement sensor, a camera and a sliding switch.  
  
Two type of scenarios are handled:  
1. A person wants to refurnish the fridge with new groceries.
2. A person wants to take a product out of the fridge to consume it. 

In both cases the user has to perform the same actions:
1. Select the modality **INSERT** or **EXTRACT**
2. Stand in front of the frigde.
3. Show the camera the barcode of the product.
4. Show the camera the expiry date of the product.
5. Insert / Take out the product.


# About this repository

In this repository you will find the code that will run on the bridge in the folder **src** and on the arduino itself in the folder **ino**.  
You will also find some sample images in the folder **images** and a test folder to make sure everything works as it should.  

# About the code

1. The bridge start the serial communication with the arduino.
2. At startup time the arduino start sending the bridge the GPS data, once the bridge gets the data it sends it to the server in order to let it know its position.  
3. After the GPS data is sent to the server, the arduino starts reading from the movement sensor if someone is standing in front of the fridge, in that care the bridge turns the camera on.
4. The camera attemps to read the barcode of product, once the barcode is read successfully the camera starts to attempt to read the expiry date. If both the barcode and the expiry date are retreived the product information is complete.
5. The bridge then reads the state of the switch, depending if it is on INSERT or EXTRACT it sends respectively a POST or a DELETE request to the server.
6. Once the person is done doing its operations they can just move out of the way of the movement sensor and the bridge will automatically turn the camera off after a given number of seconds.



