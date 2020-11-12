=======================
Javascript enhancements
=======================

Destructuring
=============

Destructuring arrays:

.. code-block:: jsx

    const [a, b, ...rest] = [10, 20, 30, 40, 50];


Destructuring objects:

.. code-block:: jsx

    const ({a, b, ...rest} = {a: 10, b: 20, c: 30, d: 40});

Provide fallback value

.. code-block:: jsx

    const ({a, b, e = 50, ...rest} = {a: 10, b: 20, c: 30, d: 40});


See more:
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment

Spread
======

Spread arrays:

.. code-block:: jsx

    let arr1 = [0, 1, 2];
    let arr2 = [3, 4, 5];

    arr1 = [...arr1, ...arr2];

Spread objects:

.. code-block:: jsx

    let obj1 = { foo: 'bar', x: 42 };
    let obj2 = { foo: 'baz', y: 13 };

    let clonedObj = { ...obj1 };

See more:
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax


Arrow functions
===============

.. code-block:: jsx

    const materials = [
      'Hydrogen',
      'Helium',
      'Lithium',
      'Beryllium'
    ];

    console.log(materials.map(material => material.length));
    // expected output: Array [8, 6, 7, 9]

See more: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
