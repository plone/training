---
myst:
  html_meta:
    "description": "Redux"
    "property=og:description": "Redux"
    "property=og:title": "Redux"
    "keywords": "Volto, Plone, Configuration"
---

# Redux

Redux is the app-state store that Volto uses.
It's been the gold standard in this matter since years ago.
It's deep integration into React lifecycle allows the app to update the wired components and adapt each time that the store updates.

It's based in actions/reducers pattern and it's used all across Volto.
Volto uses it also to store server-state on it, updating every time that the server state changes.

Volto's use of Redux is "typical" and you can find plenty examples in Volto's code base.

In modern Redux, a component can connect with a value in the store.
In class components:

```jsx
export default compose(
  withRouter,
  injectIntl,
  connect(
    (state, props) => ({
      loading: state.emailNotification.loading,
      loaded: state.emailNotification.loaded,
      error: state.emailNotification.error,
      pathname: props.location.pathname,
    }),
    { emailNotification },
  ),
)(ContactForm);
```

and in functional components using `useSelector` hook:

```jsx
import React from 'react';
import { formatDate, long_date_format } from '@plone/volto/helpers/Utils/Date';
import { useSelector } from 'react-redux';

/**
 * Friendly formatting of dates
 */
const FormattedDate = ({
  date,
  format,
  long,
  includeTime,
  relative,
  className,
  locale,
  children,
}) => {
  const language = useSelector((state) => locale || state.intl.locale);
  const toDate = (d) => (typeof d === 'string' ? new Date(d) : d);
  const args = { date, long, includeTime, format, locale: language };

  return (
    <time
      className={className}
      dateTime={date}
      title={new Intl.DateTimeFormat(language, long_date_format).format(
        new Date(toDate(date)),
      )}
    >
      {children
        ? children(
            formatDate({
              ...args,
              formatToParts: true,
            }),
          )
        : formatDate(args)}
    </time>
  );
};
```

