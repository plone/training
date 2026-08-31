---
myst:
  html_meta:
    "description": "Actions: fetch data from backend and write data to backend"
    "property=og:description": "Actions: fetch data from backend and write data to backend"
    "property=og:title": "Volto actions and component state"
    "keywords": "Plone, Volto, hooks, functional component, component state"
---

(volto-actions)=

# Volto actions and component state [voting story]

```{card}

In this part you will create the voting component which calls the backend to fetch and store votes.

Topics covered:

- Redux actions and reducers
- React component state
```

````{card}

Check out `mastering-plone-votable-add-on` at tag `endpoints`:

```shell
git checkout endpoints
```

The code at the end of the chapter:

```shell
git checkout actions
```

More info in {doc}`../code`
````

(volto-actions-overview-label)=

The conference team placed a call for proposals.
Now the program committee wants to select talks.
To support this process we will add a section to the talk view (from chapter {doc}`../volto_talkview`) where program committee members can vote for a talk.

```{figure} ../_static/volto_voting1.png
:alt: Volto Voting
:scale: 70%

Voting
```

```{figure} ../_static/volto_voting2.png
:alt: Volto Voting
:scale: 70%

Voting component, user has already voted
```


(volto-actions-fetching-label)=

## Request votes from the REST API

As you have seen in chapter {doc}`endpoints`, the `@votes` service was created to provide the data we need: votes per talk plus info if the current user has the permission to vote on this talk.
Now we can fetch this data and display it.

We start with a component to display votes.
Create the file {file}`frontend/packages/volto-ploneconf-votable/src/components/Voting/Voting.jsx`.

```{code-block} jsx
:linenos:
:emphasize-lines: 9,14-16

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation } from 'react-router-dom';
import { getVotes } from 'volto-ploneconf-votable/actions/votes/votes';
import config from '@plone/volto/registry';
import { Container as SemanticContainer } from 'semantic-ui-react';

const Voting = () => {
  const votes = useSelector((state) => state.votes);
  const dispatch = useDispatch();
  let location = useLocation();
  const content = useSelector((state) => state.content.data);

  React.useEffect(() => {
    dispatch(getVotes(location.pathname));
  }, [dispatch, location]);

  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;

  return votes?.loaded && votes?.can_vote ? ( // is store content available? (votable behavior is optional)
    <Container>
      <div className="ui segment voting">
        <div className="ui dividing header">
          Conference Talk and Training Selection
        </div>
        <div className="ui list">
          <div className="ui medium labels">
            {votes?.has_votes ? (
              <div className="ui olive ribbon label">
                Average vote for this{' '}
                {content.type_of_talk?.title.toLowerCase()}:{' '}
                {votes?.average_vote}
                <div className="detail">
                  ( Votes Cast {votes?.total_votes} )
                </div>
              </div>
            ) : (
              <div className="ui yellow ribbon label">
                There are no votes so far for this{' '}
                {content.type_of_talk?.title.toLowerCase()}.
              </div>
            )}
          </div>
        </div>
      </div>
      <br />
    </Container>
  ) : null;
};
export default Voting;
```

The `useEffect` hook runs after the component has been mounted.
It initiates the action `getVotes` by calling `dispatch(getVotes(location.pathname));`.
The action fetches the data, and the corresponding reducer stores the result in the global app store (provided by the Redux library).

The component `Voting` as well as any other component can now access the data from the global app store by subscribing with `const votes = useSelector((state) => state.votes);`.
Once the action has completed, `votes` will hold the necessary data for the current talk and user in an object in this format:

```{code-block} jsx
:linenos:

votes: {
  loaded: true,
  loading: false,
  error: null,
  already_voted: false,
  average_vote: 1,
  can_clear_votes: true,
  can_vote: true,
  has_votes: true,
  total_votes: 2
}
```

See the condition of the rendering function.
We receive all needed info for displaying from the one request including the info about the permission of the current user to vote.
Why do we need only one request?
We designed the endpoint `votes` to provide all necessary information.


(volto-actions-store-label)=

## Actions, reducers and the Redux store

Before we add the `Voting` component to the talk view, let's take a closer look at how the Redux store works.
The action `getVotes` starts a request to get the data from the API server.
The corresponding reducer writes the data to the global app store.

The action `getVotes` is defined by the request method `GET`, the address of the `@votes` endpoint and an identifier `GET_VOTES`.

{file}`frontend/packages/volto-ploneconf-votable/src/actions/votes/votes.js`

```{code-block} jsx
:linenos:

export const GET_VOTES = 'GET_VOTES';

export function getVotes(url) {
  return {
    type: GET_VOTES,
    request: {
      op: 'get',
      path: `${url}/@votes`,
    },
  };
}
```

The reducer writes the data from the response to the app store.

{file}`frontend/packages/volto-ploneconf-votable/src/reducers/votes/votes.js`

