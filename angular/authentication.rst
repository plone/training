Login
=====

Let's add a login/logout link in the top-right corner.

In our ``AppComponent``, we add a boolean property to manage the login status,
and we use the ``authentication`` service to set its value:

.. code-block:: ts

  export class AppComponent {

    logged = false;

    constructor(
      ...
    ) {
      ...
      this.plone.authentication.isAuthenticated.subscribe(auth => {
        this.logged = auth.state;
      });
    }

Now, if we are not logged in yet, we display in ``app.component.html`` a link to traverse to the ``@@login`` view:

.. code-block:: html+ng2

  <div class="row">
    <div class="col-md-12">
      <a *ngIf="!logged" traverseTo="@@login" class="pull-right">Login</a>
    </div>
  </div>

Let's implement the logout link.

..  admonition:: Solution
    :class: toggle

    We add a second link with an output bound to the ``click`` event, which will call the ``logout()`` method of our component.

    .. code-block:: html+ng2

        <div class="row">
          <div class="col-md-12">
            <a *ngIf="!logged" traverseTo="@@login" class="pull-right">Login</a>
            <a *ngIf="logged" (click)="logout()" class="pull-right">Logout</a>
          </div>
        </div>


    So let's define the ``logout()`` method:

    .. code-block:: ts

        logout() {
          this.plone.authentication.logout();
        }

Now if we create private contents in Plone, they won't show unless we are logged in.


