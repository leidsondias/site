---
title: "Transform Medium to Markdown"
tags: ['JavaScript', 'Python', 'Chrome Extension']
date: 2019-05-27T08:05:48.870000
---

## Motivation

In the last year(2018), I and my friend [heliocorreia](https://medium.com/@heliocorreia) talk about making the personal website and make a post in it. But, I different from him didn’t want to create a blog system for posting. I thought, why not use Medium with as my publication platform and I build a script to migrate from Medium to Markdown?


<!--more-->

## **Existent’s Libs**

So, I started to search for Libs with these functionalities. I found a lot of libs, but I most liked from two.

* [Turndown](https://domchristie.github.io/turndown/)

* [Medium exporter](https://github.com/xdamman/mediumexporter)

For me, the Medium Exporter is the better. It is very simple to use and work perfectly.

## Decide what I’m going to use and how I’m going to do the script

Ok, I found and now I know it’s possible to make what I want. Let’s go start from zero one Lib to transform Medium to Markdown and using stuff I do not use at now with much frequency. For example, Python.

Why Python? I used Python because I like this language and have some time I don’t work with it. It is not because is better or anything else. I like and want to make the new project with it.

### **Test**-**driven development**

Another thing that I used is [TDD](https://en.wikipedia.org/wiki/Test-driven_development). I like this technique but I do not use it every time. It’s a habit that I need to practice. Today I make tests after making the code.

My first reading about TDD was the [Thiago Belem post](http://blog.thiagobelem.net/aprendendo-tdd-ou-desenvolvimento-orientado-a-testes). Later I had the opportunity to take the Industrial Logic course. The course was about TDD and Refactor. It’s a very good course, but what I most liked was the Refactor topic. It’s a good topic for talking about.

### Paradigm

Now, I have the language and what technique I will use. What is missing?

The programming paradigm I want to use. I guess the [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) is most easy to understand. But I don’t need reuse code, extend classes, polymorphism or another thing with OOP give to me.

So, I used [Functional programming](https://en.wikipedia.org/wiki/Functional_programming). What I have on my script are the immutable state and pure functions. To be clear, I prefer OOP. But for me, you must use what your problem needs and not what you want.

## **Challenges**

I needed to remember a lot of things about Python. How to use some methods, etc. But, my main challenge was to add markups into the text without affecting anything.

The Medium post payload after make parser to JSON is some like this:

```
...
“paragraphs”: [{
 “name”: “7854”,
 “type”: 3,
 “text”: “Web Components with Redux”,
 “markups”: []
 }, {
      "name": "0c36",
      "type": 1,
      "text": "The Web Components has a method called observedAttributes , works this way: every time is your observed attribute change, his call an another method called as attributeChangedCallback . This second method has a three parameters: name, oldValue and newValue.",
      "markups": [{
       "type": 10,
       "start": 39,
       "end": 57
      }, {
       "type": 10,
       "start": 159,
       "end": 183
      }, {
       "type": 3,
       "start": 39,
       "end": 56,
       "href": "[https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges](https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges)",
       "title": "",
       "rel": "",
       "anchorType": 0
      }, {
       "type": 3,
       "start": 159,
       "end": 183,
       "href": "[https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges](https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges)",
       "title": "",
       "rel": "",
       "anchorType": 0
      }, {
       "type": 2,
       "start": 229,
       "end": 244
      }, {
       "type": 2,
       "start": 247,
       "end": 256
      }]
     },
...
```

If I iterate the paragraphs and get the markups and add to the text. The next paragraph with markup will be affected with the previous markup and we will have a problem.

One resolution for this problem is saving the number of char on the aux variable. Apply on the copy of the text without touching on the original text.

Another solution is to use aux variable to stop and concatenate the strings. And merge with the rest of the text.

So I talked with my both friends from my company ([Fábio Matias](https://medium.com/@fabiomatias21) and [Daniel Magro](https://medium.com/@dmagro04)). Both given to me good ideas to add the markups. I merged the ideas to make the below solution.

First, I sort the array of paragraphs with the keys: **start** and **type**.

```
markups = sorted(paragraph.get('markups'), key=lambda m: (m.get('start'), m.get('type')))
```

Second, I iterate the array checking if it has one more markup into the text and I remove it if it has. I keep only one in the ascendant order. I will go to improve to apply more than one markup. For applying more than one, I need to control the original text and extract the word that I want to change. After, I merge all markups.

```
markups = [mark for mark in markups if mark.get('start') not in seen and not seen.add(mark.get('start'))][::-1]
```

For last I reverse the array `[::-1]`. Because when I will add the markups, I do not make any changes for the firsts markups. How this I not change the text and not need to have the control when I add the markup.

## Automatization process

I didn’t want to keep one [Cron](https://en.wikipedia.org/wiki/Cron) running because I don’t know what with the frequency I will write the posts. So instead of using an active job for this, I want to use the reactive job. Whenever I publish the post on Medium, create a new post on my website.

### Chrome extension

My idea is creating a chrome extension. When I am on the Medium page, it listening when I publish the article and trigger my script.

I had some difficulty to make the chrome extension call the python or bash script. I didn’t find any example for executing scripts on the macOS. Just for the Windows OS.

I got it open the calculator, Spotify apps. But whenever I tried to open the terminal, it did open and closes instantly.

I did spend a lot of time trying to make the extension calls directly the script. I did not have the expected result that I did want. So, I decided to create a shortcut to copy the active URL and merge with my full instruction to run the python script.

I hope in the future I improve the extension for call the python script and I don’t need execute on the terminal.

## Conclusion

I never had read about to make a Chrome extension. In general, I don’t like the google documentation. But, the documentation about the extension is OK.

I liked the challenge to create the extension, and understand how the [NativeMessaging](https://developer.chrome.com/apps/nativeMessaging) works. The difference between `background` and `content `scripts.

So what I think is important you know about creating a Chrome extension:

* *Background script*: It’s your central event. Has the access for all Chrome API.

* *Content script*: executes in an isolated context of the webpage, has access to DOM and has very limited access to Chrome API.

* [chrome.runtime.sendMessage](https://developer.chrome.com/apps/runtime#method-sendMessage) : sends a message to your background script. 
Ex: `chrome.runtime.sendMessage({ copy: true })`

* [chrome.runtime.onMessage.addListener](https://developer.chrome.com/apps/runtime#event-onMessage): Have the responsibility for listening when script receiver any message. You can use on the content and background scripts.

* [chrome.commands.onCommand.addListener](https://developer.chrome.com/apps/commands#event-onCommand): It’s called when any shortcut is fired.

* [chrome.tabs.sendMessage](https://developer.chrome.com/extensions/tabs#method-sendMessage): Sends a single message into the specified tab.

Another approach that I can use is creating a server. And every time I create the post, I make an AJAX request for the server and it calls the transformer script. 
I created the server using docker for runs in the background, but for run the script and make the deploy I need dockerize all my project. So, I’ll leave to do this later. But when I will do, I will update the GitHub.

You can access the chrome extension code [here](https://github.com/leidsondias/site/tree/master/scripts/chrome_extension) and the python code [here](https://github.com/leidsondias/site/tree/master/scripts/python).

You can see the result for transform script into the [https://leidson.com/](https://leidson.com/), just the Hello post doesn’t use the transform script. All others use.

The original post is https://medium.com/@leidsoncruz/transform-medium-to-markdown-1e0cc216843f