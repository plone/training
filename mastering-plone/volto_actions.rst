.. _volto_actions:

Volto Actions
=====================

.. sidebar:: Volto chapter

  .. figure:: _static/volto.svg
     :alt: Volto Logo

  This chapter is about the React frontend Volto.

  Solve the same tasks in Plone Classic in chapter :doc:`viewlets_2`

.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

        git checkout testing

   Code for the end of this chapter::

        git checkout REST-API-frontend-roundtrip

.. _volto-actions-overview-label:


The Conference team placed a call for proposals. Now the team wants to select talks. To support this process we add a section to talk view from chapter :doc:`volto_talkview` where team members can vote for the talk.


Topics covered:

* actions: fetch data from backend
* component state: user interaction: call back to user before dispatching an action
* theming with Semantic-UI


.. figure:: _static/volto_voting1.png
    :scale: 50%
    :alt: Volto Voting

    Voting

.. figure:: _static/volto_voting2.png
    :scale: 50%
    :alt: Volto Voting

    Voting component, user has already voted


Fetching data from backend and displaying
-----------------------------------------

As you have seen in chapter :doc:`endpoints`, endpoints are created to provide the data we need: votes per talk plus info if the current user has the permission to vote on his talk.
Now we can fetch this data and display it.

We start with a component *Voting* to display existing votes.

:file:`src/components/Voting/Voting.jsx`

..  code-block:: jsx
    :linenos:

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
            {votes?.has_votes ? (
            <p>
                <Label.Group size="medium">
                <Label color="olive" ribbon>
                    Average vote for this {content.type_of_talk?.title}: {votes?.average_vote}
                    <Label.Detail>( Votes Cast {votes?.total_votes} )</Label.Detail>
                </Label>
                </Label.Group>
            </p>
            ) : null}
        </List>
        </Segment>
    ) : null;
    };
    export default Voting;

On mount of the component the action `getVotes` is dispatched to fetch the data by `dispatch(getVotes(location.pathname));`.
The action fetches the data. The corresponding reducer writes the data in global app store.
The component `Voting` as other components can now access the data from the app store by `const votes = useSelector((store) => store.votes);`.
The constant `votes` holds the necessary data for the current talk and user in a dictionary like

.. code-block:: json
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

See the condition of the rendering function.
We receive all needed info for displaying from the one request of data including the info about the permission of the current user to vote.
Why do we need only one request? We designed the endpoint `votes` to provide all necessary information.

Before we include the component *Voting* in talk view from chapter :doc:`volto_talkview`, some words about actions and reducers. The action `getVotes` fetches the data. The corresponding reducer writes the data in global app store.

The action `getVotes` is defined by the request method `get`, the address of the endpoint `votes` an and an identifier for the corresponding reducer to react.

.. code-block:: jsx
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

The reducer writes the data fetched by its action to app store.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 20

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

With a successfull action `getVotes`, the app store has an entry 

.. code-block:: json
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

The component gets access to this store entry by `const votes = useSelector((store) => store.votes);`

Now we can include the component *Voting* in talk view from chapter :doc:`volto_talkview`.

.. code-block:: jsx
    :linenos:

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


Communication with the backend: vote for a talk, let admin clear votes info for a talk
-----------------

Now we can care about providing the actual voting feature.

TODO

The admin has the permission …


