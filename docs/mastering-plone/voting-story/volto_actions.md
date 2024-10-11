---
myst:
  html_meta:
    "description": "Actions: fetch data from backend and write data to backend"
    "property=og:description": "Actions: fetch data from backend and write data to backend"
    "property=og:title": "Volto Actions and Component State"
    "keywords": "Plone, Volto, hooks, functional component, component state"
---

(volto-actions)=

# Volto Actions and component state [voting story]

````{card} Frontend chapter

````

(volto-actions-overview-label)=

The Conference team placed a call for proposals.
Now the jury wants to select talks.
To support this process we add a section to talk view from chapter {doc}`../volto_talkview` where jury members can vote for a talk.

Topics covered:

- actions: fetch data from backend and write data to backend
- component state: user interaction: call back to user before dispatching an action
- theming with Semantic-UI

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

## Requesting data from backend and displaying

As you have seen in chapter {doc}`endpoints`, endpoints are created to provide the data we need: votes per talk plus info if the current user has the permission to vote on his talk.
Now we can fetch this data and display it.

We start with a component _Voting_ to display votes.

{file}`src/components/Voting/Voting.jsx`

```{code-block} jsx
:linenos:
:emphasize-lines: 7,10,16

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation } from 'react-router-dom';

import { Header, Label, List, Segment } from 'semantic-ui-react';

import { getVotes } from '../../actions';

const Voting = () => {
  const votes = useSelector((store) => store.votes);
  const dispatch = useDispatch();
  let location = useLocation();
  const content = useSelector((store) => store.content.data);

  React.useEffect(() => {
    dispatch(getVotes(location.pathname));
  }, [dispatch, location]);

  return votes?.loaded && votes?.can_vote ? ( // is store content available? (votable behavior is optional)
    <Segment className="voting">
      <Header dividing>Conference Talk and Training Selection</Header>
      <List>
        <p>
          <Label.Group size="medium">
            {votes?.has_votes ? (
              <Label color="olive" ribbon>
                Average vote for this{' '}
                {content.type_of_talk?.title.toLowerCase()}:{' '}
                {votes?.average_vote}
                <Label.Detail>( Votes Cast {votes?.total_votes} )</Label.Detail>
              </Label>
            ) : (
              <b>
                There are no votes so far for this{' '}
                {content.type_of_talk?.title.toLowerCase()}.
              </b>
            )}
          </Label.Group>
        </p>
      </List>
    </Segment>
  ) : null;
};
export default Voting;
```

On mount of the component the action `getVotes` is dispatched by `dispatch(getVotes(location.pathname));`.
- The action fetches the data.
- The corresponding reducer writes the data in global app store.

The component `Voting` as well as any other component can now access the data from the global app store by subscribing with `const votes = useSelector((store) => store.votes);`.
Therefore the constant `votes` holds the necessary data for the current talk and user in a dictionary like

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
We receive all needed info for displaying from the one request of data including the info about the permission of the current user to vote.
Why do we need only one request? We designed the endpoint `votes` to provide all necessary information.


(volto-actions-store-label)=

### Actions, reducers and the app store

Before we include the component _Voting_ in talk view from chapter {doc}`../volto_talkview`, some words about actions and reducers.
The action `getVotes` requests the data.
The corresponding reducer writes the data to the global app store.

The action `getVotes` is defined by the request method `GET`, the address of the endpoint `votes` and an identifier `GET_VOTES` for the corresponding reducer to react.

`actions/votes/votes.js`
```{code-block} jsx
:linenos:

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

The reducer writes the data fetched by its action to the app store.

`reducers/votes/votes.js`
```{code-block} jsx
:emphasize-lines: 20
:linenos:

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

The action type identifiers are listed in `constants/ActionTypes.js` to keep reducer and action pairs in sync.

```js
/**
 * Add your action types here.
 * @module constants/ActionTypes
 * @example
 * export const UPDATE_CONTENT = 'UPDATE_CONTENT';
 */

export const GET_VOTES = 'GET_VOTES';
```

We now add our reducer to the overall Volto configuration:

`index.js`
```js
import { votes } from './reducers';

const applyConfig = (config) => {
  config.addonReducers.votes = votes;

  return config;
};

export default applyConfig;
```


With a successful action `getVotes`, the app store has an entry

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

The response is the data that the adapter `training.votable.behaviors.votable.Votable`  provides and exposes via the REST API endpoint `@votes`.

The component gets access to this store entry by subscribing to the store `const votes = useSelector((store) => store.votes);`


(volto-actions-including-slot-label)=

### Include the new component in the talk view

Now we can include the component `Voting` in a talk view from chapter {doc}`../volto_talkview`.

```{code-block} jsx
:linenos:
:emphasize-lines: 1-2,24-37

import { Container as SemanticContainer } from 'semantic-ui-react';
import { ContentTypeCondition } from '@plone/volto/helpers';
import { Voting } from 'volto-training-votable/components';
import { TalkView, TalkListingBlockVariation } from './components';

const applyConfig = (config) => {
  config.views = {
    ...config.views,
    contentTypesViews: {
      ...config.views.contentTypesViews,
      talk: TalkView,
    },
  };

  config.blocks.blocksConfig.listing.variations = [
    ...config.blocks.blocksConfig.listing.variations,
    {
      id: 'talks',
      title: 'Talks',
      template: TalkListingBlockVariation,
    },
  ];

  const Container =
    config.getComponent({ name: 'Container' }).component || SemanticContainer;
  const WrappedVoting = () => (
    <Container>
      <Voting />
    </Container>
  );

  config.registerSlotComponent({
    slot: 'aboveContent',
    name: 'voting',
    component: WrappedVoting,
    predicates: [ContentTypeCondition(['talk'])],
  });

  return config;
};

export default applyConfig;
```

