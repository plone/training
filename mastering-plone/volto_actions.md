(volto-actions)=

# Volto Actions and Component State

````{sidebar} Volto chapter
```{figure} _static/volto.svg
:alt: Volto Logo
:align: left
```

This chapter is about the React frontend Volto.

Solve the same tasks in Plone Classic in chapter {doc}`viewlets_2`

---

**Get the code! ({doc}`More info <code>`)**

Code for the beginning of this chapter:

```shell
git checkout testing
```

Code for the end of this chapter:

```shell
git checkout REST-API-frontend-roundtrip
```
````

(volto-actions-overview-label)=

The Conference team placed a call for proposals.
Now the team wants to select talks.
To support this process we add a section to talk view from chapter {doc}`volto_talkview` where team members can vote for the talk.

Topics covered:

- actions: fetch data from backend and write data to backend
- component state: user interaction: call back to user before dispatching an action
- theming with Semantic-UI

```{figure} _static/volto_voting1.png
:alt: Volto Voting
:scale: 50%

Voting
```

```{figure} _static/volto_voting2.png
:alt: Volto Voting
:scale: 50%

Voting component, user has already voted
```

## Fetching data from backend and displaying

As you have seen in chapter {doc}`endpoints`, endpoints are created to provide the data we need: votes per talk plus info if the current user has the permission to vote on his talk.
Now we can fetch this data and display it.

We start with a component *Voting* to display votes.

{file}`src/components/Voting/Voting.jsx`

```{code-block} jsx
:linenos: true

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation } from 'react-router-dom';

import { Header, Label, List, Segment } from 'semantic-ui-react';

import { getVotes } from '~/actions';

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

On mount of the component the action `getVotes` is dispatched to fetch the data by `dispatch(getVotes(location.pathname));`.
The action fetches the data.
The corresponding reducer writes the data in global app store.
The component `Voting` as other components can now access the data from the app store by `const votes = useSelector((store) => store.votes);`.
The constant `votes` holds the necessary data for the current talk and user in a dictionary like

```{code-block} jsx
:linenos: true

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

Before we include the component *Voting* in talk view from chapter {doc}`volto_talkview`, some words about actions and reducers. The action `getVotes` fetches the data. The corresponding reducer writes the data in global app store.

The action `getVotes` is defined by the request method `get`, the address of the endpoint `votes` an and an identifier for the corresponding reducer to react.

```{code-block} jsx
:linenos: true

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

The reducer writes the data fetched by its action to app store.

```{code-block} jsx
:emphasize-lines: 20
:linenos: true

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

With a successfull action `getVotes`, the app store has an entry

```{code-block} jsx
:linenos: true

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

This data written by the reducer is the response of the request to \<backend>/<mailto:api/@votes>: <http://greenthumb.ch/api/@votes>, if your backend is available at <http://greenthumb.ch>.
It is the data that the adapter `Vote` from `starzel.votable_behavior` `behavior/voting.py` provides and exposes via the REST API endpoint `@votes`.

The component gets access to this store entry by `const votes = useSelector((store) => store.votes);`

Now we can include the component *Voting* in talk view from chapter {doc}`volto_talkview`.

```{code-block} jsx
:linenos: true

import { Voting } from '~/components';

const TalkView = ({ content }) => {
const color_mapping = {
    Beginner: 'green',
    Advanced: 'yellow',
    Professional: 'purple',
};

return (
    <Container id="page-talk">
    <h1 className="documentFirstHeading">
        {content.type_of_talk.title}: {content.title}
    </h1>
    <Voting />
```

```{figure} _static/volto_voting3.png
:alt: 'Volto Voting: displaying votes'
:scale: 50%
```

## Writing to the backend…

… and the clue about a React component

Now we can care about providing the actual voting feature.

We add a section to our `Voting` component.

```{code-block} jsx
:linenos: true

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
import { getVotes, vote, clearVotes } from '~/actions';
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
:linenos: true

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

As the corresponding reducer updates the app store, the subscribed component `Voting` **reacts by updating itself**. The subsription is done by just

```jsx
const votes = useSelector((store) => store.votes);
```

The component updates itself, it renders with the updated info about if the user has already voted, about the average vote and the total number of already posted votes. So the buttons disappear as we made the rendering conditional to `votes?.already_voted` which says if the current user has already voted.

Why is it possible that this info about the current user has been fetched by `getVotes`? Every request is done with the token of the logged in user.

The authorized user can now vote:

```{figure} _static/volto_voting1.png
:alt: Volto Voting
:scale: 50%
```

Observe that we do not calculate average votes and do not check if a user can vote via permissions, roles, whatsoever.
Every logic is done by the backend. We request votes and infos like 'can the current user do this and that' from the backend.

## Component State

Next step is the feature for developers to clear votes of a talk while preparing the app.
We want to offer a button to clear votes and integrate a hurdle to prevent unwanted clearing.
The user shall click and see a question if she really wants to clear the votes.

We are using the *component state* to be incremented before requesting the backend to definitly clear votes.

```{code-block} jsx
:emphasize-lines: 14
:linenos: true

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
:linenos: true

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
After a successfull `clearVotes` action the corresponding reducer updates the store.
As the component is subscribed to the store via `const votes = useSelector((store) => store.votes);` the component updates itself ( is rendered with the updated values ).
