# findmysmile

## Inspiration
The aim of this project was to improve the convenience of people's lives. Most of us have very limited knowledge when it comes to medical knowledge, and an even smaller subset of that knowledge when it comes to our knowledge of teeth. To have a deep understanding of matters related to dentistry, one would have to dedicate many years learning the fundamentals relevant to various dentistry/medical procedures, spend decades and invest significant amount of time learning about such things. However, given that we have a finite amount of time and we may not have the time/energy to search through myriad of articles, advices and information regarding symptoms related to toothache and gum swelling, it can lead to negligence of our teeth health and can make the problem worse. We wanted to simplify this process, rather than having to go through the hassle of spending hours reading misleading/fear-inducing articles, as that is the tendency for many google searches minor symptoms, it provides unhelpful/fear-inducing information, undermining the reliability, the primary reliable sources being our doctors and physicians.

## What it does
Using AI, the idea was to help reduce that stressful process, where RAG based LLMS model will utilize information on the internet, reducing the need for us to search through confusing array of information, the model determines not only the treatments needed to alleviate/cure the symptoms, but also provides recommendations based on the user's location the available places, their contact information, exact address, whether or not the location is operational as well as the price range for the corresponding dental clinic based on the user's geolocation.

## How we built it

<b>Frontend</b>: React Native, Expo, Typescript, Auth0

<b>Backend</b>: Flask, Python, Modal, Warp

<b>Model</b>: PyTorch, LlamaIndex, OpenAI, GooglePalm, Nomic, Langchain, Huggingface

<b>Database</b>: MongoDB Atlas


## Challenges we ran into

Integrating the frontend with the backend, primarily due to the accumulated mental exhaustion, and the complexity of the project alongside determining the correct models to implement, how database such as MongoDB works and interacting with it.

## What we learned
We learned about llama index, Data pipelines, CI/CD, MongoDB atlas, indexing/vectorized data, React-Native stack and interactivity, Auth0 privacy and modal's remote deployment features.

## What's next for Find My Smile
- [ ] Complete integration of backend with frontend, cleaning and up and implementing new API routes, nicer UI and interactivity.
- [ ] Improving the existing data pipeline to better interact with one another.
- [ ] Model finetuning to improve accuracy.
- [ ] Ensuring image processing model works as intended.
- [ ] Gather more data, automate the process of data collection, in order to have up-to-date data.


## Relevant Images of MVP

Landing Screen             |  Home Screen             |  Upload Teeth Image Part 1                 
:-------------------------:|:-------------------------:|:---------------------:
![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/448/datas/gallery.jpg)  |  ![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/450/datas/gallery.jpg) | ![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/449/datas/gallery.jpg)

Upload Teeth Image Part 2             |    Alternative, Choose Image from gallery           |   Recommended Dentists Nearby                
:-------------------------:|:-------------------------:|:---------------------:
![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/451/datas/gallery.jpg)  |  ![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/452/datas/gallery.jpg) | ![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/485/datas/gallery.jpg)

Treatment Recommendation |    Recommended Dentists Nearby Part 2           
:-------------------------:|:-------------------------:
![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/486/datas/gallery.jpg)  |  ![](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/830/484/datas/gallery.jpg) 

[Link to Devpost, Leave a Like!](https://devpost.com/software/find-my-smile)