```{code-block} jsx
:emphasize-lines: 22
:linenos:

import { GET_VOTES } from 'volto-ploneconf-votable/actions/votes/votes';

const initialState = {
  loaded: false,
  loading: false,
  error: null,
};


export default function votes(state = initialState, action = {}) {
  switch (action.type) {
    case `${GET_VOTES}_PENDING`:
      return {
        ...state,
        error: null,
        loaded: false,
        loading: true,
      };
    case `${GET_VOTES}_SUCCESS`:
      return {
        ...state,
        ...action.result,
        error: null,
        loaded: true,
        loading: false,
      };
    case `${GET_VOTES}_FAIL`:
      return {
        ...state,
        error: action.error,
        loaded: false,
        loading: false,
      };
    default:
      return state;
  }
}
```

We have to add our reducer to the overall Volto configuration:

{file}`frontends/packages/volto-ploneconf-votable/src/config/settings.ts`

```js
import type { ConfigType } from '@plone/registry';
import votes from 'volto-ploneconf-votable/reducers/votes/votes';

export default function install(config: ConfigType) {
  config.addonReducers = {
    ...config.addonReducers,
    votes,
  };

  return config;
}
```


After a successful action `getVotes`, the app store has an entry

```{code-block} jsx
:linenos:

votes: {
  loaded: true,
  loading: false,
  error: null,
  already_voted: false,
  average_vote: 1,
  can_clear_votes: true,
  can_vote: true,
  has_votes: true,
  total_votes: 2
}
```

This data written by the reducer is the response of the request to `http://localhost:3000/++api++/talks/python-in-arts/@votes` which is proxied to `http://localhost:8080/Plone/talks/python-in-arts/@votes`.

The response is the data that the adapter `training.votable.behaviors.votable.Votable` provides and exposes via the REST API endpoint `@votes`.

The component gets access to this data by subscribing to the store with `const votes = useSelector((state) => state.votes);`


(volto-actions-including-slot-label)=

## Include the new component in the talk view

Now we can include the `Voting` component in the talk view.

{file}`frontend/packages/volto-ploneconf-votable/config/settings.ts`

```{code-block} jsx
:linenos:
:emphasize-lines: 6-10,18-23

import type { ConfigType } from '@plone/registry';
import type { Content } from '@plone/types';
import votes from 'volto-ploneconf-votable/reducers/votes/votes';
import Voting from 'volto-ploneconf-votable/components/Voting/Voting';

function FieldCondition(field: string) {
  return ({ content }: { content: Content }) => {
    return Boolean(content?.[field]);
  };
}

export default function install(config: ConfigType) {
  config.addonReducers = {
    ...config.addonReducers,
    votes,
  };

  config.registerSlotComponent({
    slot: 'aboveContent',
    name: 'voting',
    component: Voting,
    predicates: [FieldCondition('can_vote')],
  });

  return config;
}
```

We are registering the `Voting` component in the `aboveContent` slot.
It has a _predicate_ which is a condition for when to show the component.
The `FieldCondition` here will show the component only for content items that have the `can_vote` field (because they have our behavior enabled and the current user has permission to vote).

```{figure} ../_static/volto_voting3.png
:alt: 'Volto Voting: displaying votes'
:scale: 50%
```

Check the `Redux` tab of the browser developer tools to see the store changes made by our reducer.
You can filter by "votes".

```{figure} ../_static/developertools_redux.png
:alt: 'Developer Tools Redux'
:scale: 40%
```


## Write votes to the REST API

Now we can add the actions to actually place a vote.

We add a section to our `Voting` component.

{file}`frontend/packages/volto-ploneconf-votable/src/components/Voting/Voting.jsx`

```{code-block} jsx
:linenos:

          <div className="ui horizontal section divider">Vote</div>
          {votes?.already_voted ? (
            <div className="item">
              <div className="content">
                <div className="header">
                  You voted for this {content.type_of_talk?.title}.
                </div>
                <div className="description">
                  Please review more interesting talks and vote.
                </div>
              </div>
            </div>
          ) : (
            <div className="item">
              <div className="ui buttons">
                <button
                  type="button"
                  className="ui green button"
                  onClick={() => handleVoteClick(1)}
                >
                  Approve
                </button>
                <button
                  type="button"
                  className="ui blue button"
                  onClick={() => handleVoteClick(0)}
                >
                  Do not know what to expect
                </button>
                <button
                  type="button"
                  className="ui red button"
                  onClick={() => handleVoteClick(-1)}
                >
                  Decline
                </button>
              </div>
            </div>
          )}
```

We check if the user has already voted with `votes?.already_voted`.
We get this info from our `votes` data selected from the app store state.

If the user has not voted yet, the component shows buttons to vote.
The click event handler `handleVoteClick` starts the communication with the backend by dispatching the `vote` action.
We import this action from `src/actions`.

```jsx
import { getVotes, vote, clearVotes } from 'volto-ploneconf-votable/actions/votes/votes';
```

The click event handler `handleVoteClick` dispatches the action `vote`:

