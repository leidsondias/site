---
title: "Web Components with Redux"
tags: ['Web Components', 'JavaScript', 'Redux', 'Event Driven Architecture']
date: 2019-05-22T20:12:49.717000
---

Do you need use Web Components in your application? No, you don’t need it. I’m totally against the hype. You should use if only you need. I see some advantages to use if you really need it. For example componentization and your advantages, very small final bundle size, etc.

In the article I talk about a project we(My team) started at [globo.com](https://www.globo.com/). The project was build **Stories** like **Instagram**. We use [ZuckJS](https://github.com/ramon82/zuck.js/) for a POC(proof of concept) but we need to customize a lot this lib. It was a very expensive cost to customize, so I start writing a Vanilla Javascript Lib and after I transform it to Web Components. You can see [here](https://github.com/leidsondias/storiesJSOlder) the vanilla version — branch master.


<!--more-->

At first, I had some troubles to share data between components. I do not want to use any plugin for help with this problem, I wanted to solve with what Web Components provides me and Vanilla Javascript.

If you want to go for Redux topic click [here](#13e6). I tell first what approaches I did use before going to use Redux.

## Observing changes to attributes

The Web Components has a method called [observedAttribute](https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges)s , works this way: every time is your observed attribute change, his call an another method called as [attributeChangedCallback](https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges) . This second method has three parameters: *name, oldValue *and* newValue*.

So, the first approach I did use for pass data to mine elements was set up an attribute and use `attributeChangedCallback` when having attribute changed for change the visualization:

<script src="https://gist.github.com/leidsondias/fec20e1535c4bb832a85321f84fb08d9.js"></script>*Example 1 — Story and Story Items component — The way what i put data on story-items component is not the better. But how i not have the instance for story-items component i need to do that.*

I have an array of objects called as `slides` and on my component `stories-story` I receive the object for use in another component the `story-items`. How you see, if my object `slides` are large my tag from HTML stays too big and too polluted. So, how you can imagine is not better way to share data between components. In my opinion, works if it is for small things, on the documentation you can see an [example](https://developers.google.com/web/fundamentals/web-components/customelements#attrchanges) of use to check if an attribute is disabled or not and from according value sets another attributes on the component.

## Event-driven Architecture

In **event-driven architecture** you send and/or listening events, for example if in `Component A `I need the data from `Component B` , my `Component A` need has two events. One for listening and another for tell `Component B` to want your data. For `Component B` is the same, needs an event for listening if any component wants data and another to send the data:

<script src="https://gist.github.com/leidsondias/f8d5dc281f911a93f4819dba036db81f.js"></script>*Example 2 — This example attached events on document because i don’t have a valid target. But on below code you will see the attachment is on components.*

Try paste this in your browser console. You will see the order for execute is: *get data (ComponentA), send data(ComponentB) *and *receive data(ComponentA).*

So my other approach was to use **event-driven architecture** to work with objects and not need to set attributes on elements. Who started migrate to this architecture was my friend [Ricardo Lino](https://medium.com/@ricardo.linorj), he created a wrapper for events dispatch called as `EventEmitter` .

The `EventEmitter` is our wrapper for events management:

<script src="https://gist.github.com/leidsondias/395df6eb81a303c5630955e6f3ad40d1.js"></script>*Example 3 — Event Emitter, component to management events*

The most important methods are: *on *and *dispatch. *The first is to listen to what you want and the second is to dispatch what event you want.

Below you can see an example for component with listening and dispatch events. Is the same component from the first example (Example 1). The `stories-story` component but written really like a component and now is reusable.

<script src="https://gist.github.com/leidsondias/f9f78b22056cc1c651152263d5d90c62.js"></script>*Example 4 — Story component using our Event Emitter*

Wow, now we have a reusable component with your responsibilities and scopes. But, our mistake was try to migrate code instead of creating from start but starting with **event-driven architecture**. We found a lot of bugs because the Vanilla way was based on find elements from parents or children. Also, I didn’t like needs two methods for get an object. So on our migration process, we needed to close the POC and it had a high cost for close because of the bugs . And the high cost is not are welcome to a POC. This way we stop the project (you can find [here](https://github.com/leidsondias/storiesJSOlder) —branch is feature/EventEmitter).

I really enjoyed this challenge, write Stories with web components. So, I started again but this time using [Redux](https://redux.js.org/) to help me with events and data.

## Using Redux

Why will use **Redux**? Using **Redux** my code became is very simple and very easy to get data in the other components. With it my problems for events control is over as like bugs create by us on the migration progress (**Vanilla** > **Web Components**) haha.

See below the same component from *Example 1*:

<script src="https://gist.github.com/leidsondias/ad0f10258cabc9a78770f23a496c11ea.js"></script>*Example 5 — Story Component using Redux*

Now my Event Emitter has just methods for *subscribing*, *dispatch* and *getState* from **Store** (You can read about Store [here](https://redux.js.org/api/store)).

<script src="https://gist.github.com/leidsondias/9353e41b42af08b3a5135a27511adea8.js"></script>*Example 6 — Event Emitter with store*

**Redux** has the same idea an **event-driven architecture**. Dispatch one event and have another event to listening and fired some function.

For getting started we need configuration our `Store` . The store is a place where you have states of components and only change him through actions.

<script src="https://gist.github.com/leidsondias/b0204f0802c2e9e9c914f3ddc3778733.js"></script>*Example 7 — File for Store object*

Our `Reducer`(In this example I merge the files but the reducer for Story it’s at another file). The **Reducer **has the responsibility to tell how the application state changes from the according to action send to store:

<script src="https://gist.github.com/leidsondias/20aab8061772531322aabb1bd49d0768.js"></script>*Example 8 — Reducer*

So when we receive an action to `LOAD_STORIES` our reducer gets the state from `reducerStories` and change the `stories` key with what the action send on `payload` key. For the `SET_ACTIVE_STORY` action is the same thing only changing the key, instead of `stories` is `activeStory` .

Below is the same component as *Example 1* but with another name. I renamed and make the component cleaner and with more clear responsibility:

<script src="https://gist.github.com/leidsondias/904e5dd006a695d53d746c02f69167e2.js"></script>*Example 9 — Story component but with i rename to Stories*

Now, we have new stuff *loadStories and connectedCallback *in our code.

In the first line, we have the `loadStories` , the function responsibility is to load the data and call the action for send to the store. We receive the data from params, but you can fetch in some API or from another way. The code for `loadStories` is this:

<script src="https://gist.github.com/leidsondias/5db18c267d2fca92d9b0ac8c8242903c.js"></script>*Example 10 — Load Stories action*

You can see what `ACTIONS.LOAD_STORIES` do on our from **Reducer** file in the 13º line. Basically, keeps state and change the state from `stories` key for what we pass from the `payload`.

I use the `connectedCallback` method for initializing our component. Why I use `connectedCallback` instead of `constructor` ? The `constructor` is for you to set up your component and initialize your state, but it is called only one time. So, if the data is dynamic it’s never changed because your component was be started and will not calls the constructor again. The `connectedCallback` is called every time the element is inserted into the DOM. The documentation and the good practices recommend you use to fetch resources or rendering your component. You can find good practices for web components [here](https://developers.google.com/web/fundamentals/web-components/best-practices).

Ok, I load my data on the store now I can work with the data. Our data have an array of objects. Each object is a story data. Below you can see an example for values from the stories key:

<script src="https://gist.github.com/leidsondias/774f978e5c28918e85e9437b967f6c5c.js"></script>*Example 11 — JSON with stories content*

The `Stories` component adds the `StoriesList.` And inside from this component we can get the `stories` saved on our state and make what we want. (In our case we use a Component for render each story)

<script src="https://gist.github.com/leidsondias/f89f27b59076682c9a3f58d9f205d657.js"></script>*Example 12 — Stories List component, your responsibility is to be a wrapper for the story list*

Now we can call `getState` from `EventEmitter` and get state from any reducer. You can see how get the state in the 19º line. In the 20º line, we iterate the `stories` and create a **Story** component for each data from `stories`.

Until now, we see how **dispatch an event** and **get state** from **Redux**. Missed anything? Yeah, the subscribe method for listening when the state change and fire any method. For example, render every time we receiver a new data.

<script src="https://gist.github.com/leidsondias/1782fd1147758611f2c7b69066b57b61.js"></script>*Example 13 — Modal component, your responsibility is has slides from active story.*

The `Modal` component listens if have a change for the state. If has, the `render` method is executed. You can see this code on the 12º line. In the `render` method, we check if exist any story active. If we have an active story we create the `SlideList` component and append on the `Modal` component.

A bad point this code is you listening to all events when state changes, not just when `activeStory `changes. We need to improve this code for not listening all, you can create an abstract class for control this. For now, it is no problem for our code but is a thing for change on the next steps.

A good refactoring is to isolate our components, we can use **containers pattern**.

But what we gain with this change? We will have a component reusable in any place without need your data provider is to be `Redux`. Also, this way is easier to test your component, because you just need pass the fixture to it and test. Without use **containers pattern** we need to use `MockStore` to test our components.

So an example of how to use containers on our example:

<script src="https://gist.github.com/leidsondias/ff40f2bbc505c473e6f56bea070a2864.js"></script>*Example 14 — Stories component without Redux*

So, now our component receives two params: *object *and the *loadStories *function. If you don’t know what `{ stories }` do, this is called the destructor you can found detail explanation [here](https://gist.github.com/leidsondias/ff40f2bbc505c473e6f56bea070a2864), but basically what this does is — extract the stories key from object I received on the params. *loadStories* are the same function that we import on the before examples. But this time we do not have a connection with **Redux**, **Actions, Reducers **or our **Event Emitter. **This way, you only have to pass data and the function to test the component. If you want, you can pass an empty function.

Our container is this:

<script src="https://gist.github.com/leidsondias/afed9535e1a6f54835ffbf104b5c48f9.js"></script>*Example 15 — Stories container*

The container has the `loadStories` action, responsibility for dispatch event to load data to store.

And now in the main file, we call the container instead of the component.

<script src="https://gist.github.com/leidsondias/3492766ac213fd69ebf6e35bdd8da301.js"></script>*Example 16 — main file from project*

If you want, you can create the container how like class. In my case I don’t guess is necessary, so just the function resolves my problem.

You can follow all the progress for the project [here](https://github.com/leidsondias/storiesJS) and contribute too. I’am writing slowly because I moved to another country and I have a lot to solve and take care of. But I will finish and hope in a few months.

I hope you have liked it and any suggestions or doubts are welcome. If you want correct my English I will like too hahaha ❤

The original post is https://medium.com/@leidsoncruz/web-components-with-redux-9e7c2da45602