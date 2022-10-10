---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Really short primer on Javascript enhancements

## Destructuring

Destructuring arrays:

```jsx
const [a, b, ...rest] = [10, 20, 30, 40, 50];
```

Destructuring objects:

```jsx
const ({a, b, ...rest} = {a: 10, b: 20, c: 30, d: 40});
```

Provide fallback value

```jsx
const ({a, b, e = 50, ...rest} = {a: 10, b: 20, c: 30, d: 40});
```

See more:
<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment>

## Spread

Spread arrays:

```jsx
let arr1 = [0, 1, 2];
let arr2 = [3, 4, 5];

arr1 = [...arr1, ...arr2];
```

Spread objects:

```jsx
let obj1 = { foo: 'bar', x: 42 };
let obj2 = { foo: 'baz', y: 13 };

let clonedObj = { ...obj1 };
```

See more:
<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax>

## Arrow functions

```jsx
const materials = [
  'Hydrogen',
  'Helium',
  'Lithium',
  'Beryllium'
];

console.log(materials.map(material => material.length));
// expected output: Array [8, 6, 7, 9]
```

See more: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>