```jsx
  const handleVoteClick = (value) => {
    dispatch(vote(location.pathname, value));
  };
```

The action `vote` is similar to our previous action `getVotes`.
It creates a request to submit the rating to the `@votes` POST endpoint.

{file}`frontend/packages/volto-ploneconf-votable/src/actions/votes/votes.js`

```{code-block} jsx
:emphasize-lines: 8
:linenos:

export const VOTE = 'VOTE';

export function vote(url, vote) {
  if ([-1, 0, 1].includes(vote)) {
    return {
      type: VOTE,
      request: {
        op: 'post',
        path: `${url}/@votes`,
        data: { rating: vote },
      },
    };
  }
}
```

As the corresponding reducer updates the app store, the subscribed component `Voting` reacts by updating itself.
The subscription is done with:

```jsx
const votes = useSelector((state) => state.votes);
```

The component updates itself, it renders with the updated info about if the user has already voted, about the average vote and the total number of already posted votes.
So the buttons disappear as we made the rendering conditional to `votes?.already_voted` which checks whether the current user has already voted.

Why is it possible that this info about the current user has been fetched by `getVotes`?
Every request of a Volto app is done with the token of the logged in user.

The authorized user can now vote:

```{figure} ../_static/volto_voting1.png
:alt: Volto Voting
:scale: 50%
```

Observe that we do not calculate average votes and do not check if a user can vote via permissions, roles, whatsoever.
This logic is done in the backend.
We request votes and information like 'can the current user do this and that' from the backend.

The reducer is enhanced to handle the `VOTE` action:

{file}`frontend/volto-ploneconf-votable/src/reducers/votes/votes.js`

```{code-block} js
:emphasize-lines: 3,15,23,32
:linenos:

import {
  GET_VOTES,
  VOTE,
} from 'volto-ploneconf-votable/actions/votes/votes';

const initialState = {
  loaded: false,
  loading: false,
  error: null,
};

export default function votes(state = initialState, action = {}) {
  switch (action.type) {
    case `${GET_VOTES}_PENDING`:
    case `${VOTE}_PENDING`:
      return {
        ...state,
        error: null,
        loaded: false,
        loading: true,
      };
    case `${GET_VOTES}_SUCCESS`:
    case `${VOTE}_SUCCESS`:
      return {
        ...state,
        ...action.result,
        error: null,
        loaded: true,
        loading: false,
      };
    case `${GET_VOTES}_FAIL`:
    case `${VOTE}_FAIL`:
      return {
        ...state,
        error: action.error,
        loaded: false,
        loading: false,
      };
    default:
      return state;
  }
}
```

## Component state

Finally, let's add a feature for developers to clear votes of a talk while preparing the app.
We want to offer a button to clear votes and integrate a hurdle to prevent unwanted clearing.
The user shall click and see a question to confirm whether to clear the votes.

We are using the _component state_ to be incremented before requesting the backend to definitely clear votes.

```{code-block} jsx
:linenos:

          {votes?.can_clear_votes && votes?.has_votes ? (
            <>
              <div className="ui red horizontal section divider">
                Danger Zone
              </div>
              <div className="item">
                <button className="ui red button" onClick={handleClearVotes}>
                  {
                    [
                      'Clear votes for this item',
                      'Are you sure to clear votes for this item?',
                      'Votes for this item are reset.',
                    ][stateClearVotes]
                  }
                </button>
              </div>
            </>
          ) : null}
```

This additional code snippet of our `Voting` component displays a delete button with a label depending on the component state `stateClearVotes`.

The `stateClearVotes` component state is defined as a value/accessor pair like this:

```jsx
const [stateClearVotes, setStateClearVotes] = useState(0);
```

The click event handler `handleClearVotes` distinguishes on the `stateClearVotes` component state to decide if it already dispatches the delete action `clearVotes` or if it waits for a second confirming click.

```{code-block} jsx
:emphasize-lines: 3
:linenos:

  const handleClearVotes = () => {
    if (stateClearVotes === 1) {
      dispatch(clearVotes(location.pathname));
    }
    // increment count up to 2
    let counter = stateClearVotes < 2 ? stateClearVotes + 1 : 2;
    setStateClearVotes(counter);
  };
```

For completeness, we need the `clearVotes` action.
As you have already guessed, it does a `DELETE` request to the `@votes` endpoint.

```{code-block} js
:linenos:

export const CLEAR_VOTES = 'CLEAR_VOTES';

export function clearVotes(url) {
  return {
    type: CLEAR_VOTES,
    request: {
      op: 'del',
      path: `${url}/@votes`,
    },
  };
}
```

You will see now that the clearing section disappears after clearing.
This is because it is conditional with `votes?.has_votes`.
After a successful `clearVotes` action the corresponding reducer updates the store.
As the component is subscribed to the store via `const votes = useSelector((state) => state.votes);` the component updates itself (it is re-rendered with the updated values).
And the voting buttons are visible again.
