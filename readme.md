#### Disclaimer
**Note**: A better description of what i did, can be found in the main notebook itself, since it made more sense to me to describe what I was trying to achive while doing it. Nonetheless a readme.md makes total sense for the introduction of the project.

# Project goal/Motivation
For this project I tested a view existing multimodals like *idefics2-8b*, different versions of *llava* and *chatGPT-4o*. However I only included the code for chatGPT since I now know that its not that easy (impossible depending on the hardware) to run those models locally. Also I wasn't able to run all of them in collab. The process of reloading them generate the text was also rather time consuming - a bad fit for someone else to present the solution.

So as you can see one goal of me was, to just test out some of the newer models that exist:)

**So what was the project all about?**
The goal of the project was to identify the items and their quantities in a cardboard box based on images provided to the model. An example of such an image is as follows:
![example image](results/2.jpg)

**So what are the benefits of this project, why is it relevant?**
In our daily lives, the task of taking items out of or putting items into a container happens frequently. Examples include doing laundry, placing your wallet in your pocket, packing or unpacking a backpack, grocery shopping, organizing documents in a drawer, and so on.

Even in businesses, many such tasks occur regularly. For some of these tasks, tracking the objects inside a container would be extremely useful.

My motivation for this project was to explore whether a model could effectively track the contents of my fridge. By doing so, I could automate my shopping list and generate meal plans based on the available ingredients. Additionally, I would be able to determine if an edible item is about to spoil within a certain timeframe. 

As you can see, the provided image consists of multiple images, illustrating how the object moves. Hence, determining the direction of the object's movement without any motion blur or other indicators would be very hard with only a single image.
**I approached the tracking of contents in two ways:**
1. Creating a prompt that included an object containing all the items currently inside the box and asking the model what is inside the box after processing the provided image.
2. Creating a prompt in which the model would return the object name, quantity, and whether it was added to or removed from the box. With this information, I could update the box's contents using a variable.

For every model I used, except chatGPT only the second aproach offered okayish result. For chatGPT I started with the first approach and it was already doing a great job.