```{figure} ../_static/volto_voting3.png
:alt: 'Volto Voting: displaying votes'
:scale: 50%
```

Check the `Redux` tab of Google developer tools to see the store changes forced by our reducer.
You can filter by "votes".

```{figure} ../_static/developertools_redux.png
:alt: 'Developer Tools Redux'
:scale: 40%
```


## Writing to the backend…

… and the clue about a React component

Now we can care about providing the actual voting feature.

We add a section to our `Voting` component.

```{code-block} jsx
:linenos:

<Divider horizontal section>
    Vote
</Divider>

{votes?.already_voted ? (
  <List.Item>
    <List.Content>
      <List.Header>
        You voted for this {content.type_of_talk?.title}.
      </List.Header>
      <List.Description>
        Please see more interesting talks and vote.
      </List.Description>
    </List.Content>
  </List.Item>
) : (
  <List.Item>
    <Button.Group widths="3">
      <Button color="green" onClick={() => handleVoteClick(1)}>
        Approve
      </Button>
      <Button color="blue" onClick={() => handleVoteClick(0)}>
        Do not know what to expect
      </Button>
      <Button color="orange" onClick={() => handleVoteClick(-1)}>
        Decline
      </Button>
    </Button.Group>
  </List.Item>
)}
```

We check if the user has already voted by `votes?.already_voted`.
We get this info from our `votes` subscriber to the app store.

After some info the code offers buttons to vote.
The click event handler `handleVoteClick` starts the communication with the backend by dispatching action `vote`.
We import this action from `src/actions`.

```jsx
import { getVotes, vote, clearVotes } from "../../actions";
```

The click event handler `handleVoteClick` dispatches the action `vote`:

```jsx
function handleVoteClick(value) {
  dispatch(vote(location.pathname, value));
}
```

The action `vote` is similar to our previous action `getvotes`. It is defined by the request method
`post` to submit the necessary data `rating`.

```{code-block} jsx
:emphasize-lines: 8
:linenos:

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

As the corresponding reducer updates the app store, the subscribed component `Voting` **reacts by updating itself**. The subsription is done by:

```jsx
const votes = useSelector((store) => store.votes);
```

The component updates itself, it renders with the updated info about if the user has already voted, about the average vote and the total number of already posted votes. So the buttons disappear as we made the rendering conditional to `votes?.already_voted` which says if the current user has already voted.

Why is it possible that this info about the current user has been fetched by `getVotes`?
Every request of a Volto app is done with the token of the logged in user.

The authorized user can now vote:

```{figure} ../_static/volto_voting1.png
:alt: Volto Voting
:scale: 50%
```

Observe that we do not calculate average votes and do not check if a user can vote via permissions, roles, whatsoever.
Every logic is done by the backend. We request votes and infos like 'can the current user do this and that' from the backend.

The reducer is enhanced by the voting part:

`src/reducers/votes/votes.js`

```{code-block} js
:emphasize-lines: 24,32,41
:linenos:

/**
 * Voting reducer.
 * @module reducers/votes/votes
 */

import { GET_VOTES, VOTE, CLEAR_VOTES } from '../../constants/ActionTypes';

const initialState = {
  loaded: false,
  loading: false,
  error: null,
};

/**
 * Voting reducer.
 * @function votes
 * @param {Object} state Current state.
 * @param {Object} action Action to be handled.
 * @returns {Object} New state.
 */
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

Next step is the feature for developers to clear votes of a talk while preparing the app.
We want to offer a button to clear votes and integrate a hurdle to prevent unwanted clearing.
The user shall click and see a question if she really wants to clear the votes.

We are using the _component state_ to be incremented before requesting the backend to definitely clear votes.

```{code-block} jsx
:emphasize-lines: 14
:linenos:

{votes?.can_clear_votes && votes?.has_votes ? (
  <>
    <Divider horizontal section color="red">
        Danger Zone
    </Divider>
    <List.Item>
      <Button.Group widths="2">
      <Button color="red" onClick={handleClearVotes}>
        {
          [
            'Clear votes for this item',
            'Are you sure to clear votes for this item?',
            'Votes for this item are reset.',
          ][stateClearVotes]
        }
      </Button>
      </Button.Group>
    </List.Item>
  </>
) : null}
```

This additional code snippet of our `Voting` component displays a delete button with a label depending of the to be incremented component state `stateClearVotes`.

The `stateClearVotes` component state is defined as value / accessor pair like this:

```jsx
const [stateClearVotes, setStateClearVotes] = useState(0);
```

The click event handler `handleClearVotes` distinguishes on the `stateClearVotes` component state to decide if it already dispatches the delete action `clearVotes` or if it waits for a second confirming click.

```{code-block} jsx
:emphasize-lines: 3
:linenos:

function handleClearVotes() {
  if (stateClearVotes === 1) {
    dispatch(clearVotes(location.pathname));
  }
  // count count counts to 2
  let counter = stateClearVotes < 2 ? stateClearVotes + 1 : 2;
  setStateClearVotes(counter);
}
```

You will see now that the clearing section disappears after clearing.
This is because it is conditional with `votes?.has_votes`.
After a successful `clearVotes` action the corresponding reducer updates the store.
As the component is subscribed to the store via `const votes = useSelector((store) => store.votes);` the component updates itself ( is rendered with the updated values ).
And the voting buttons are visible again.

For completnes, the action.
You have already guessed, it does a `DEL` request to the `@votes` endpoint.
And the endpoint service from last chapter knows what to do.

```js
/**
 * Delete votes of an item
 * @function clearVotes
 * @returns {Object} Votes action.
 */
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

```{note}
Get the code! 
[volto-training-votable](https://github.com/collective/volto-training-votable)
```